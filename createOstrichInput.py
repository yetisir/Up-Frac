#!/usr/bin/env python3

import sys
import os
import csv
from OSTRICH.vectorMath import *
import math
import argparse
import importlib
import pickle
import numpy
import statistics

def getMaxStrain():
    
    return 0.05

def getVelocityString(velTable):
    accelTime = velTable[-1]/10
    amp = -1
    vString = '((0, {0}), '.format(amp)
    for i in range(len(velTable)-1):
        vString += '({0}, {1}), ({2}, {3}), '.format(velTable[i]-accelTime, amp, velTable[i]+accelTime, amp*-1)
        amp = amp*-1
    vString += '({0}, {1}))'.format(velTable[-1], amp)
    return vString
    
def getInelasticStrain(numStrainPoints = 100):
    inelasticStrain = divide(range(0, numStrainPoints+1), numStrainPoints/getMaxStrain())
    return inelasticStrain

                                
def maxTensileStrainIO(mode):
    fName = os.path.join('OSTRICH', 'data', '{0}_modelParameters.dat'.format(mName))
    if mode == 'r':
        with open(fName, 'r') as file:
            maxTensileStrain = float(file.readline().split()[0] )
        return maxTensileStrain
    elif mode == 'w':
        with open(fName, 'w') as file:        
            file.write(str(getMaxStrain())) 
        return 1
        
def getBoundaryDisplacements(parameterizationRun):
    displacements = []
    for k in range(len(modelData.confiningStress)):
        with open(os.path.join('HOMOGENIZE', 'binaryData', '{0}({1}.{2})_homogenizedData.pkl'.format(modelData.modelName, parameterizationRun, k)), 'rb') as bundleFile:
            bundle = pickle.load(bundleFile)
            timeHistory = bundle[0]
            stressHistory = bundle[1]
            strainHistory = bundle[2]
        LE11 = [x[0,0] for x in strainHistory]
        LE22 = [x[1,1] for x in strainHistory]
        
        U1 = [x*modelData.modelSize for x in LE11]
        U2 = [x*modelData.modelSize for x in LE22]

        v1Tuple = [(timeHistory[i], U1[i]) for i in range(len(timeHistory))]
        v2Tuple = [(timeHistory[i], U2[i]) for i in range(len(timeHistory))]
        displacements.append((v1Tuple, v2Tuple))
    return displacements
        
def getBoundaryStresses(parameterizationRun):
    stresses = []
    for k in range(len(modelData.confiningStress)):
        with open(os.path.join('HOMOGENIZE', 'binaryData', '{0}({1}.{2})_homogenizedData.pkl'.format(modelData.modelName, parameterizationRun, k)), 'rb') as bundleFile:
            bundle = pickle.load(bundleFile)
            timeHistory = bundle[0]
            stressHistory = bundle[1]
            strainHistory = bundle[2]
        S11 = [-x[0,0] for x in stressHistory]
        S22 = [-x[1,1] for x in stressHistory]
        
        S1Tuple = [(timeHistory[i], S11[i]) for i in range(len(timeHistory))]
        S2Tuple = [(timeHistory[i], S22[i]) for i in range(len(timeHistory))]
        stresses.append((S1Tuple, S2Tuple))
    return stresses
        
def getModelParameters(parameterizationRun):

    parameters =  {'$$mSize': modelData.modelSize,
                            '$$mName': '\''+modelData.modelName+'\'',
                            '$$sName': ['{0}({1}.{2})'.format(modelData.modelName, 0, x) for x in range(len(modelData.confiningStress))],
                            '$$nSteps': modelData.numberOfSteps,
                            '$$rho': modelData.rho,
                            '$$confStress': [x for x in modelData.confiningStress], #***********************************************************fix for different confining stresses!!!!!
                            '$$approxStrain': modelData.velocity[parameterizationRun]*modelData.simulationTime[parameterizationRun]/modelData.modelSize,
                            '$$vel':modelData.velocity[parameterizationRun],
                            '$$sTime':modelData.simulationTime[parameterizationRun],
                            '$$vString':getVelocityString(modelData.velocityTable[parameterizationRun]),
                            '$$boundaryDisplacements': getBoundaryDisplacements(parameterizationRun),
                            '$$boundaryStresses': getBoundaryStresses(parameterizationRun),
                            '$$relVars': modelData.relevantMeasurements, 
                            '$$abaqusMaterial':'\''+modelData.abaqusMaterial+'\''}
    return parameters
                                
def getOstrichParameters(parameterizationRun, optimizer, frontBias=1):
    ostrichParametersText = '' 
    ostrichParameters = material.ostrichParameters.keys()
    for parameter in ostrichParameters:
            p = material.ostrichParameters[parameter]
            newRecord = '$' + parameter + '\t' + str(p['init']) + '\t' + str(p['low']) + '\t' +str(p['high']) +'\tnone\tnone\tnone\n'
            ostrichParametersText += newRecord
 
    observations = ''
    obsNo = 0
    for k in range(len(modelData.confiningStress)):
        with open(os.path.join('HOMOGENIZE', 'binaryData', '{0}({1}.{2})_homogenizedData.pkl'.format(modelData.modelName, parameterizationRun, k)), 'rb') as bundleFile:
            bundle = pickle.load(bundleFile)
            timeHistory = bundle[0]
            stressHistory = bundle[1]
            strainHistory = bundle[2]
        averageS11 = statistics.mean([x[0, 0] for x in stressHistory])
        averageS22 = statistics.mean([x[1, 1] for x in stressHistory])
        averageS12 = statistics.mean([x[0, 1] for x in stressHistory])
        averageLE11 = statistics.mean([x[0, 0] for x in strainHistory])
        averageLE22 = statistics.mean([x[1, 1] for x in strainHistory])
        averageLE12 = statistics.mean([x[0, 1] for x in strainHistory])
        averageS = (averageS11+averageS12+averageS22)/3
        averageLE = (averageLE11+averageLE12+averageLE22)/3
        
        numObservations = len(timeHistory) + 1
        #TODO: add weightings so strain and stress can be used together
        for i in range(1, numObservations):
            for j in range(len(modelData.relevantMeasurements)):
                if modelData.relevantMeasurements[j] == 'S11':
                    o = stressHistory[i-1][0, 0]
                    c = 2
                    # w = 1/averageS
                    w = 1
                elif modelData.relevantMeasurements[j] == 'S22':
                    o = stressHistory[i-1][1, 1]
                    c = 3
                    # w = 1/averageS
                    w = 1
                elif modelData.relevantMeasurements[j] == 'S12':
                    o = stressHistory[i-1][0, 1]
                    c = 4
                    # w = 1/averageS
                    w = 1
                elif modelData.relevantMeasurements[j] == 'LE11':
                    o = strainHistory[i-1][0, 0]
                    c = 5
                    # w = 1/averageLE
                    w = 1
                elif modelData.relevantMeasurements[j] == 'LE22':
                    o = strainHistory[i-1][1, 1]
                    c = 6
                    # w = 1/averageLE
                    w = 1
                elif modelData.relevantMeasurements[j] == 'LE12':
                    o = strainHistory[i-1][0, 1]
                    c = 7
                    # w = 1/averageLE
                    w = 1
                if str(o) != str(numpy.NaN):
                    l = k*(numObservations-1)+ i 
                    #obsNo = k*(numObservations-1)*len(modelData.relevantMeasurements) + (i-1)*len(modelData.relevantMeasurements) + (j +1)
                    obsNo += 1
                    bias = frontBias
                    w = w*((1-bias)/numObservations*i+bias)
                    newObservation = 'obs{} \t\t{:10f} \t{} \toutput.dat \tOST_NULL \t{} \t\t{}\n'.format(obsNo, o, w, l, c)
                    observations += newObservation

    parameters = {'$$ostrichParameters':ostrichParametersText, 
                  '$$ostrichObservations':observations,
                  '$$pType':optimizer}



    return parameters
    
def getModelConstants(parameterizationRun):
    parameters = {}
    for parameter in material.ostrichParameters:
        parameters[parameter] = parameter
    for i in range(parameterizationRun-1):
         with open(os.path.join('OSTRICH', 'ostOutput', 'OstOutput_{0}_{1}.txt'.format(modelData.modelName, i+1))) as ostOutputFile:
            ostOutput = ostOutputFile.read()
            startIndex = ostOutput.find('Optimal Parameter Set')
            endIndex = ostOutput.find('\n\n', startIndex)
            parameterBlock = ostOutput[startIndex:endIndex+1]
            for parameter in materialParameters[i]:
                paramPosition = parameterBlock.find(parameter)
                colonPosition = parameterBlock.find(':', paramPosition)
                eolPosition = parameterBlock.find('\n', paramPosition)
                value = float(parameterBlock[colonPosition+1:eolPosition])
                parameters[parameter] = value
    parameters['$$$materialDef'] = material.abaqusTemplate
    return parameters
     
def fillTemplate(template, parameters, file):
    with open(os.path.join('OSTRICH', template), 'r') as templateFile:
        t = templateFile.read()
        for i in parameters.keys():
            t = t.replace(i, str(parameters[i]))
        with open(os.path.join('OSTRICH', file), 'w') as modelFile:
            modelFile.write(t)
            

def importModelData(modelName):
    global modelData
    modelData = importlib.import_module('UDEC.modelData.'+modelName)

def importMaterialData(materialName):
    global material
    material = importlib.import_module('OSTRICH.materials.'+materialName)

def run(modelName, parameterizationRun):
    importModelData(modelName)
    importMaterialData(modelData.abaqusMaterial)
    main(parameterizationRun)

def main(parameterizationRun, optimizer='ParticleSwarm'):
    fillTemplate('parameters.tpl', getModelParameters(parameterizationRun-1), 'parameters.py')
    fillTemplate('ostIn.tpl', getOstrichParameters(parameterizationRun-1, optimizer), 'ostIn.txt')
    fillTemplate('runAbaqus.tpl', getModelConstants(parameterizationRun-1), 'runAbaqus.temp.tpl') 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='createOstrichInput: Creates the Neccessary Input files to Run OSTIRCH')
    parser.add_argument('-n', '--name', required=True, help='Name of the file containing the model data without the extension')
    parser.add_argument('-r', '--run', required=True, type=int, help='Parameterization run number')
    parser.add_argument('-o', '--optimizer', default='ParticleSwarm', help='optimization algorithm')

    args = parser.parse_args()
    modelName = args.name
    parameterizationRun = args.run
    optimizer = args.optimizer
    
    importModelData(modelName)
    importMaterialData(modelData.abaqusMaterial)
    main(parameterizationRun, optimizer)
 
  

#!/usr/bin/env python3

import sys
import os
import csv
from OSTRICH.vectorMath import *
import math
import argparse
import importlib
import pickle

def getMaxStrain():
    with open(os.path.join('OSTRICH', 'observationUDEC.dat')) as udecFile:
        udecData = csv.reader(udecFile, delimiter=' ')
        next(udecData, None)  # skip the header
        strains = [abs(float(item)) for sublist in [row[4:-1] for row in udecData] for item in sublist]
    return max(strains)

def getVelocityString(velTable):
    accelTime = velTable[-1]/10
    amp = -1
    vString = '((0, {0}), '.format(amp)
    for i in range(len(velTable)-1):
        vString += '({0}, {1}), ({2}, {3}), '.format(velTable[i]-accelTime, amp, velTable[i]+accelTime, amp*-1)
        amp = amp*-1
    vString += '({0}, {1}))'.format(velTable[-1], amp)
    return vString
    
# def getCrackingStrain(numStrainPoints = 100):
    # if '(t)' in modelName:
        # crackingStrain = divide(range(0, numStrainPoints+1), numStrainPoints/getMaxStrain())
    # elif '(c)' in modelName:
        # crackingStrain = divide(range(0, numStrainPoints+1), numStrainPoints/maxTensileStrainIO('r'))
    # return crackingStrain
    
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
        
def getModelParameters(parameterizationRun):

    parameters =  {'$$mSize': modelData.modelSize,
                            '$$mName': '\''+modelData.modelName+'\'',
                            '$$sName': ['{0}({1}.{2})'.format(modelData.modelName, 0, x) for x in modelData.confiningStress],
                            '$$nSteps': modelData.numberOfSteps,
                            '$$rho': modelData.rho*1e9,
                            '$$confStress': [x*1e6 for x in modelData.confiningStress], #***********************************************************fix for different confining stresses!!!!!
                            '$$cStrain': getInelasticStrain(), #fix for concrete plasticity
                            '$$iStrain': getInelasticStrain(),
                            '$$vel':modelData.velocity[parameterizationRun],
                            '$$sTime':modelData.simulationTime[parameterizationRun],
                            '$$vString':getVelocityString(modelData.velocityTable[parameterizationRun])}
    return parameters
                                
def getOstrichParameters(parameterizationRun):
    ostrichParametersText = '' 
    ostrichParameters = material.ostrichParameters.keys()
    for parameter in ostrichParameters:
            p = material.ostrichParameters[parameter]
            newRecord = '$' + parameter + '\t' + str(p['init']) + '\t' + str(p['low']) + '\t' +str(p['high']) +'\tnone\tnone\tnone\n'
            ostrichParametersText += newRecord
 
    observations = ''
    obsNo = 0
    for k in range(len(modelData.confiningStress)):
        with open(os.path.join('HOMOGENIZE', 'binaryData', '{0}({1}.{2})_homogenizedData.pkl'.format(modelData.modelName, parameterizationRun, modelData.confiningStress[k])), 'rb') as bundleFile:
            bundle = pickle.load(bundleFile)
            timeHistory = bundle[0]
            stressHistory = bundle[1]
            strainHistory = bundle[2]

        numObservations = len(timeHistory) + 1
        #TODO: add weightings so strain and stress can be used together
        for i in range(1, numObservations):
            for j in range(len(modelData.relevantMeasurements)):
                if modelData.relevantMeasurements[j] == 'S11':
                    o = stressHistory[i-1][0, 0]
                    c = 2
                elif modelData.relevantMeasurements[j] == 'S22':
                    o = stressHistory[i-1][1, 1]
                    c = 3
                elif modelData.relevantMeasurements[j] == 'S12':
                    o = stressHistory[i-1][0, 1]
                    c = 4
                elif modelData.relevantMeasurements[j] == 'LE11':
                    o = strainHistory[i-1][0, 0]
                    c = 5
                elif modelData.relevantMeasurements[j] == 'LE22':
                    o = strainHistory[i-1][1, 1]
                    c = 6
                elif modelData.relevantMeasurements[j] == 'LE12':
                    o = strainHistory[i-1][0, 1]
                    c = 7
                l = i + 1 
                #obsNo = k*(numObservations-1)*len(modelData.relevantMeasurements) + (i-1)*len(modelData.relevantMeasurements) + (j +1)
                obsNo += 1
                newObservation = 'obs{} \t\t{:10f} \t1 \toutput.dat \tOST_NULL \t{} \t\t{}\n'.format(obsNo, o, l, c)
                observations += newObservation

    parameters = {'$$ostrichParameters':ostrichParametersText, 
                            '$$ostrichObservations':observations}



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

def main(parameterizationRun):
    fillTemplate('parameters.tpl', getModelParameters(parameterizationRun-1), 'parameters.py')
    fillTemplate('ostIn.tpl', getOstrichParameters(parameterizationRun-1), 'ostIn.txt')
    fillTemplate('runAbaqus.tpl', getModelConstants(parameterizationRun-1), 'runAbaqus.temp.tpl') 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='createOstrichInput: Creates the Neccessary Input files to Run OSTIRCH')
    parser.add_argument('-n', '--name', required=True, help='Name of the file containing the model data without the extension')
    parser.add_argument('-r', '--run', required=True, type=int, help='Parameterization run number')

    args = parser.parse_args()
    modelName = args.name
    parameterizationRun = args.run
    
    importModelData(modelName)
    importMaterialData(modelData.abaqusMaterial)
    main(parameterizationRun)
 
        
        
        
      




















# def createOstIn(fileName, parameters):
    # #TODO: change import format, use template, not module maybe?
    # observations = ''
    # for k in range(len(confiningStress)):
        # with open(os.path.join('HOMOGENIZE', 'binaryData', fileName+str(confiningStress[k])+')_homogenizedData.pkl'), 'rb') as bundleFile:
            # bundle = pickle.load(bundleFile)
            # timeHistory = bundle[0]
            # stressHistory = bundle[1]
            # strainHistory = bundle[2]

        # numObservations = len(timeHistory) + 1
        # #TODO: add weightings so strain and stress can be used together
        # for i in range(1, numObservations):
            # for j in range(len(parameters)):
                # if parameters[j] == 'S11':
                    # o = stressHistory[i-1][0, 0]
                    # c = 2
                # elif parameters[j] == 'S22':
                    # o = stressHistory[i-1][1, 1]
                    # c = 3
                # elif parameters[j] == 'S12':
                    # o = stressHistory[i-1][0, 1]
                    # c = 4
                # elif parameters[j] == 'LE11':
                    # o = strainHistory[i-1][0, 0]
                    # c = 5
                # elif parameters[j] == 'LE22':
                    # o = strainHistory[i-1][1, 1]
                    # c = 6
                # elif parameters[j] == 'LE12':
                    # o = strainHistory[i-1][0, 1]
                    # c = 7
                # l = k*(numObservations+startIndex) + i + 1 + startIndex
                # obsNo = k*(numObservations-1)*len(parameters) + (i-1)*len(parameters) + (j +1)
                # newObservation = 'obs{} \t\t{:10f} \t1 \toutput.dat \tOST_NULL \t{} \t\t{}\n'.format(obsNo, o, l, c)
                # observations += newObservation
    # with open(os.path.join('OSTRICH', 'OstIn.tpl'), 'w') as f:
        # f.write(OSTRICH.ostIn.topText+observations+OSTRICH.ostIn.bottomText)
      
        
        
        
        

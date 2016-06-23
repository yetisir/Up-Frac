#!/usr/bin/env python3

import sys
import os
import csv
import math
import argparse
import importlib
import pickle
import numpy

def getVelocityString(velTable):
    accelTime = velTable[-1]/10
    amp = -1
    vString = '((0, {0}), '.format(amp)
    for i in range(len(velTable)-1):
        vString += '({0}, {1}), ({2}, {3}), '.format(velTable[i]-accelTime, amp, velTable[i]+accelTime, amp*-1)
        amp = amp*-1
    vString += '({0}, {1}))'.format(velTable[-1], amp)
    return vString
    

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
                            '$$abaqusMaterial':'\''+modelData.abaqusMaterial+'\''}
    return parameters
                                
def getOstrichParameters(parameterizationRun):
    ostrichParametersText = '' 
    ostrichParameters = material.ostrichParameters.keys()
    for parameter in ostrichParameters:
            p = material.ostrichParameters[parameter]
            newRecord = '$' + parameter + '\t' + str(p['init']) + '\t' + str(p['low']) + '\t' +str(p['high']) +'\tnone\tnone\tnone\n'
            ostrichParametersText += newRecord
 
    parameters = {'$$ostrichParameters':ostrichParametersText, 
                            '$$ostrichObservations':observations}



    return parameters
    
def getModelConstants(fittedName):
    parameters = {}
    for parameter in material.ostrichParameters:
        parameters['${0}'.format(parameter)] = parameter
    for i in range(len(modelData.velocityTable)):
         with open(os.path.join('OSTRICH', 'ostOutput', 'OstOutput_{0}_{1}_{2}.txt'.format(fittedName, modelData.abaqusMaterial,i+1))) as ostOutputFile:
            ostOutput = ostOutputFile.read()
            startIndex = ostOutput.find('Optimal Parameter Set')
            endIndex = ostOutput.find('\n\n', startIndex)
            parameterBlock = ostOutput[startIndex:endIndex+1]
            for parameter in material.ostrichParameters:
                paramPosition = parameterBlock.find(parameter)
                colonPosition = parameterBlock.find(':', paramPosition)
                eolPosition = parameterBlock.find('\n', paramPosition)
                value = float(parameterBlock[colonPosition+1:eolPosition])
                parameters['${0}'.format(parameter)] = value
    print(parameters)
    return parameters
    
    
def getMaterialConstants():
    parameters = {'$$$materialDef':material.abaqusTemplate}
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
    print(modelData.abaqusMaterial)

def importMaterialData(materialName):
    global material
    material = importlib.import_module('OSTRICH.materials.'+materialName)

def run(modelName, parameterizationRun, fittedName):
    importModelData(modelName)
    importMaterialData(modelData.abaqusMaterial)
    main(parameterizationRun, fittedName)

def main(parameterizationRun, fittedName):
    fillTemplate('parameters.tpl', getModelParameters(parameterizationRun-1), 'parameters.py')
    fillTemplate('runAbaqus.tpl', getMaterialConstants(), 'runAbaqus.temp.tpl') 
    fillTemplate('runAbaqus.temp.tpl', getModelConstants(fittedName), 'runAbaqus.py') 
    for j in range(len(modelData.confiningStress)):
        open(os.path.join('OSTRICH', 'fittedHistory', '{0}({1}.{2})_{3}_fittedHistory.pkl'.format(modelData.modelName, parameterizationRun-1, j, modelData.abaqusMaterial)), 'w').close()
    
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='runAbaqusModel: Creates the Neccessary Input files to Run Abaqus model')
    parser.add_argument('-f', '--fitted-model', required=True, help='Name of the model that has been fitted to DEM data')
    parser.add_argument('-n', '--new-model', required=True, help='Name of the model to run with -f parameters')
    parser.add_argument('-r', '--run', required=True, type=int, help='Parameterization run number')

    args = parser.parse_args()
    fittedName = args.fitted_model
    modelName = args.new_model
    parameterizationRun = args.run
    
    importModelData(modelName)
    importMaterialData(modelData.abaqusMaterial)
    main(parameterizationRun, fittedName)
 
  

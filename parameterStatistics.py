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

def getModelConstants(parameterizationRun, fileName):
    parameters = {}

    for i in range(parameterizationRun):
         with open(os.path.join('OSTRICH', 'ostOutput', fileName)) as ostOutputFile:
            ostOutput = ostOutputFile.read()
            startIndex = ostOutput.find('Optimal Parameter Set')
            endIndex = ostOutput.find('\n\n', startIndex)
            parameterBlock = ostOutput[startIndex:endIndex+1]
            for parameter in list(material.ostrichParameters.keys())+['Objective Function']:
                paramPosition = parameterBlock.find(parameter)
                colonPosition = parameterBlock.find(':', paramPosition)
                eolPosition = parameterBlock.find('\n', paramPosition)
                value = float(parameterBlock[colonPosition+1:eolPosition])
                parameters[parameter] = value
    return parameters
    
def getAverageValues(optimalParameters):
    params = optimalParameters[0].keys()
    averages = {}
    for parameter in params:
        allValues = [x[parameter] for x in optimalParameters]
        averages[parameter] = statistics.mean(allValues)
    return averages
        
def getVariances(optimalParameters):
    params = optimalParameters[0].keys()
    variances = {}
    for parameter in params:
        allValues = [x[parameter] for x in optimalParameters]
        variances[parameter] = statistics.variance(allValues)
    return variances
        
def getStandardDeviations(optimalParameters):
    params = optimalParameters[0].keys()
    stdevs = {}
    for parameter in params:
        allValues = [x[parameter] for x in optimalParameters]
        stdevs[parameter] = statistics.stdev(allValues)
    return stdevs
        
def getMaximum(optimalParameters):
    params = optimalParameters[0].keys()
    m = {}
    for parameter in params:
        allValues = [x[parameter] for x in optimalParameters]
        m[parameter] = max(allValues)
    return m
             
def getMinimum(optimalParameters):
    params = optimalParameters[0].keys()
    m = {}
    for parameter in params:
        allValues = [x[parameter] for x in optimalParameters]
        m[parameter] = min(allValues)
    return m
        
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
    allFiles = os.listdir(os.path.join('OSTRICH', 'ostOutput'))
    optimalParameters  = []
    for i in range(len(allFiles)):
        fileName ='OstOutput_{0}_{1}_{2}_{3}_id-{4}.txt'.format(modelData.modelName, modelData.abaqusMaterial, parameterizationRun, optimizer, i+1)
        if fileName in allFiles:
            print('hello')
            optimalParameters.append(getModelConstants(parameterizationRun, fileName))
    av = getAverageValues(optimalParameters)
    std = getStandardDeviations(optimalParameters)
    maximum = getMaximum(optimalParameters)
    minimum = getMinimum(optimalParameters)
    
    print('*'*70)
    print ('Parameter Estimation Statistics')
    print('*'*70)
    for parameter in av:
        print (parameter)
        print('\tMean: \t\t\t{0}'.format(av[parameter]))
        print('\tStandard Deviation: \t{0}'.format(std[parameter]))
        print('\tMax: \t\t\t{0}'.format(maximum[parameter]))
        print('\tMin: \t\t\t{0}'.format(minimum[parameter]))
    
    
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
 
  

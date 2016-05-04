#!/usr/bin/env python3

import sys
import os
import csv
from OSTRICH.vectorMath import *
import math

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
        
def getModelParameters(modelNumber, endTime, numObservations):
    #TODO: cleanup, make more general, maybe move to material definitions since not consistant
    # print(math.floor((numObservations)*(endTime/sTime[modelNumber])))
    # print((numObservations)*(endTime/sTime[modelNumber]))
    # print(numObservations)
    # print(endTime)
    # print(sTime[modelNumber])
    
    parameters =  {'$$mSize': mSize,
                            '$$mName': '\''+modelName+'\'',
                            '$$sName': '\''+fileName+'\'',
                            '$$nObs': numObservations,
                            '$$rho': rho*1e9,
                            '$$dAngle': jDilation,
                            '$$confStress': confiningStress[0]*1e6, #***********************************************************fix for different confining stresses!!!!!
                            '$$cStrain': getInelasticStrain(), #fix for concrete plasticity
                            '$$iStrain': getInelasticStrain(),
                            '$$vel':vel[modelNumber],
                            '$$sTime':endTime,
                            '$$vString':getVelocityString(velTable[modelNumber])}
    # if '(c)' in modelName:
        # parameters .update({ '$$maxTS':maxTensileStrainIO('r'),
                                # '$$sTime':sTime_c,
                                # '$$vel':vel_c,
                                # '$$vString':getVelocityString(velTable_c) })
    # elif '(t)' in modelName:
        # parameters.update({ '$$maxTS':maxTensileStrainIO('w'),
                                # '$$sTime':sTime_t,
                                # '$$vel':vel_t,
                                # '$$vString':getVelocityString(velTable_t) })
    return parameters
                                
def getOstrichParameters(parameterizationRun):
    ostrichParametersText = '' 
    for parameter in ostrichParameters:
        if '$' + parameter in materialParameters[parameterizationRun-1]:
            p = ostrichParameters[parameter]
            newRecord = '$' + parameter + '\t' + str(p['init']) + '\t' + str(p['low']) + '\t' +str(p['high']) +'\tnone\tnone\tnone\n'
            ostrichParametersText += newRecord
    return {'$$ostrichParameters':ostrichParametersText}
    
# def getOstInVoid(parameterizationRun):
    # parameters = {}
    # for parameter in materialParameters[parameterizationRun-1]:
        # parameters[parameter] = '#'+parameter
    # return parameters
    
def getModelConstants(modelName, parameterizationRun):
    parameters = {}
    for parameter in ostrichParameters:
        parameters['$'+parameter] = ostrichParameters[parameter]['init']
    for parameter in materialParameters[parameterizationRun-1]:
        parameters[parameter] = parameter
    for i in range(parameterizationRun-1):
         with open(os.path.join('OSTRICH', 'ostOutput', 'OstOutput_{0}_{1}.txt'.format(modelName, i+1))) as ostOutputFile:
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
            
# def main():
    #use argparse
               
            
if __name__ == '__main__':
    # main()
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
        parameterizationRun = int(clargs[2])
        numObservations = int(clargs[3])
        dt = float(clargs[4])
     #else: error message
    modelName = fileName[:fileName.find('(')]
    module = __import__('UDEC.modelData.'+modelName+'_modelData', globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)
    module = __import__('OSTRICH.materials.'+abaqusMaterial, globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)
        
    counter = 0
    for i in range(len(parameterizationSplits)):
        for j in range(len(parameterizationSplits[i])+1):
            counter += 1
            if counter == parameterizationRun:
                modelNumber = i
                # if j < len(parameterizationSplits[i]):
                    # endTime = parameterizationSplits[i][j]
                # else:
                    # endTime = sTime
    
    
    endTime = dt*numObservations
    fillTemplate('parameters.tpl', getModelParameters(modelNumber, endTime, numObservations), 'parameters.py')
    fillTemplate('ostIn.tpl', getOstrichParameters(parameterizationRun), 'ostIn.txt')
    # fillTemplate('ostIn.txt', getOstInVoid(), 'ostIn.txt')
    fillTemplate('runAbaqus.tpl', getModelConstants(modelName, parameterizationRun), 'runAbaqus.temp.tpl')
        
        
        
        
        
        
        
        
        

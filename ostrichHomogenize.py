import os
import sys
import pickle
from HOMOGENIZE import Homogenize
from numpy import interp
import numpy
import math
import argparse
import importlib

def writeToFile(timeHistory, stressHistory, strainHistory, cStressIndex, parameterizationRun, interpolate=True):
    print('Saving homogenization time history:')
    fileName = '{0}({1}.{2})'.format(modelData.modelName, parameterizationRun, cStressIndex)
    with open(os.path.join('HOMOGENIZE', 'textData', fileName+'_homogenizedData.dat'), 'w') as f:
        f.write('time S11 S22 S12 LE11 LE22 LE12\n')
        #converting data correspond to an expected S22 strain step in order to compare against FEM better
        prescribedStrainHistory = prescribedStrain(modelData.modelSize, modelData.velocityTable[parameterizationRun], -modelData.velocity[parameterizationRun], timeHistory)
        S11History = [x[0,0] for x in stressHistory]
        S22History = [x[1,1] for x in stressHistory]
        S12History = [x[0,1] for x in stressHistory]
        LE11History = [x[0,0] for x in strainHistory]
        LE22History = [x[1,1] for x in strainHistory]
        LE12History = [x[0,1] for x in strainHistory]

        if interpolate:
            S22History = interpolateData(S22History, LE22History, prescribedStrainHistory, timeHistory, parameterizationRun)
            S11History = interpolateData(S11History, LE22History, prescribedStrainHistory, timeHistory, parameterizationRun)
            S12History = interpolateData(S12History, LE22History, prescribedStrainHistory, timeHistory, parameterizationRun)
            LE11History = interpolateData(LE11History, LE22History, prescribedStrainHistory, timeHistory, parameterizationRun)
            LE22History = prescribedStrainHistory
            LE12History = interpolateData(LE12History, LE22History, prescribedStrainHistory, timeHistory, parameterizationRun)
        #stressHistory = [numpy.array([[-modelData.confiningStress[cStressIndex], 0],[0, 0]] )]+stressHistory 
        #strainHistory = [numpy.array([[0,0],[0,0]])]+strainHistory
        for i in range(len(stressHistory)):
            LE11 = LE11History[i]                 
            LE22 = LE22History[i]
            LE12 = LE12History[i]
            S11 = S11History[i]
            S22 = S22History[i]
            S12 = S12History[i]
            stressHistory[i][0,0] = S11
            stressHistory[i][1,1] = S22
            stressHistory[i][1,0] = S12
            stressHistory[i][0,1] = S12
            strainHistory[i][0,0] = LE11
            strainHistory[i][1,1] = LE22
            strainHistory[i][1,0] = LE12
            strainHistory[i][0,1] = LE12

            time = timeHistory[i]
            record = [time, S11, S22, S12, LE11, LE22, LE12]
            record = ' '.join(map(str, record))
            f.write(record + '\n')

    bundle = [timeHistory, stressHistory, strainHistory]
    with open(os.path.join('HOMOGENIZE', 'binaryData', fileName+'_homogenizedData.pkl'), 'wb') as bundleFile:
        pickle.dump(bundle, bundleFile)
    print('\tDone')

def interpolateData(rawStressData, rawStrainData, prescribedStrainData, prescribedTimeData, parameterizationRun):
    newStressData = numpy.array([])
    startStrainIndex = 0
    for i in range(len(modelData.velocityTable[parameterizationRun])):
        endStrain = interp(modelData.velocityTable[parameterizationRun][i], prescribedTimeData, prescribedStrainData)
        endStrainIndex = len(prescribedStrainData) - prescribedStrainData[::-1].index(endStrain) - 1
        sectionStrains = prescribedStrainData[startStrainIndex: endStrainIndex+1]
        
        positiveSectionStrainData= [x*-1 for x in sectionStrains]
        positiveRawStrainData = [x*-1 for x in rawStrainData]

        newStressData = numpy.append(newStressData, interp(positiveSectionStrainData, positiveRawStrainData, rawStressData, right=numpy.NaN))
        startStrainIndex = endStrainIndex
    return newStressData
    
# def interpolateStress(rawStressData, rawStrainData, prescribedStrainData, prescribedTimeData, test=0):
    # newStressData = []
    # startStrainIndex = 0
    # for i in range(len(modelData.velocityTable)):
        # endStrain = interp(modelData.velocityTable[i], prescribedTimeData, prescribedStrainData)
        # endStrainIndex = len(prescribedStrainData) - prescribedStrainData[::-1].index(endStrain) - 1
        # sectionStrains = prescribedStrainData[startStrainIndex: endStrainIndex+1]
        # positiveSectionStrains = [x*-1 for x in sectionStrains]
        # positiveRawStrainData = [x*-1 for x in rawStrainData]
        # newStressData = interp(positiveSectionStrains, positiveRawStrainData, rawStressData, right=numpy.NaN)
    # return newStressData
                
def prescribedStrain(originalLength, velTable, velocity, timeHistory):


    strainHistory = []
    accelTime = velTable[-1]/10
    amp = velocity
    velocityTimes = [0]
    velocityTable = [amp]
    for i in range(len(velTable)):
        velocityTimes.append((velTable[i]-accelTime))
        velocityTimes.append((velTable[i]+accelTime))
        velocityTable.append(amp)
        velocityTable.append(amp*-1)
        amp = amp*-1
    velocityTimes.append((velTable[-1]))
    velocityTable.append(amp)

    startIndex = 0
    endIndex = 0
    strainHistory = []
    currentLength = originalLength
    timeHistory = [0] + timeHistory
    for i in range(1, len(timeHistory)):
        velocity = interp(timeHistory[i], velocityTimes, velocityTable)
        currentLength = currentLength + velocity*(timeHistory[i]-timeHistory[i-1])
        strain22 = math.log(currentLength/originalLength)
        strainHistory.append(strain22)
    return strainHistory
    
            
def main(revCentreX=None, revCentreY=None, revRadius=None, interpolate=True):
    os.system('cls')

    if revCentreX == None:
        revCentreX = modelData.modelSize/2
    if revCentreY == None:
        revCentreY = modelData.modelSize/2
    if revRadius == None:
        revRadius = modelData.modelSize/2-modelData.blockSize*2
    revCentre = {'x':revCentreX, 'y':revCentreY}

    for i in range(len(modelData.simulationTime)):
        for j in range(len(modelData.confiningStress)):
            f = '{0}({1}.{2})'.format(modelData.modelName, i, j)
            H = Homogenize.Homogenize(revCentre, revRadius, fileName=f)
            stressHistory = H.stress()
            strainHistory = H.strain()
            timeHistory = H.time()
            
            writeToFile(timeHistory, stressHistory, strainHistory, j, i, interpolate=interpolate)
            print (' ')
            
    # main()
    
def importModelData(modelName):
    global modelData
    modelData = importlib.import_module('UDEC.modelData.'+modelName)
    
    
def run(modelName, revCentreX=None, revCentreY=None, revRadius=None, interpolate=True):
    importModelData(modelName)
    main(revCentreX, revCentreY, revRadius, interpolate=interpolate)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ostrichHomogenize: Homogenizes the specified DEM data')
    parser.add_argument('-n', '--name', required=True ,help='Name of the file containing the model data without the extension')
    parser.add_argument('-x', '--revX', type=float ,help='x coordinate of REV centre')
    parser.add_argument('-y', '--revY', type=float ,help='y coordinate of REV centre')
    parser.add_argument('-r', '--revRadius', type=float ,help='Radius of REV centre')
    parser.add_argument('-i', '--interpolate', dest='interpolate', help='Interpolate Stress and strain data', action='store_true')
    parser.add_argument('-ni', '--no-interpolate', dest='interpolate', help='Dont interpolate Stress and strain data', action='store_false')
    parser.set_defaults(interpolate=False)

    args = parser.parse_args()
    modelName = args.name
    revCentreX = args.revX
    revCentreY = args.revY
    revRadius = args.revRadius
    interpolate = args.interpolate
    
    importModelData(modelName)
    main(revCentreX, revCentreY, revRadius, interpolate=interpolate)

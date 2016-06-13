import os
import sys
import pickle
from HOMOGENIZE import Homogenize
from numpy import interp
import math
import argparse
import importlib

def writeToFile(timeHistory, stressHistory, strainHistory, fileName, parameterizationRun):
    print('Saving homogenization time history:')
    with open(os.path.join('HOMOGENIZE', 'textData', fileName+'_homogenizedData.dat'), 'w') as f:
        f.write('time S11 S22 S12 LE11 LE22 LE12\n')
        f.write('0.0 '+str(modelData.confiningStress[parameterizationRun]*1e6)+' 0.0 0.0 0.0 0.0 0.0\n') 
        #f.write('0.0 0.0 '+str(stressHistory[0][1,1])+' 0.0 0.0 0.0 0.0\n') #fix this line
        
        prescribedStrainHistory = prescribedStrain(modelData.modelSize, modelData.velocityTable[parameterizationRun], -modelData.velocity[parameterizationRun], timeHistory)
        for i in range(len(stressHistory)):
            S11 = stressHistory[i][0,0]
            S22 = stressHistory[i][1,1]
            S12 = stressHistory[i][0,1]
            LE11 = strainHistory[i][0,0]                  
            #Assuming displacement controlled boundary conditions in the 22 direction
            strainHistory[i][1,1] = prescribedStrainHistory[i]
            LE22 = strainHistory[i][1,1]
            LE12 = strainHistory[i][0,1]
            time = timeHistory[i]
            record = [time, S11, S22, S12, LE11, LE22, LE12]
            record = ' '.join(map(str, record))
            f.write(record + '\n')

    bundle = [timeHistory, stressHistory, strainHistory]
    with open(os.path.join('HOMOGENIZE', 'binaryData', fileName+'_homogenizedData.pkl'), 'wb') as bundleFile:
        pickle.dump(bundle, bundleFile)
    print('\tDone')
    
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
    
            
def main():
    os.system('cls')
    
    revCentre = {'x':modelData.modelSize/2, 'y':modelData.modelSize/2}
    revRadius = modelData.modelSize/2-modelData.blockSize*2

    for i in range(len(modelData.simulationTime)):
        for j in range(len(modelData.confiningStress)):
            f = '{0}({1}.{2})'.format(modelData.modelName, i, modelData.confiningStress[j])
            H = Homogenize.Homogenize(revCentre, revRadius, fileName=f)
            stressHistory = H.stress()
            strainHistory = H.strain()
            timeHistory = H.time()
            
            writeToFile(timeHistory, stressHistory, strainHistory, f, i)
            print (' ')
            
    # main()
    
def importModelData(modelName):
    global modelData
    modelData = importlib.import_module('UDEC.modelData.'+modelName)
    
    
def run(modelName):
    importModelData(modelName)
    main()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ostrichHomogenize: Homogenizes the specified DEM data')
    parser.add_argument('-n', '--name', required=True ,help='Name of the file containing the model data without the extension')

    args = parser.parse_args()
    modelName = args.name
    
    importModelData(modelName)
    main()

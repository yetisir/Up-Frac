import os
import sys
import pickle
from HOMOGENIZE import Homogenize
from numpy import interp
import math

def writeToFile(timeHistory, stressHistory, strainHistory, fileName, modelNo):
    print('Saving homogenization time history:')
    with open(os.path.join('HOMOGENIZE', 'textData', fileName+'_homogenizedData.dat'), 'w') as f:
        f.write('time S11 S22 S12 LE11 LE22 LE12\n')
        # f.write('0.0 '+str(confiningStress*1e6)+' '+str(stressHistory[0][1,1])+' 0.0 0.0 0.0 0.0\n') 
        f.write('0.0 0.0 '+str(stressHistory[0][1,1])+' 0.0 0.0 0.0 0.0\n') #fix this line
        
        prescribedStrainHistory = prescribedStrain(mSize, velTable[modelNo], timeHistory)
        for i in range(len(stressHistory)):
            S11 = stressHistory[i][0,0]
            S22 = stressHistory[i][1,1]
            S12 = stressHistory[i][0,1]
            LE11 = strainHistory[i][0,0]                  
            #Assuming displacement controlled boundary conditions in the 22 direction
            LE22 = prescribedStrainHistory[i]
            # LE22 = strainHistory[i][1,1]
            LE12 = strainHistory[i][0,1]
            time = timeHistory[i]
            record = [time, S11, S22, S12, LE11, LE22, LE12]
            record = ' '.join(map(str, record))
            f.write(record + '\n')

    bundle = [timeHistory, stressHistory, strainHistory]
    with open(os.path.join('HOMOGENIZE', 'binaryData', fileName+'_homogenizedData.pkl'), 'wb') as bundleFile:
        pickle.dump(bundle, bundleFile)
    print('\tDone')
    
def prescribedStrain(originalLength, velTable, timeHistory):
    strainHistory = []
    accelTime = velTable[-1]/10
    amp = -1
    velocityTimes = []
    velocityTable = []
    for i in range(len(velTable)-1):
        velocityTimes.append((velTable[i]-accelTime))
        velocityTimes.append((velTable[i]+accelTime))
        velocityTable.append(amp)
        velocityTable.append(amp*-1)
        amp = amp*-1
    velocityTimes.append((velTable[i]+accelTime))
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
    
            
# def main():
if __name__ == '__main__':
    os.system('cls')
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
    #else: error message
    #add other cl args for centre and radius
    module = __import__('UDEC.modelData.'+fileName[0:]+'_modelData', globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)
        
    revCentre = {'x':mSize/2, 'y':mSize/2}
    revRadius = mSize/2-bSize*2

    for i in range(len(sTime)):
        for j in range(len(confiningStress)):
            f = '{0}({1}.{2})'.format(mName, i, confiningStress[j])
            H = Homogenize.Homogenize(revCentre, revRadius, fileName=f)
            stressHistory = H.stress()
            strainHistory = H.strain()
            timeHistory = H.time()
            
            writeToFile(timeHistory, stressHistory, strainHistory, f, i)
            print (' ')
            
    # main()

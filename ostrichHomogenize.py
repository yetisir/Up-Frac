import os
import sys
import pickle
from HOMOGENIZE import Homogenize

def writeToFile(timeHistory, stressHistory, strainHistory, fileName):
    print('Saving homogenization time history:')
    with open(os.path.join('ostrich', 'observationUDEC.dat'), 'w') as f:
        f.write('time S11 S22 S12 LE11 LE22 LE12\n')
        f.write('0.0 '+str(confiningStress*1e6)+' '+str(stressHistory[0][1,1])+' 0.0 0.0 0.0 0.0\n')
        for i in range(len(stressHistory)):
            S11 = stressHistory[i][0,0]
            S22 = stressHistory[i][1,1]
            S12 = stressHistory[i][0,1]
            LE11 = strainHistory[i][0,0]
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
            
def main():
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
            
            writeToFile(timeHistory, stressHistory, strainHistory, f)
            
if __name__ == '__main__':
    main()
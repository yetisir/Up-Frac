import os
import sys
from Homogenize import Homogenize

def writeToFile(timeHistory, stressHistory, strainHistory):
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
    print('\tDone')

def createOstIn(H, parameters):
    print('Creating OstIn.txt for OSTRICH:')
    #TODO: change import format, use template, not module maybe?
    import ostrich.ostIn
    observations = ''
    numObservations = len(H.timeHistory)
    for i in range(numObservations):
        for j in range(len(parameters)):
            if parameters[j] == 'S11':
                o = H.stressHistory[i][0, 0]
                c = 2
            elif parameters[j] == 'S22':
                o = H.stressHistory[i][1, 1]
                c = 3
            elif parameters[j] == 'S12':
                o = H.stressHistory[i][0, 1]
                c = 4
            elif parameters[j] == 'LE11':
                o = H.strainHistory[i][0, 0]
                c = 5
            elif parameters[j] == 'LE22':
                o = H.strainHistory[i][1, 1]
                c = 6
            elif parameters[j] == 'LE12':
                o = H.strainHistory[i][0, 1]
                c = 7
            l = i+2
            obsNo = i*len(parameters)+j+1
            newObservation = 'obs{} \t\t{:10f} \t1 \toutput.dat \tOST_NULL \t{} \t\t{}\n'.format(obsNo, o, l, c)
            observations += newObservation
    with open(os.path.join('ostrich', 'OstIn.txt'), 'w') as f:
        f.write(ostrich.ostIn.topText+observations+ostrich.ostIn.bottomText)
    print('\tDone')
            
if __name__ == '__main__':
    os.system('cls')
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
    #else: error message
    #add other cl args for centre and radius
    module = __import__('UDEC.modelData.'+fileName[0:-3]+'_modelData', globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)
    revCentre = {'x':mSize/2, 'y':mSize/2}
    revRadius = mSize/2-bSize*2
    
    H = Homogenize(revCentre, revRadius, fileName=fileName)


    stressHistory = H.stress()
    strainHistory = H.strain()
    timeHistory = H.time()
    writeToFile(timeHistory, stressHistory, strainHistory)
    createOstIn(H, relVars)

    #following command should be moved to up-scaling script
    os.system('python createParameters.py ' + fileName)


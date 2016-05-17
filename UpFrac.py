#copy modelData modules from UDEC to HOMOGENIZE
import os
import sys
import pickle
import shutil
import time
import psutil

def createOstIn(fileName, parameters, startTime, endTime):
    #TODO: change import format, use template, not module maybe?
    import OSTRICH.ostIn
    observations = ''
    startIndex = 0
    endIndex = 0
    for k in range(len(confiningStress)):
        with open(os.path.join('HOMOGENIZE', 'binaryData', fileName+str(confiningStress[k])+')_homogenizedData.pkl'), 'rb') as bundleFile:
            bundle = pickle.load(bundleFile)
            timeHistory = bundle[0]
            stressHistory = bundle[1]
            strainHistory = bundle[2]

        for i in range(len(timeHistory)):
            if timeHistory[i] <= startTime:
                startIndex = i +1
            if timeHistory[i] <= endTime:
                endIndex = i
        th = timeHistory
        timeHistory = timeHistory[startIndex:endIndex+1]
        stressHistory = stressHistory[startIndex:endIndex+1]
        strainHistory = strainHistory[startIndex:endIndex+1]
        numObservations = len(timeHistory) + 1
    #TODO: add weightings so strain and stress can be used together
        for i in range(1, numObservations):
            for j in range(len(parameters)):
                if parameters[j] == 'S11':
                    o = stressHistory[i-1][0, 0]
                    c = 2
                elif parameters[j] == 'S22':
                    o = stressHistory[i-1][1, 1]
                    c = 3
                elif parameters[j] == 'S12':
                    o = stressHistory[i-1][0, 1]
                    c = 4
                elif parameters[j] == 'LE11':
                    o = strainHistory[i-1][0, 0]
                    c = 5
                elif parameters[j] == 'LE22':
                    o = strainHistory[i-1][1, 1]
                    c = 6
                elif parameters[j] == 'LE12':
                    o = strainHistory[i-1][0, 1]
                    c = 7
                l = k*(numObservations+startIndex) + i + 1 + startIndex
                obsNo = k*(numObservations-1)*len(parameters) + (i-1)*len(parameters) + (j +1)
                newObservation = 'obs{} \t\t{:10f} \t1 \toutput.dat \tOST_NULL \t{} \t\t{}\n'.format(obsNo, o, l, c)
                observations += newObservation
    with open(os.path.join('OSTRICH', 'OstIn.tpl'), 'w') as f:
        f.write(OSTRICH.ostIn.topText+observations+OSTRICH.ostIn.bottomText)
    dt = timeHistory[1]-timeHistory[0]
    return [len(th[0:endIndex+1] ), dt]#this is soooooooo wrong , fix ASAP. should be retruned from a seperate function


# def main():


if __name__ == '__main__':
    MPI = True
    os.system('cls')
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
        
    module = __import__('UDEC.modelData.'+fileName[0:]+'_modelData', globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)

    # os.system('python ostrichHomogenize.py' + fileName)
    parameterizationRun = 1
    for i in range(len(parameterizationSplits)):
        startTime = 0
        splitTimes = parameterizationSplits[i] + [sTime[i]]
        for j in range(len(splitTimes)):  
            homoFileName = '{0}({1}.'.format(mName, i, 0)
            endTime = splitTimes[j]
            print('*'*70)
            print('OSTRICH file setup for {0} set {1}'.format(fileName, parameterizationRun))
            print('*'*70)
            print('Creating OstIn.txt template...'.format(fileName, parameterizationRun))
            numObs, dt = createOstIn(homoFileName, relVars, startTime, endTime) #please fix, this fucntion should not return this value
            print('\tDone')
            print('Filling in model templates...')
            os.system('python createOstrichInput.py ' + mName + '  ' + str(parameterizationRun) + ' ' + str(numObs)+' '+str(dt))
            print('\tDone')
            os.chdir(os.path.join(os.getcwd(), 'OSTRICH'))
            print('Cleaning up OSTRICH mess from previous run...')
            os.system('cleanup.bat')
            print('\tDone')
            print('Initializing OSTRICH...' )
            print('\tDone')
            if MPI:
                print('Running OSTRICH MPI...\n\t', end='')
                os.system('mpirun.bat >NUL')
                while 1:
                    try:
                        with open('OstStatus0.txt', 'r') as file:
                            lines = file.readlines()
                            comp = int(float(lines[2][18:-1]))
                            numString = '{0}%'.format(comp)
                            print(numString, end='')
                            print('\b'*len(numString), end='')
                            sys.stdout.flush()
                            if comp == 100:
                                print('100%')
                                print('Computing parameter statistics...')
                                while 1:
                                    runningProcesses = psutil.pids()
                                    br = True
                                    for k in runningProcesses:
                                        try:
                                            if psutil.Process(k).name() == 'OstrichMPI.exe':
                                                br = False
                                        except:
                                            pass
                                    if br:
                                        break
                                print('\tDone')        
                                print('Shutting Down OSTRICH...\n\t', end='')
                                sleepTime = 10
                                for k in range(sleepTime):
                                    time.sleep(1)
                                    numString = '{0}%'.format(int(k/sleepTime*100))
                                    print(numString, end='')
                                    print('\b'*len(numString), end='')
                                    sys.stdout.flush()
                                print('100%')
                                break
                    except (FileNotFoundError, IndexError, PermissionError):
                        pass
                    time.sleep(1)
            else:
                print('Running Serial OSTRICH')
                os.system('ostrich.exe')
                print('\tDone')
                print('Shutting Down OSTRICH...')
                print('\Done')
            os.chdir(os.pardir)
            
            print('Saving estimated parameter set')
            shutil.copy(os.path.join('OSTRICH', 'OstOutput0.txt'), os.path.join('OSTRICH', 'ostOutput', 'OstOutput_{0}_{1}.txt'.format(fileName, parameterizationRun)))
            print('\tDone\n')
          
            parameterizationRun +=1
            startTime = endTime
    os.chdir(os.path.join(os.getcwd(), 'OSTRICH'))
    # os.system('cleanup.bat')
    os.chdir(os.pardir)
    

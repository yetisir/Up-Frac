#copy modelData modules from UDEC to HOMOGENIZE
import os
import sys
import pickle
import shutil

def createOstIn(fileName, parameters, startTime, endTime):
    print('Creating OstIn.txt for OSTRICH:')
    with open(os.path.join('HOMOGENIZE', 'binaryData', fileName+'_homogenizedData.pkl'), 'wb') as bundleFile:
        pickle.dump(bundle, bundleFile)
        bundle = pickle.load()
        timeHistory = bundle[0]
        stressHistory = bundle[1]
        strainHistory = bundle[2]
    #TODO: change import format, use template, not module maybe?
    import OSTRICH.ostIn
    observations = ''
    startIndex = 0
    endIndex = 0
    for i in range(len(timeHistory)):
        if timeHistory[i] <= startTime:
            startIndex i
        if timeHistory[i] <= endTime:
            endIndex = i
    timeHistory = timeHistory[startIndex:endIndex]
    stressHistory = stressHistory[startIndex:endIndex]
    strainHistory = strainHistory[startIndex:endIndex]
    numObservations = len(timeHistory)
    
    #TODO: add weightings so strain and stress can be used together
    for i in range(numObservations):
        for j in range(len(parameters)):
            if parameters[j] == 'S11':
                o = stressHistory[i][0, 0]
                c = 2
            elif parameters[j] == 'S22':
                o = stressHistory[i][1, 1]
                c = 3
            elif parameters[j] == 'S12':
                o = stressHistory[i][0, 1]
                c = 4
            elif parameters[j] == 'LE11':
                o = strainHistory[i][0, 0]
                c = 5
            elif parameters[j] == 'LE22':
                o = strainHistory[i][1, 1]
                c = 6
            elif parameters[j] == 'LE12':
                o = strainHistory[i][0, 1]
                c = 7
            l = i+2
            obsNo = i*len(parameters)+j+1
            newObservation = 'obs{} \t\t{:10f} \t1 \toutput.dat \tOST_NULL \t{} \t\t{}\n'.format(obsNo, o, l, c)
            observations += newObservation
    with open(os.path.join('OSTRICH', 'OstIn.tpl'), 'w') as f:
        f.write(OSTRICH.ostIn.topText+observations+OSTRICH.ostIn.bottomText)
    print('\tDone')



def main():
    os.system('cls')
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
        
    module = __import__('UDEC.modelData.'+fileName[0:]+'_modelData', globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)

    os.system('python ostrichHomogenize.py' + fileName)
    parameterizationRun = 1
    for i in range(len(parameterizationSplits)):
        startTime = 0
        for j in range(len(parameterizationSplits[i])+1):  
            homoFileName = '{0}({1}.{2})'.format(mName, i, confiningStress[j])
            if len(parameterizationSplits[i]) > j:
                endTime = parameterizationSplits[i][j+1]
            else:
                endTime = parameterizationSplits[i][-1]
            createOstIn(homoFileName, relVars, startTime, endTime)
            os.system('python createOstrichInput.py ' + homoFileName + '  ' + parameterizationRun)
            os.system('OSTRICH\ostrich.exe')

def copy_rename(old_file_name, new_file_name):
        src_dir= os.curdir
        dst_dir= os.path.join(os.curdir , "subfolder")
        src_file = os.path.join(src_dir, old_file_name)
        shutil.copy(src_file,dst_dir)
        
        dst_file = os.path.join(dst_dir, old_file_name)
        new_dst_file_name = os.path.join(dst_dir, new_file_name)
        os.rename(dst_file, new_dst_file_name)
            parameterizationRun +=1
            startTime = endTime




if __name__ == '__main__':
    main()
    

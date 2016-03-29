import sys
import os
import csv
from OSTRICH.vectorMath import *


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
    
def getCrackingStrain(numStrainPoints = 100):
    if '(t)' in modelName:
        crackingStrain = divide(range(0, numStrainPoints+1), numStrainPoints/getMaxStrain())
    elif '(c)' in modelName:
        crackingStrain = divide(range(0, numStrainPoints+1), numStrainPoints/maxTensileStrainIO('r'))
    return crackingStrain
    
def getInelasticStrain(numStrainPoints = 100):
    inelasticStrain = divide(range(0, numStrainPoints+1), numStrainPoints/getMaxStrain())

                                
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
        
def getModelParameters():
    parameters =  {'$$mSize': mSize,
                            '$$mName': '\''+modelName+'\'',
                            '$$rho': rho*1e9,
                            '$$dAngle': jDilation,
                            '$$confStress': confiningStress*1e6,
                            '$$maxStrain': getMaxStrain(),
                            '$$cStrain': getCrackingStrain(),
                            '$$iStrain': getCrackingStrain()}
    if '(c)' in modelName:
        parameters .update({ '$$maxTS':maxTensileStrainIO('r'),
                                '$$sTime':sTime_c,
                                '$$vel':vel_c,
                                '$$vString':getVelocityString(velTable_c) })
    elif '(t)' in modelName:
        parameters.update({ '$$maxTS':maxTensileStrainIO('w'),
                                '$$sTime':sTime_t,
                                '$$vel':vel_t,
                                '$$vString':getVelocityString(velTable_t) })
    return parameters
                                
def getOstrichParameters():
    return {'$$ostrichParameters':ostrichParameters}
    
def getLoadingParameters():
    if '(c)' in modelName:
        parameters =  {'$elasticModulus': '#elasticModulus',
                                '$poissonsRatio': '#poissonsRatio',
                                '$initialTensileYeild': '#initialTensileYeild',
                                '$tLambda': '#tLambda',
                                '$tensileDamageScaling': '#tensileDamageScaling'}

    elif '(t)' in modelName:
        parameters =  {'$PeakYeildStrain': '#PeakYeildStrain',
                                '$PeakYeildStress': '#PeakYeildStress',
                                '$InitialcompressiveYeild': '#InitialcompressiveYeild',
                                '$compressiveDamageScaling': '#compressiveDamageScaling'}
    return parameters
     
def fillTemplate(template, parameters, file):
    
    with open(os.path.join('OSTRICH', template), 'r') as templateFile:
        t = templateFile.read()
        for i in parameters.keys():
            t = t.replace(i, str(parameters[i]))
        with open(os.path.join('OSTRICH', file), 'w') as modelFile:
            modelFile.write(t)
            
            
if __name__ == '__main__':
    clargs = sys.argv
    if len(clargs) >= 2:
        modelName = clargs[1]
    #else: error message
    module = __import__('UDEC.modelData.'+modelName[0:-3]+'_modelData', globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)


    fillTemplate('parameters.tpl', getModelParameters(), 'parameters.py')
    fillTemplate('ostIn.tpl', getOstrichParameters(), 'ostIn.txt')
    fillTemplate('ostIn.txt', getLoadingParameters(), 'ostIn.txt')
      
        
        
        
        
        
        
        
        
        

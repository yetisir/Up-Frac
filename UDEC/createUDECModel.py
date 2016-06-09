import sys, os

clargs = sys.argv
if len(clargs) >= 2:
    modelName = clargs[1]
#else: error message
module = __import__('modelData.'+modelName+'_modelData', globals(), locals(), ['*'])
for k in dir(module):
    locals()[k] = getattr(module, k)
#from modelData.test_modelData import *
accelTime = []
vString = []
for i in range(len(sTime)):
    accelTime.append(velTable[i][-1]/10)
    amp = -1
    vString.append('0 {0} '.format(amp))
    for j in range(len(velTable[i])-1):
        vString[i] += '{0} {1} {2} {3} '.format(velTable[i][j]-accelTime[i], amp, velTable[i][j]+accelTime[i], amp*-1)
        amp = amp*-1
    vString[i] += '{0} {1}'.format(velTable[i][-1], amp)


rangeOffset = bSize/1000
bRange = '{0},{1} {0},{2}'.format(-rangeOffset, mSize+rangeOffset, rangeOffset)
tRange = '{0},{1} {2},{1}'.format(-rangeOffset, mSize+rangeOffset, mSize-rangeOffset)
lRange = '{0},{1} {0},{2}'.format(-rangeOffset, rangeOffset, mSize+rangeOffset)
rRange = '{0},{1} {2},{1}'.format(mSize-rangeOffset, mSize+rangeOffset, -rangeOffset)
UDECParameters = {
    '$nSteps': nSteps, #depending on the number of contacts, the memory is exceeded with too many steps. future iteration of cycleModel.fis shall write to file after each step rather than after all steps to reduce the memory load. 
    '$mSize': mSize,
    '$bSize': bSize,
    '$meshSize': meshSize,
    '$round': float(bSize)/100,
    '$edge': float(bSize)/20,
    '$vSeed': 1,
    '$rho': rho,
    '$bulk': E/(3*(1-2*nu)),
    '$shear': E/(2*(1+nu)),
    '$jks': jks,
    '$jkn': jkn,
    '$jFriction': jFriction,
    '$jCohesion': jCohesion,
    '$jTension': jTension,
    '$jDilation': jDilation,
    '$bRange': bRange,
    '$tRange': tRange,
    '$lRange': lRange,
    '$rRange': rRange}


fileNames = []
for i in range(len(sTime)):
    UDECParameters['$sTime'] = float(sTime[i])
    UDECParameters['$vTable'] = vString[i]
    UDECParameters['$vel'] = vel[i]
    for j in range(len(confiningStress)):
        UDECParameters['$cStress'] = -confiningStress[j]
        UDECParameters['$mName'] = '\''+mName+'('+str(i)+'.'+str(confiningStress[j])+')'+'\''      
        with open('UDECModel.tpl', 'r') as templateFile:
            template = templateFile.read()
            for k in UDECParameters.keys():
                template = template.replace(k, str(UDECParameters[k]))
            fileNames.append('{0}({1}.{2})_Model.dat'.format(mName, i, confiningStress[j]))
            with open(fileNames[-1], 'w') as modelFile:
                modelFile.write(template)
                
with open('{0}(batchrun).dat'.format(mName), 'w') as modelFile:
    batchrun = []
    for i in range(len(fileNames)):
        batchrun.append('new\n')
        batchrun.append('call \'{}\'\n'.format(os.path.join(os.getcwd(), fileNames[i])))
    modelFile.writelines(batchrun)

        


# accelTime_t = velTable_t[-1]/10
# amp = -1
# vString_t = '0 {0} '.format(amp)
# for i in range(len(velTable_t)-1):
    # vString_t += '{0} {1} {2} {3} '.format(velTable_t[i]-accelTime_t, amp, velTable_t[i]+accelTime_t, amp*-1)
    # amp = amp*-1
# vString_t += '{0} {1}'.format(velTable_t[-1], amp)

# accelTime_c = velTable_c[-1]/10
# amp = -1
# vString_c = '0 {0} '.format(amp)
# for i in range(len(velTable_c)-1):
    # vString_c += '{0} {1} {2} {3} '.format(velTable_c[i]-accelTime_c, amp, velTable_c[i]+accelTime_c, amp*-1)
    # amp = amp*-1
# vString_c += '{0} {1}'.format(velTable_c[-1], amp)
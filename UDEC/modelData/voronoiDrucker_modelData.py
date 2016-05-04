#Add cmd output and error handling
import os.path
mName = os.path.basename(__file__[:__file__.find('_')])

mSize = 10
bSize = 0.5
meshSize = 0.5
vorSeed = 1
rho = 2.7e-3
E = 12e3
nu = 0.3

jks = 1e3
jkn = 1e7
jFriction = 30
jCohesion = 0.1
jTension = 10
jDilation = 10

confiningStress = [0, 5, 10, 20]

units = 'm-MPa-Gg-s'
# testMode = 't' #c, t, or all
relVars = ['S22', 'LE11']

# #tensileTest
# sTime_t = 10
# velTable_t = [5, sTime_t]
# vel_t = -0.001

# #compressionTest
# sTime_c = 20
# velTable_c = [10, sTime_c]
# vel_c = 0.01

sTime = [20]
velTable = [[sTime[0]/2, sTime[0]]]
vel = [0.01]

# abaqusMaterial = 'concreteDamage'
# ostrichParameters = {'peakYeildStrain':{'init':100, 'low':99, 'high':101}, #should be e-3
                                # 'peakYeildStress':{'init':10.5e6, 'low':5e6, 'high':15e6},
                                # 'initialCompressiveYeild':{'init':3.1e6, 'low':1e6, 'high':5e6},
                                # 'compressiveDamageScaling':{'init':0.5, 'low':0.4, 'high':0.6},
                                # 'initialTensileYeild':{'init':2.2e6, 'low':1e6, 'high':5e6},
                                # 'tLambda':{'init':2.2e3, 'low':1e3, 'high':5e3},
                                # 'tensileDamageScaling':{'init':0.5, 'low':0.4, 'high':0.6},
                                # 'elasticModulus':{'init':7.5e9, 'low':5e9, 'high':15e9},
                                # 'poissonsRatio':{'init':0.35, 'low':0.3, 'high':0.4}}
                                
abaqusMaterial = 'druckerDamage'
parameterizationSplits = [[1, sTime[0]/2]]
ostrichParameters = {'frictionAngle':{'init':15, 'low':10, 'high':20}, 
                                'dilationAngle':{'init':10, 'low':5, 'high':15},
                                'hardening_A':{'init':5e6, 'low':1e6, 'high':10e6},
                                'hardening_B':{'init':10e6, 'low':5e6, 'high':20e6},
                                'johnson_D2':{'init':20e-3, 'low':1e-3, 'high':100e-3},
                                'johnson_D3':{'init':-2, 'low':-5, 'high':-1},
                                'failureDisplacement':{'init':50e-6, 'low':10e-6, 'high':100e-6},
                                'initialTensileStrength':{'init':10e3, 'low':5e3, 'high':50e3},
                                'elasticModulus':{'init':7.5e9, 'low':5e9, 'high':15e9},
                                'poissonsRatio':{'init':0.35, 'low':0.3, 'high':0.4}}
 

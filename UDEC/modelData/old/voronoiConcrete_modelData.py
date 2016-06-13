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
relVars = ['S22', 'LE22']

sTime = [10, 20]
nSteps = 50
velTable = [[sTime[0]/2, sTime[0]], [sTime[0]/2, sTime[1]]]
vel = [-0.001, 0.01]

abaqusMaterial = 'concreteDamage'
parameterizationSplits = [[], []]
ostrichParameters = {'peakYeildStrain':{'init':100, 'low':99, 'high':101}, #should be e-3
                                'peakYeildStress':{'init':10.5e6, 'low':5e6, 'high':15e6},
                                'initialCompressiveYeild':{'init':3.1e6, 'low':1e6, 'high':5e6},
                                'compressiveDamageScaling':{'init':0.5, 'low':0.4, 'high':0.6},
                                'initialTensileYeild':{'init':2.2e6, 'low':1e6, 'high':5e6},
                                'tLambda':{'init':2.2e3, 'low':1e3, 'high':5e3},
                                'tensileDamageScaling':{'init':0.5, 'low':0.4, 'high':0.6},
                                'elasticModulus':{'init':7.5e9, 'low':5e9, 'high':15e9},
                                'poissonsRatio':{'init':0.35, 'low':0.3, 'high':0.4}}

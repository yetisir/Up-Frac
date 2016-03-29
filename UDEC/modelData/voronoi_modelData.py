#Add cmd output and error handling
mName = 'voronoi'

mSize = 10
bSize = 0.5
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

confiningStress = 0

units = 'm-MPa-Gg-s'
testMode = 't' #c, t, or all
relVars = ['S22']

#tensileTest
sTime_t = 10
velTable_t = [5, sTime_t]
vel_t = -0.001

#compressionTest
sTime_c = 20
velTable_c = [10, sTime_c]
vel_c = 0.01

abaqusMaterial = 'concreteDamage'

ostrichParametersText = '''
#parameter	                            init.	        low	        high	        tx_in            tx_ost	      tx_out
$peakYeildStrain                        5.4e-3      0.005        0.03         none             none           none
$peakYeildStress                       10.5e6      5e6           20e6         none             none           none
$initialCompressiveYeild             3.1e6        1e6          10e6         none             none           none
$compressiveDamageScaling      0.5           0.3           0.6         none             none           none
$initialTensileYeild		                2.2e6       1e6           10e6         none             none           none
$tLambda                                  2.2e3       1e3           10e3         none             none           none
$tensileDamageScaling		        0.9           0.5            1              none             none           none
$elasticModulus			                7.5e9       10e9          15e9         none	            none           none
$poissonsRatio                           0.35         0.2           0.4           none             none           none
'''

ostrichParameters = {'peakYeildStrain':{'init':100, 'low':99, 'high':101}, #should be e-3
                                'peakYeildStress':{'init':10.5e6, 'low':5e6, 'high':15e6},
                                'initialCompressiveYeild':{'init':3.1e6, 'low':1e6, 'high':5e6},
                                'compressiveDamageScaling':{'init':0.5, 'low':0.4, 'high':0.6},
                                'initialTensileYeild':{'init':2.2e6, 'low':1e6, 'high':5e6},
                                'tLambda':{'init':2.2e3, 'low':1e3, 'high':5e3},
                                'tensileDamageScaling':{'init':0.5, 'low':0.4, 'high':0.6},
                                'elasticModulus':{'init':7.5e9, 'low':5e9, 'high':15e9},
                                'poissonsRatio':{'init':0.35, 'low':0.3, 'high':0.4}}
 
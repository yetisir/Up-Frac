import os.path
mName = os.path.basename(__file__[:__file__.find('_')])

mSize = 10
bSize = 0.5
meshSize = 0.5
vorSeed = 1
rho = 2.7e-3
E = 65e3
nu = 0.2

jks = 20e6
jkn = 20e6
jFriction = 30
jCohesion = 0
jTension = 0
jDilation = 10

confiningStress = [0, 5, 10, 20]

units = 'm-MPa-Gg-s'
relVars = ['S22', 'LE22']

sTime = [10]
nSteps = 50
velTable = [[sTime[0]]]
vel = [0.05]
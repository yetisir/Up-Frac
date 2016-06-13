import os.path
mName = os.path.basename(__file__[:__file__.find('.py')])

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

confiningStress = [5, 10, 20]

units = 'm-MPa-Gg-s'
relVars = ['S22', 'LE22']

sTime = [20]
nSteps = 50
velTable = [[sTime[0]/2, sTime[0]]]
vel = [0.01]
                               
abaqusMaterial = 'druckerDamage'
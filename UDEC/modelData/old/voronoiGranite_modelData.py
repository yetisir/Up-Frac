import os.path
modelName = os.path.basename(__file__[:__file__.find('.py')])

modelSize = 10
blockSize = 0.5
meshSize = 0.5
voronoiSeed = 1
rho = 2.7e-3
E = 65e3
nu = 0.2

jks = 20e3
jkn = 20e3
jFriction = 30
jCohesion = 0
jTension = 0
jDilation = 10

confiningStress = [0, 5, 10]

units = ['m', 'MPa', 'Gg', 's']
relevantMeasurements = ['S22']

simulationTime = [100]
numberOfSteps = 50
velocityTable = [[simulationTime[0]]]
velocity = [0.005]

timeStepFraction = 0.01

abaqusMaterial = 'druckerDamage'


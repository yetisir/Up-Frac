mName = 'voronoiGraniteReverse'
sName = ['voronoiGraniteReverse(0.0)', 'voronoiGraniteReverse(0.1)', 'voronoiGraniteReverse(0.2)', 'voronoiGraniteReverse(0.3)']

abaqusMaterial = 'concreteDamage'
    
gridPoints = [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]

sectionLocation = (10/2, 10/2, 0.0)

simulationTime = 100
numberOfSteps = 50

confiningStress = [500000.0, 1000000.0, 2000000.0, 4000000.0]

density = 2700.0
approxStrain = 0.05

try:
    from abaqusConstants import *
        
    elementType = CPE4R
    elementShape = QUAD
    meshSize = 10

    instanceName = 'BLOCK-1'

    boundaries = {'Bottom': (10/2, 0.0, 0.0), 'Top':(10/2, 10, 0.0), 'Left':(0.0, 10/2, 0.0), 'Right':(10, 10/2, 0.0)}

    # steps = ('Initial', 'Step-1', 'Step-2')
    v = 0.005
    vNames = (('Bottom', ), ('Top', ), ('Left', ), ('Right', ))
    velocityTable = ((0, -1), (40.0, -1), (60.0, 1), (100, 1))

    largeDef=ON
except ImportError: pass
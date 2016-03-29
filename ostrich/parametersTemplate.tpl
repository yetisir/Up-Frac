mName = $$mName
    
gridPoints = [[0, 0], [$$mSize, 0], [$$mSize, $$mSize], [0, $$mSize], [0, 0]]

sectionLocation = ($$mSize/2, $$mSize/2, 0.0)

simulationTime = $$sTime
numberOfSteps = 50

confiningStress = $$confStress

try:
    from abaqusConstants import *
        
    elementType = CPE4R
    elementShape = QUAD
    meshSize = 10

    instanceName = 'BLOCK-1'

    boundaries = {'Bottom': ($$mSize/2, 0.0, 0.0), 'Top':($$mSize/2, $$mSize, 0.0), 'Left':(0.0, $$mSize/2, 0.0), 'Right':($$mSize, $$mSize/2, 0.0)}

    steps = ('Initial', 'Step-1', 'Step-2')
    v = $$vel
    vNames = (('Bottom', ), ('Top', ), ('Left', ), ('Right', ))
    velocityTable = $$vString

    largeDef=ON
except ImportError: pass
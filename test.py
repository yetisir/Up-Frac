import importlib
import pickle
import os
def getBoundaryVelocities(parameterizationRun):
    velocities = []
    displacements = []
    for k in range(len(modelData.confiningStress)):
        with open(os.path.join('HOMOGENIZE', 'binaryData', '{0}({1}.{2})_homogenizedData.pkl'.format(modelData.modelName, parameterizationRun, k)), 'rb') as bundleFile:
            bundle = pickle.load(bundleFile)
            timeHistory = bundle[0]
            stressHistory = bundle[1]
            strainHistory = bundle[2]
        LE11 = [x[0,0] for x in strainHistory]
        LE22 = [x[1,1] for x in strainHistory]
        
        U1 = [x*modelData.modelSize for x in LE11]
        U2 = [x*modelData.modelSize for x in LE22]

        # velocityTime = [(timeHistory[i+1]+timeHistory[i])/2 for i in range(len(timeHistory)-1)]
        # v1 = [(U1[i+1]-U1[i])/(timeHistory[i+1]-timeHistory[i]) for i in range(len(timeHistory)-1)]
        # v2 = [(U2[i+1]-U2[i])/(timeHistory[i+1]-timeHistory[i]) for i in range(len(timeHistory)-1)]
        # with open('test.log', 'a') as file:
            # file.writelines([str(v1), '\n', str(v2), '\n'])
        
        # velocityTime = [0] + velocityTime + [timeHistory[-1]]
        # v1 = [v1[0]] + v1 + [v1[-1]]
        # v2 = [v2[0]] + v2 + [v2[-1]]
        
        # v1Tuple = [(velocityTime[i], v1[i]) for i in range(len(velocityTime))]
        # v2Tuple = [(velocityTime[i], v2[i]) for i in range(len(velocityTime))]

        displacements.append([timeHistory, U1, U2])
    return displacements
    
def importModelData(modelName):
    global modelData
    modelData = importlib.import_module('UDEC.modelData.'+modelName)


if __name__ == '__main__':
    importModelData('voronoiGranite')
    v = getBoundaryVelocities(0)
    import matplotlib.pyplot as plt
    cs = 1
    data = v[cs]
    plt.plot(data[0], data[1], 'r-', label='U1')
    plt.plot(data[0], data[2], 'b-', label='U2')
    plt.legend()
    plt.show()
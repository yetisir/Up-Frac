import pickle
import sys
import os
import numpy
import time
import random
from HOMOGENIZE.Plot import Plot
import matplotlib.pyplot as plt

class UpFracPlot(Plot):
    def __init__(self, plotName, fileName, showPlots=True, interactive=True):
        Plot.__init__(self, plotName, showPlots=showPlots, interactive=interactive)
        
        demFileName = os.path.join('HOMOGENIZE', 'binaryData', fileName+'_homogenizedData.pkl')
        with open(demFileName, 'rb') as demFile:
            self.demData = pickle.load(demFile)
            
        femFileName = os.path.join('OSTRICH', 'fittedHistory', fileName+'_fittedHistory.pkl')
        self.femDataList = []
        with open(femFileName, 'rb') as femFile:
            while True:
                try:
                    femData = pickle.load(femFile)
                    self.femDataList.append(femData)
                except EOFError:
                    break
        
        self.animationImages = [[] for _ in range(len(self.femDataList))] #num frames
        self.fileName = fileName
        
    #Plotting Functions
    def plotFemCurves(self, direction):
        print('Plotting FEM stress-strain curves:')
        for i in range(len(self.femDataList)):
            stressData = self.femDataList[i][1]
            strainData = self.femDataList[i][2]
            if direction == '11':
                dirIndex=0
            elif direction == '22':
                dirIndex=1
            elif direction == '12':
                dirIndex=2            
            stress = [x[dirIndex] for x in stressData]
            strain = [x[dirIndex] for x in strainData]
            self.animationImages[i] += self.axes.plot(strain, stress, 'b.', label='FEM Approximation')
        print('\tDone')           

        
    def plotCurrentFemCurve(self, handle, direction):
        femFileName = os.path.join('OSTRICH', 'fittedHistory', self.fileName+'_fittedHistory.pkl')
        with open(femFileName, 'rb') as femFile:
            femData = pickle.load(femFile)
        
            stressData = femData[1]
            strainData = femData[2]
            if direction == '11':
                dirIndex=0
            elif direction == '22':
                dirIndex=1
            elif direction == '12':
                dirIndex=2            
            stress = [x[dirIndex]*random.random() for x in stressData]
            strain = [x[dirIndex]*random.random() for x in strainData]
            handle.set_xdata(strain)
            handle.set_ydata(stress)
            
    def interactivePlot(self, direction):
        plt.ion()
        h, = self.axes.plot([],[], 'b.')
        plt.show()
        while True:
            self.plotCurrentFemCurve(h, direction)
            plt.draw()
            plt.pause(0.5)
            

    def plotDemCurve(self, direction):
        print('Plotting DEM stress-strain curves:')
        stressData = self.demData[1]
        strainData = self.demData[2]
        if direction == '11':
            dirIndex=0
        elif direction == '22':
            dirIndex=1
        elif direction == '12':
            dirIndex=2
        stress = [x[dirIndex] for x in stressData]
        strain = [x[dirIndex] for x in strainData]

        for i in range(len(self.femDataList)):
            self.animationImages[i] += self.axes.plot(strain, stress, 'r*', label='DEM Simulation')
        print('\tDone')        

    def setAxis(self, direction):
        axisLimits = self.limits(direction)
        self.axes.set_xlim(axisLimits[0], axisLimits[1])
        self.axes.set_ylim(axisLimits[2], axisLimits[3])
        self.labelAxis()             
        
    def limits(self, direction):
        demStress = self.demData[1]
        demStrain = self.demData[2]
        if direction == '11':
            dirIndex=(0,0)
        elif direction == '22':
            dirIndex=(1,1)
        elif direction == '12':
            dirIndex=(1,2)
        maxStress = max([x[dirIndex] for x in demStress])
        minStress = min([x[dirIndex] for x in demStress])
        maxStrain = max([x[dirIndex] for x in demStrain])
        minStrain = min([x[dirIndex] for x in demStrain])
        
        stressBuffer = (maxStress-minStress)*0.2
        strainBuffer = (maxStrain-minStrain)*0.2
        
        return [minStrain-strainBuffer, maxStrain+strainBuffer, minStress-stressBuffer, maxStress+stressBuffer]        
    
    def labelAxis(self):
        self.axes.set_xlabel('Strain')
        self.axes.set_ylabel('Stress')     
    
    
def main():
    os.system('cls')
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
        
    P = UpFracPlot('test', fileName)
    P.setAxis('22')
    P.plotDemCurve('22')
    #P.plotFemCurves('22')
    P.interactivePlot('22')
    P.animate()
    


if __name__ =='__main__':
    main()
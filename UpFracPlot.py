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
        
        #an issue with matplotlib returns a depreciation warning. this suprpesses it.
        import warnings
        warnings.filterwarnings("ignore")
         
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
        numFrames = 0
        with open(femFileName, 'rb') as femFile:
            while True:
                try:
                    femData = pickle.load(femFile)
                    numFrames += 1
                except EOFError:
                    break
        
            stressData = femData[1]
            strainData = femData[2]
            if direction == '11':
                dirIndex=0
            elif direction == '22':
                dirIndex=1
            elif direction == '12':
                dirIndex=2            
            stress = [x[dirIndex] for x in stressData]
            strain = [x[dirIndex] for x in strainData]
            handle.set_xdata(strain)
            handle.set_ydata(stress)
        return numFrames
            
    def interactivePlot(self, direction):
        plt.ion()
        h, = self.axes.plot([],[], 'b.')
        plt.show()
        lastNumFrames = 0
        print('Plotting FEM stress-strain curves:')
        print('\tChecking for new data...', end='')
        while True:
            currentNumFrames = self.plotCurrentFemCurve(h, direction)
            if currentNumFrames == lastNumFrames:
                resultString = 'No new data found'
            else:
                resultString = 'Plotting new data'
                lastNumFrames = currentNumFrames
            print (resultString, end='')
            plt.draw()
            sys.stdout.flush()
            plt.pause(0.5)
            print('\b'*len(resultString)+' '*len(resultString), end='')
            sys.stdout.flush()
            print('\b'*len(resultString), end='')
            plt.pause(0.5)
            
            
    def plotDemCurve(self, direction):
        print('Plotting DEM stress-strain curves:')
        stressData = self.demData[1]
        strainData = self.demData[2]
        if direction == '11':
            dirIndex=(0,0)
        elif direction == '22':
            dirIndex=(1,1)
        elif direction == '12':
            dirIndex=(0,1)
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
    
    direction = clargs[2] #'22'
    P.setAxis(direction)
    P.plotDemCurve(direction)
    #P.plotFemCurves('22')
    P.interactivePlot(direction)
    P.animate()
    


if __name__ =='__main__':
    main()
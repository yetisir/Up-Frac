import pickle
import sys
import os
import numpy
import scipy
import time
import random
from HOMOGENIZE.Plot import Plot
from HOMOGENIZE.Homogenize import Homogenize
import matplotlib.pyplot as plt
import matplotlib
import argparse
import importlib

class StressStrainPlot(Plot):
    def __init__(self, mode, direction=2, showPlots=True, interactive=True, colorBar=False, parameterizationRun=0):
        Plot.__init__(self, '{0}_{1}_dir-{2}'.format(modelData.abaqusMaterial, mode, direction), showPlots=showPlots, interactive=interactive, colorBar=colorBar)

        self.demData = []
        self.femDataList = []
        for i in range(len(modelData.confiningStress)):
            demFileName = os.path.join('HOMOGENIZE', 'binaryData', '{0}({1}.{2})_homogenizedData.pkl'.format(modelData.modelName, parameterizationRun, i))
            with open(demFileName, 'rb') as demFile:
                self.demData.append(pickle.load(demFile))
            print (self.demData[-1][-1][-1])
            try:    
                femFileName = os.path.join('OSTRICH', 'fittedHistory', '{0}({1}.{2})_{3}_fittedHistory.pkl'.format(modelData.modelName, parameterizationRun, i, modelData.abaqusMaterial))
                self.femDataList.append([])
                with open(femFileName, 'rb') as femFile:
                    while True:
                        try:
                            femData = pickle.load(femFile)
                            self.femDataList[i].append(femData)
                        except EOFError:
                            break
                self.animationImages = [[] for _ in range(len(self.femDataList[0]))] #num frames
            except FileNotFoundError:
                self.animationImages = [[]]
        if len(self.animationImages) == 0:
            self.animationImages = [[]]
        #an issue with matplotlib returns a depreciation warning. this suprpesses it.
        import warnings
        warnings.filterwarnings("ignore")
        self.parameterizationRun = parameterizationRun
        self.fileName = modelData.modelName
        self.direction=direction-1
    #Plotting Functions

    def plotAllFemCurves(self):
        print('Plotting FEM stress-strain curves:')
        for i in range(len(modelData.confiningStress)):
            self.plotFemCurves(i)
            print('\tPlotting for confining stress={0}MPa'.format(modelData.confiningStress[i]/1e6))
        print('\tDone')        
        
        
    def plotFemCurves(self, confiningStress):
        for i in range(len(self.femDataList[0])):
            stressData = self.femDataList[confiningStress][i][1]
            strainData = self.femDataList[confiningStress][i][2]
            stress = [(x[self.direction])/-1e6 for x in stressData]
            strain = [x[self.direction]*-100 for x in strainData]
            self.animationImages[i] += self.axes.plot(strain, stress, '--', linewidth=2, color=modelData.colors[confiningStress], label='CDM - {0}MPa'.format(modelData.confiningStress[confiningStress]/1e6))

    def plotCurrentFemCurve(self, handle, confiningStress):
        femFileName = os.path.join('OSTRICH', 'fittedHistory', '{0}({1}.{2})_{3}_fittedHistory.pkl'.format(modelData.modelName, self.parameterizationRun, confiningStress, modelData.abaqusMaterial))
        numFrames = 0
        try:
            with open(femFileName, 'rb') as femFile:
                while True:
                    try:
                        femData = pickle.load(femFile)
                        numFrames += 1
                    except EOFError:
                        break
            
                stressData = femData[1]
                strainData = femData[2]
      
                stress = [(x[self.direction])/-1e6 for x in stressData]
                strain = [x[self.direction]*-100 for x in strainData]
                handle.set_xdata(strain)
                handle.set_ydata(stress)
        except:
            pass
        return numFrames
            
    def interactivePlot(self):
        plt.ion()
        handles = []
        for i in range(len(modelData.confiningStress)):
            h, = self.axes.plot([],[], '*-', linewidth=2, color=modelData.colors[i])
            handles.append(h)
        plt.show()
        lastNumFrames = 0
        print('Plotting FEM stress-strain curves:')
        print('\tChecking for new data...', end='')
        while True:
            totalNumFrames = 0
            for i in range(len(handles)):
                currentNumFrames = self.plotCurrentFemCurve(handles[i], i)
                totalNumFrames += currentNumFrames
            if totalNumFrames == lastNumFrames:
                resultString = 'No new data found'
            else:
                resultString = 'Plotting new data'
                lastNumFrames = totalNumFrames
            print (resultString, end='')
            plt.draw()
            sys.stdout.flush()
            plt.pause(0.5)
            print('\b'*len(resultString)+' '*len(resultString), end='')
            sys.stdout.flush()
            print('\b'*len(resultString), end='')
            plt.pause(0.5)

    def plotDemCurves(self):
        print('Plotting DEM stress-strain curves...')
        for i in range(len(modelData.confiningStress)):
            self.plotDemCurve(i)
            print('\tPlotting for confining stress={0}MPa'.format(modelData.confiningStress[i]/1e6))
        print('\tDone')        
            
    def plotDemCurve(self, confiningStress):
        stressData = self.demData[confiningStress][1]
        strainData = self.demData[confiningStress][2]

        stress = [(x[(self.direction,self.direction)])/-1e6 for x in stressData]
        strain = [x[(self.direction,self.direction)]*-100 for x in strainData]
        for i in range(len(self.animationImages)):
            self.animationImages[i] += self.axes.plot(strain, stress, '-', linewidth=1, color=modelData.colors[confiningStress], label='DEM - {0}MPa'.format(modelData.confiningStress[confiningStress]/1e6))
    def setAxis(self):
        axisLimits = self.limits()
        self.axes.set_xlim(axisLimits[0], axisLimits[1])
        self.axes.set_ylim(axisLimits[2], axisLimits[3])
        self.labelAxis()             
        
    def limits(self):
        demStress = []
        demStrain = []
        for i in range(len(modelData.confiningStress)):
            demStress += self.demData[i][1]
            demStrain += self.demData[i][2]

        maxStress = max([(x[(self.direction,self.direction)])/-1e6 for x in demStress])
        minStress = min([(x[(self.direction,self.direction)])/-1e6 for x in demStress])
        
        maxStrain = max([x[(self.direction,self.direction)]*-100 for x in demStrain])
        minStrain = min([x[(self.direction,self.direction)]*-100 for x in demStrain])

        if abs(maxStrain) > abs(minStrain):
            minStrain = 0
        else:
            maxStrain = 0

        if abs(maxStress) > abs(minStress):
            minStress = 0
        else:
            maxStress = 0
        stressBuffer = (maxStress-minStress)*0.2
        strainBuffer = (maxStrain-minStrain)*0.3
        if self.direction == 1:
            return [minStrain, maxStrain+strainBuffer, minStress, maxStress+stressBuffer]        
        elif self.direction == 0:
            return [minStrain-strainBuffer, maxStrain, minStress, maxStress+stressBuffer]        
    
    def labelAxis(self):
        if self.direction == 1:
            self.axes.set_xlabel('Vertical Strain ($\%$)')
            self.axes.set_ylabel('Vertical Stress ($MPa$)')
        elif self.direction == 0:
            self.axes.set_xlabel('Horizontal Strain ($\%$)')
            self.axes.set_ylabel('Horizontal Stress ($MPa$)')
            

    def addAnnotations(self):
        for i in range(len(modelData.confiningStress)):
            #strains = [x[self.direction]*-100 for x in self.femDataList[i][-1][2]]
            strains = [x[(self.direction, self.direction)]*-100 for x in self.demData[i][2]]
            #stresses = [x[self.direction]/-1e6 for x in self.femDataList[i][-1][1]]
            stresses = [x[(self.direction, self.direction)]/-1e6 for x in self.demData[i][1]]
            if self.direction == 1:
                x = max(strains)*1.1
                y = stresses[strains.index(x)]
            elif self.direction == 0:
                x = min(strains)
                y = stresses[strains.index(x)]
                x-=4
            textArtist = matplotlib.text.Text(x, y, '${0}MPa$'.format(modelData.confiningStress[i]/1e6))
            for j in range(len(self.animationImages)):
                self.animationImages[j].append(textArtist)
        solidLine = matplotlib.lines.Line2D([0,1], [0,1], linestyle='-', color='k')
        dashedLine = matplotlib.lines.Line2D([0,1], [0,1], linestyle='--', color='k')
        leg = matplotlib.legend.Legend(self.axes, [solidLine, dashedLine], ['DEM Response', 'Fitted CDM Response'], loc=2, framealpha=1, fontsize=12, frameon=False)
        for i in range(len(self.animationImages)):
            self.animationImages[i].append(leg)
        self.addRootMeanSquareErrorStrain()
        # self.addRootMeanSquareErrorStress()
        
    def addRootMeanSquareErrorStress(self):
        demStress = []
        femStress = []
        for i in range(len(modelData.confiningStress)):
            for j in range(len(self.demData[0][0])):
                demStress.append(self.demData[i][1][j][(self.direction,self.direction)])
                femStress.append(self.femDataList[i][-1][1][j][self.direction])
        rmse = numpy.sqrt(numpy.nanmean(((numpy.array(demStress) - numpy.array(femStress)) ** 2)))
        textArtist = matplotlib.text.Text(0.05, 0.82, 'RMSE=${0:.2f}MPa$'.format(rmse/1e6), transform=self.axes.transAxes)
        for i in range(len(self.animationImages)):
            self.animationImages[i].append(textArtist)
            
    def addRootMeanSquareErrorStrain(self):
        demStrain = []
        femStrain = []
        for i in range(len(modelData.confiningStress)):
            for j in range(len(self.demData[0][0])):
                demStrain.append(self.demData[i][2][j][(self.direction,self.direction)])
                femStrain.append(self.femDataList[i][-1][2][j][self.direction])
        rmse = numpy.sqrt(numpy.nanmean(((numpy.array(demStrain) - numpy.array(femStrain)) ** 2)))
        textArtist = matplotlib.text.Text(0.05, 0.82, 'RMSE=${0:.2f}$'.format(rmse), transform=self.axes.transAxes)
        for i in range(len(self.animationImages)):
            self.animationImages[i].append(textArtist)
            
    
def main(parameterizationRun=0, mode='lastFrame', direction=2):
    os.system('cls')
       
    P = StressStrainPlot(mode, parameterizationRun=parameterizationRun, direction=direction)
    P.setAxis()
    try:
        P.plotDemCurves()
    except:
        print('\tError Plotting DEM Curves')
    
    if mode == 'demOnly':
        #P.addLegend()
        P.lastFrame()
    else:
        try:
            if mode == 'lastFrame':
                P.plotAllFemCurves()
                P.addAnnotations()
                P.lastFrame()
            elif mode == 'firstFrame':
                P.plotAllFemCurves()
                P.addAnnotations()
                P.firstFrame()
            elif mode == 'continuous':
                P.interactivePlot()
            elif mode == 'history':
                P.plotAllFemCurves()
                #P.addAnnotations()
                P.animate()
            else:
                print('Mode not recognized')
        except Exception as E:
            print(E)
            print('\tError Plotting FEM Curves')
def importModelData(modelName):
    global modelData
    modelData = importlib.import_module('UDEC.modelData.'+modelName)
    
    
def run(modelName, parameterizationRun=0, mode='lastFrame'):
    importModelData(modelName)
    main(parameterizationRun=parameterizationRun, mode=mode)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UpFracPlot:')
    parser.add_argument('-n', '--name', required=True ,help='Name of the file containing the model data without the extension')
    parser.add_argument('-p', '--parameterizationRun', required=False, type=int, default=0, help='Parameterization run')
    parser.add_argument('-m', '--mode', required=False, default=0, help='Type of Plot')
    parser.add_argument('-d', '--direction', required=True, type=int, default=2, help='Direction of Stress')

    args = parser.parse_args()
    modelName = args.name
    parameterizationRun = args.parameterizationRun
    mode = args.mode
    direction = args.direction
    
    importModelData(modelName)
    main(parameterizationRun=parameterizationRun, mode=mode, direction=direction)


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
    def __init__(self, mode, showPlots=True, interactive=True, colorBar=False, parameterizationRun=0):
        Plot.__init__(self, '{0}_{1}'.format(modelData.abaqusMaterial, mode), showPlots=showPlots, interactive=interactive, colorBar=colorBar)

        self.demData = []
        self.femDataList = []
        for i in range(len(modelData.confiningStress)):
            demFileName = os.path.join('HOMOGENIZE', 'binaryData', '{0}({1}.{2})_homogenizedData.pkl'.format(modelData.modelName, parameterizationRun, i))
            with open(demFileName, 'rb') as demFile:
                self.demData.append(pickle.load(demFile))
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
            stress = [(x[1])/-1e6 for x in stressData]
            strain = [x[1]*-100 for x in strainData]
            self.animationImages[i] += self.axes.plot(strain, stress, '--', linewidth=2, color=modelData.colors[confiningStress], label='CDM - {0}MPa'.format(modelData.confiningStress[confiningStress]/1e6))

    def plotCurrentFemCurve(self, handle, confiningStress):
        femFileName = os.path.join('OSTRICH', 'fittedHistory', '{0}({1}.{2})_{3}_fittedHistory.pkl'.format(modelData.modelName, self.parameterizationRun, confiningStress, modelData.abaqusMaterial))
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
  
            stress = [(x[1])/-1e6 for x in stressData]
            strain = [x[1]*-100 for x in strainData]
            handle.set_xdata(strain)
            handle.set_ydata(stress)
        return numFrames
            
    def interactivePlot(self):
        plt.ion()
        handles = []
        for i in range(len(modelData.confiningStress)):
            h, = self.axes.plot([],[], '--', linewidth=2, color=modelData.colors[i])
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

        stress = [(x[(1,1)])/-1e6 for x in stressData]
        strain = [x[(1,1)]*-100 for x in strainData]
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

        maxStress = max([(x[(1,1)])/-1e6 for x in demStress])
        minStress = 0
        maxStrain = max([x[(1,1)]*-100 for x in demStrain])
        minStrain = 0
        
        stressBuffer = (maxStress-minStress)*0.2
        strainBuffer = (maxStrain-minStrain)*0.3
        
        return [0, maxStrain+strainBuffer, 0, maxStress+stressBuffer]        
    
    def labelAxis(self):
        self.axes.set_xlabel('Axial Strain ($\%$)')
        self.axes.set_ylabel('Axial Stress ($MPa$)')

    def addAnnotations(self):
        for i in range(len(modelData.confiningStress)):
            strains = [x[1]*-100 for x in self.femDataList[i][-1][2]]
            stresses = [x[1]/-1e6 for x in self.femDataList[i][-1][1]]
            x = max(strains)
            y = stresses[strains.index(x)]
            x+=0.1
            textArtist = matplotlib.text.Text(x, y, '${0}MPa$'.format(modelData.confiningStress[i]/1e6))
            for j in range(len(self.animationImages)):
                self.animationImages[j].append(textArtist)
        solidLine = matplotlib.lines.Line2D([0,1], [0,1], linestyle='-', color='k')
        dashedLine = matplotlib.lines.Line2D([0,1], [0,1], linestyle='--', color='k')
        leg = matplotlib.legend.Legend(self.axes, [solidLine, dashedLine], ['DEM Response', 'Fitted CDM Response'], loc=2, framealpha=1, fontsize=12, frameon=False)
        for i in range(len(self.animationImages)):
            self.animationImages[i].append(leg)
        self.addRootMeanSquareError()
        
    def addRootMeanSquareError(self):
        demStress = []
        femStress = []
        for i in range(len(modelData.confiningStress)):
            for j in range(len(self.demData[0][0])):
                demStress.append(self.demData[i][1][j][(1,1)])
                femStress.append(self.femDataList[i][-1][1][j][1])
        print(((numpy.array(demStress) - numpy.array(femStress)) ** 2))
        rmse = numpy.sqrt(numpy.nanmean(((numpy.array(demStress) - numpy.array(femStress)) ** 2)))
        textArtist = matplotlib.text.Text(0.05, 0.82, 'RMSE=${0:.2f}MPa$'.format(rmse/1e6), transform=self.axes.transAxes)
        for i in range(len(self.animationImages)):
            self.animationImages[i].append(textArtist)
            
    
def main(parameterizationRun=0, mode='lastFrame'):
    os.system('cls')
       
    P = StressStrainPlot(mode, parameterizationRun=parameterizationRun)
    P.setAxis()
    try:
        P.plotDemCurves()
    except:
        print('\tError Plotting DEM Curves')
    
    if mode == 'demOnly':
        P.addLegend()
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

    args = parser.parse_args()
    modelName = args.name
    parameterizationRun = args.parameterizationRun
    mode = args.mode
    
    importModelData(modelName)
    main(parameterizationRun=parameterizationRun, mode=mode)


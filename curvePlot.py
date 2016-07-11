from StressStrainPlot import StressStrainPlot
import os
import sys
import argparse
import importlib

def main(parameterizationRun=0):
    os.system('cls')
       
    P = StressStrainPlot('demOnly', parameterizationRun=parameterizationRun, showPlots=False)
    P.plotName = 'schematic'
    P.setAxis()
    P.plotDemCurves()
    P.plotAllFemCurves()
    P.lastFrame()
    P.removeFrame()
    P.saveFigure()
          
            
def importModelData(modelName):
    global modelData
    modelData = importlib.import_module('UDEC.modelData.'+modelName)
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UpFracPlot:')
    parser.add_argument('-n', '--name', required=True ,help='Name of the file containing the model data without the extension')

    args = parser.parse_args()
    modelName = args.name
    
    importModelData(modelName)
    main(parameterizationRun=0)

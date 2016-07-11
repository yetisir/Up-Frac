from HOMOGENIZE.FracPlot import FracPlot
from HOMOGENIZE import common
import os
import sys

def main():
    os.system('cls')
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
        
    P = FracPlot('blockModel', fileName=fileName, showPlots=False, colorBar=False)
    P.setAxis_Zoom()  
    P.plotBlocks()
    P.removeAxes()
    P.lastFrame()
    P.removeAxes()
    P.saveFigure()
if __name__ == '__main__':
    main()

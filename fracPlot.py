from HOMOGENIZE.FracPlot import FracPlot
from HOMOGENIZE import common
import os
import sys

def main():
    os.system('cls')
    
    clargs = sys.argv
    if len(clargs) >= 2:
        fileName = clargs[1]
        
    P = FracPlot('test', fileName=fileName)
    P.setAxis_Full()  
    P.plotStressField('S22', sigma=1)
    P.plotZones()
    P.plotBlocks()
    P.addLegend()
    P.animate()

if __name__ == '__main__':
    main()

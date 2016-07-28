from HOMOGENIZE.HomoPlot import HomoPlot
from HOMOGENIZE.Homogenize import Homogenize
from HOMOGENIZE import common
import os
import sys

def main():
    os.system('cls')
    fileName = 'voronoiGranite(0.0)'
    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
    P = HomoPlot('test', H, showPlots=True, colorBar=False)
    P.plotBlocks()
    P.plotBoundaryEdge_Initial(linewidth=1)
    P.plotBoundaryEdge(linewidth=2)
    
    P.setAxis_Full()
    P.specifyFrame(10)
    P.saveFigure()


if __name__ == '__main__':
    main()

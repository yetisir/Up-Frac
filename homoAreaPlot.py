from HOMOGENIZE.HomoPlot import HomoPlot
from HOMOGENIZE.Homogenize import Homogenize
from HOMOGENIZE import common
import os
import sys

def main():
    os.system('cls')
    fileName = 'voronoiGranite(0.0)'
    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
    P = HomoPlot('homogenizationBoundaryPlotZoom', H, showPlots=False, colorBar=False)
    P.plotBoundaryBlocks()
    P.plotBoundaryEdge_Initial(linewidth=1)
    P.plotBoundaryEdge(linewidth=2)
    
    P.setAxis_Zoom(centre=[.725,.2], zoom=6)
    P.plotZoomBox(centre=[.725,.2], zoom=7)
    P.lastFrame()
    P.saveFigure()


    P.clear()
    fileName = 'voronoiGranite(0.0)'
    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
    P = HomoPlot('homogenizationBoundaryPlot', H, showPlots=False, colorBar=False)
    P.plotBoundaryBlocks()
    P.plotBoundaryEdge_Initial(linewidth=1)
    P.plotBoundaryEdge(linewidth=2)
    
    P.setAxis_Full()
    P.plotZoomBox(centre=[.725,.2], zoom=7)

    P.addLegend(location='upper left')
    P.lastFrame()
    P.saveFigure()



    P.clear()
    fileName = 'voronoiGranite(0.0)'
    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
    P = HomoPlot('homogenizationAreaPlotZoom', H, showPlots=False, colorBar=False)
    P.plotBlocks()
    P.plotREV()
    P.plotBoundaryEdge(linewidth=3)
    
    P.setAxis_Zoom(centre=[.7,.3])
    P.plotZoomBox(centre=[.7,.3], zoom=4.5)
    P.firstFrame()
    P.saveFigure()


    P.clear()
    fileName = 'voronoiGranite(0.0)'
    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
    P = HomoPlot('homogenizationAreaPlot', H, showPlots=False, colorBar=False)
    P.plotBlocks()
    P.plotREV()
    P.plotBoundaryEdge(linewidth=3)
    
    P.setAxis_Full()
    P.plotZoomBox(centre=[.7,.3], zoom=4.5)

    P.addLegend(location='upper left')
    P.firstFrame()
    P.saveFigure()


if __name__ == '__main__':
    main()

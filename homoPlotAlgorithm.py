from HOMOGENIZE.HomoPlot import HomoPlot
from HOMOGENIZE.Homogenize import Homogenize
from HOMOGENIZE import common
import os
import sys

def main():
    os.system('cls')
    fileName = 'voronoiGranite(0.0)'
    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
    P = HomoPlot('homostep1', H, showPlots=False, colorBar=False)
    P.plotBoundaryBlocks()
    P.plotREV()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep1l'
    P.lastFrame()
    P.saveFigure()

    P = HomoPlot('homostep2', H, showPlots=False, colorBar=False)
    P.plotOutsideBlocks()
    P.plotREV()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep2l'
    P.lastFrame()
    P.saveFigure()
    
    P = HomoPlot('homostep3', H, showPlots=False, colorBar=False)
    P.plotBoundaryBlocks()
    P.plotBoundaryContacts()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep3l'
    P.lastFrame()
    P.saveFigure()
    
    P = HomoPlot('homostep4', H, showPlots=False, colorBar=False)
    P.plotBoundaryBlocks()
    P.plotBoundaryContactCorners()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep4l'
    P.lastFrame()
    P.saveFigure()
    
    P = HomoPlot('homostep5', H, showPlots=False, colorBar=False)
    P.plotBoundaryBlocks()
    P.plotBoundaryBlockContacts()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep5l'
    P.lastFrame()
    P.saveFigure()
    
    P = HomoPlot('homostep6', H, showPlots=False, colorBar=False)
    P.plotBoundaryContactBlocks()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep6l'
    P.lastFrame()
    P.saveFigure()

    P = HomoPlot('homostep7', H, showPlots=False, colorBar=False)
    P.plotBoundaryContactBlocks()
    P.plotBoundaryBlockCorners()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep7l'
    P.lastFrame()
    P.saveFigure()

    P = HomoPlot('homostep8', H, showPlots=False, colorBar=False)
    P.plotBoundaryContactBlocks()
    P.plotBoundaryCorners()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep8l'
    P.lastFrame()
    P.saveFigure()

    P = HomoPlot('homostep9', H, showPlots=False, colorBar=False)
    P.plotBoundaryContactBlocks()
    P.plotBoundaryEdge()
    P.plotBoundaryCorners()
    P.setAxis_Full()
    P.firstFrame()
    P.saveFigure()
    P.plotName = 'homostep9l'
    P.lastFrame()
    P.saveFigure()

##    P.clear()
##    fileName = 'voronoiGranite(0.0)'
##    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
##    P = HomoPlot('homostep2', H, showPlots=False, colorBar=False)
##    P.plotBoundaryBlocks()
##    P.plotBoundaryEdge_Initial(linewidth=1)
##    P.plotBoundaryEdge(linewidth=2)
##    
##    P.setAxis_Full()
##    P.plotZoomBox(centre=[.725,.2], zoom=2)
##
##    P.addLegend(location='upper left')
##    P.lastFrame()
##    P.saveFigure()
##
##
##
##    P.clear()
##    fileName = 'voronoiGranite(0.0)'
##    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
##    P = HomoPlot('homostep3', H, showPlots=False, colorBar=False)
##    P.plotBlocks()
##    P.plotREV()
##    P.plotBoundaryEdge(linewidth=3)
##    
##    P.setAxis_Zoom(centre=[.7,.3])
##    P.plotZoomBox(centre=[.7,.3], zoom=4.5)
##    P.firstFrame()
##    P.saveFigure()
##
##
##    P.clear()
##    fileName = 'voronoiGranite(0.0)'
##    H = Homogenize({'x':5, 'y':5}, 3, fileName=fileName)
##    P = HomoPlot('homostep4', H, showPlots=False, colorBar=False)
##    P.plotBlocks()
##    P.plotREV()
##    P.plotBoundaryEdge(linewidth=3)
##    
##    P.setAxis_Full()
##    P.plotZoomBox(centre=[.7,.3], zoom=4.5)
##
##    P.addLegend(location='upper left')
##    P.firstFrame()
##    P.saveFigure()


if __name__ == '__main__':
    main()

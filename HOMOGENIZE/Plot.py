import os
from collections import OrderedDict

class Plot(object):
    def __init__(self, plotName, showPlots=True, interactive=False, colorBar=True):
        if showPlots != True:
            import matplotlib
            matplotlib.use('Agg')
        global plt
        global animation
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
    
        print('-'*70)
        print('Establishing {} Plot'.format(plotName))
        print('-'*70)
        
        self.plotName = plotName
        
        #TODO: fix this to acocmodate non-colorbar plots
        if colorBar:
            self.figure = plt.figure(figsize=(6,5))
            self.axes = self.figure.add_axes([0.1, 0.1, 0.825*5/6, 0.825])
            self.colorBarAxes = self.figure.add_axes([0.825, 0.1, 0.05, 0.825])
        else:
            self.figure = plt.figure(figsize=(5,5))
            self.axes = self.figure.add_axes([0.15, 0.1, 0.8, 0.85])
            
            
    #Axis Functions    
    def setAxis_Full(self, equal=True):
        axisLimits = self.limits()
    
        if equal is True:
            self.axes.axis('equal')
        self.axes.set_xlim(axisLimits[0], axisLimits[1])
        self.axes.set_ylim(axisLimits[2], axisLimits[3])
        self.labelAxis()     
        
    def setAxis_Zoom(self, centre=(0.5,0.5), zoom=4):
        axisLimits = self.limits()
    
        self.axes.axis('equal')
        
        xMin = axisLimits[0]
        xMax = axisLimits[1]
        yMin = axisLimits[2]
        yMax = axisLimits[3]
        
        xLen = xMax - xMin
        yLen = yMax - yMin
        
        xCen = centre[0]*xLen + xMin
        yCen = centre[0]*yLen + yMin
        
        xOff = xLen/2/zoom
        yOff = yLen/2/zoom
        
        self.axes.set_xlim(xCen - xOff, xCen + xOff)
        self.axes.set_ylim(yCen - yOff, yCen + yOff)
        self.labelAxis()

    def addLegend(self):
        handles, labels = self.axes.get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        times = sorted(self.blockData)
        for i in range(len(times)):
            self.animationImages[i].append(self.axes.legend(by_label.values(), by_label.keys()))
        
    #Viewing Functions
    def animate(self, interval=50, delay=1000):
        delayFrames = int(delay/interval)
        ai = self.animationImages
        for i in range(delayFrames):
            ai.append(self.animationImages[-1])
        im_ani = animation.ArtistAnimation(self.figure, ai, interval=50, blit=True)
        print ('Encoding Video File:')
        self.saveVideo(im_ani)
        print('\tDone')
        self.showPlot()

    def firstFrame(self):
        self.axes.cla()
        for i in range(len(self.animationImages[0])):
            self.axes.add_artist(self.animationImages[0][i])
        self.showPlot()

    def lastFrame(self):
        self.axes.cla()
        for i in range(len(self.animationImages[-1])):
            self.axes.add_artist(self.animationImages[-1][i])
        self.saveFigure()
        self.showPlot()
        
    def saveFigure(self):
        fileName = os.path.join('figures', self.fileName+'_'+self.plotName) 
        self.figure.savefig(fileName+'.svg', format='svg')
        self.figure.savefig(fileName+'.png', format='png')

    def saveVideo(self, ani):
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, bitrate=1800)
        fileName = os.path.abspath(os.path.join('figures', self.fileName+'_'+self.plotName) )
        ani.save(fileName+'.mp4', writer=writer)

    def showPlot(self):
        self.labelAxis()
        plt.show()

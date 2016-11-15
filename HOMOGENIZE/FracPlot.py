import os
import numpy as np
import math
import sys
import pickle
import matplotlib.path as mplPath
import matplotlib
from . import common
from scipy.ndimage.filters import gaussian_filter
from collections import OrderedDict

from .DataSet import DataSet
from .Plot import Plot
class FracPlot(DataSet, Plot):
    def __init__(self, plotName, fileName=None, dataClass=None, showPlots=True, colorBar=True):
        DataSet.__init__(self, fileName=fileName, dataClass=dataClass)
        Plot.__init__(self, plotName, showPlots=showPlots, interactive=False, colorBar=colorBar)
        global plt
        global animation
        global colorbar
        global patches
        global matcolors
        import matplotlib.colors as matcolors
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        from matplotlib import colorbar, patches
        
        self.animationImages = [[] for _ in range(len(self.blockData.keys()))] #num frames

        time = min(self.blockData.keys())
        self.blocks = self.blockData[time].keys()
        self.zones = self.zoneData[time].keys()
        self.corners = self.cornerData[time].keys()
        self.contacts = self.contactData[time].keys()
        self.gridPoints = self.gridPointData[time].keys()
        self.domains = self.domainData[time].keys()
  
    #Model Functions
    def blockEdges(self, blocks, time = 0):
        if time == 0:
            time = min(self.blockData.keys())
        xEdge = []
        yEdge = []
        for block in blocks:
            blockCorners = self.blockData[time][block]['corners']
            for blockCorner in blockCorners:
                gridPointIndex = self.cornerData[time][blockCorner]['gridPoint']
                gridPoint = self.gridPointData[time][gridPointIndex]
                xEdge.append(gridPoint['x'])
                yEdge.append(gridPoint['y'])
            gridPointIndex = self.cornerData[time][blockCorners[0]]['gridPoint']
            gridPoint = self.gridPointData[time][gridPointIndex]
            xEdge.append(gridPoint['x'])
            yEdge.append(gridPoint['y'])
            xEdge.append(None)
            yEdge.append(None)
        return (xEdge, yEdge)

    def contactPoints(self, contacts, time = 0):
        if time == 0:
            time = min(self.blockData.keys())
        contactX = []
        contactY = []
        for contact in contacts:
            contactX.append(self.contactData[time][contact]['x'])
            contactY.append(self.contactData[time][contact]['y'])
        return (contactX, contactY)
        
    def cornerPoints(self, corners, time = 0):
        if time == 0:
            time = min(self.blockData.keys())
        cornerX = []
        cornerY = []
        for corner in corners:
            gp = self.cornerData[time][corner]['gridPoint']
            cornerX.append(self.gridPointData[time][gp]['x'])
            cornerY.append(self.gridPointData[time][gp]['y'])
        return (cornerX, cornerY)
        
    def zoneEdges(self, zones, time = 0):
        if time == 0:
            time = min(self.zoneData.keys())
        xEdge = []
        yEdge = []
        for zone in zones:
            zoneGridPoints = self.zoneData[time][zone]['gridPoints']
            for zoneGridPoint in zoneGridPoints:
                gridPoint = self.gridPointData[time][zoneGridPoint]
                xEdge.append(gridPoint['x'])
                yEdge.append(gridPoint['y'])
            gridPoint = self.gridPointData[time][zoneGridPoints[0]]
            xEdge.append(gridPoint['x'])
            yEdge.append(gridPoint['y'])
            xEdge.append(None)
            yEdge.append(None)
        return (xEdge, yEdge)

    #Plotting Functions
    def labelAxis(self):
        self.axes.set_xlabel('Horizontal (m)')
        self.axes.set_ylabel('Vertical (m)')
        
    def plotBlocks(self):
        times = sorted(self.blockData)
        print('Plotting block boundaries:')
        for i in range(len(times)):
            blockEdges = self.blockEdges(self.blocks, time=times[i])
            self.animationImages[i] += self.axes.plot(blockEdges[0], blockEdges[1], 'b-', label='Block Boundaries')
        print('\tDone')

    def plotContacts(self):
        times = sorted(self.contactData)
        print('Plotting contacts:')
        for i in range(len(times)):
            contactPoints = self.contactPoints(self.contacts, time=times[i])
            self.animationImages[i] += self.axes.plot(contactPoints[0], contactPoints[1], 'k*', label='Boundary Contacts')
        print('\tDone')
        
    def plotCorners(self):
        times = sorted(self.cornerData)
        print('Plotting contacts:')
        for i in range(len(times)):
            cornerPoints = self.cornerPoints(self.corners, time=times[i])
            self.animationImages[i] += self.axes.plot(cornerPoints[0], cornerPoints[1], 'r*', label='Boundary Contacts')
        print('\tDone')
        
    def plotZones(self):        
        times = sorted(self.blockData)
        print('Plotting zone boundaries:')
        for i in range(len(times)):
            zoneEdges = self.zoneEdges(self.zones, time=times[i])
            self.animationImages[i] += self.axes.plot(zoneEdges[0], zoneEdges[1], 'g:', label='Zone Boundaries')
        print('\tDone')
                
    def plotCircle(self, radius, centre, label='Circle', color='r'):
        times = sorted(self.blockData)
        for i in range(len(times)):
            self.animationImages[i].append(self.axes.add_patch(patches.Circle((centre['x'], centre['y']), radius, color=color, fill=False, label=label)))

    def plotLine(self, x, y, label='Line', linestyle='k-', linewidth=2, marker='.', markersize=10):        
        times = sorted(self.blockData)
        for i in range(len(times)):
            self.animationImages[i] += self.axes.plot(x, y, linestyle, label=label, linewidth=linewidth, marker=marker, markersize=markersize)

    def plotBorder(self, shape, label='Border', linestyle='k-', linewidth=1):        
        times = sorted(self.blockData)
        x = [i[0] for i in shape]
        y = [i[1] for i in shape]
        for i in range(len(times)):
            self.animationImages[i] += self.axes.plot(x, y, linestyle, label=label, linewidth=linewidth)
            
            
    # def removeAxes(self):
        # self.axes.get_xaxis().set_visible(False)
        # self.axes.get_yaxis().set_visible(False)
        
    # def removeFrame(self):
        # self.figure.patch.set_visible(False)
        # self.axes.axis('off')
             
            
    def plotZoomBox(self, centre=(0.5, 0.5), zoom=4, label=None, linestyle='g-'):        
        axisLimits = self.limits()    
        xMin = axisLimits[0]
        xMax = axisLimits[1]
        yMin = axisLimits[2]
        yMax = axisLimits[3]
        
        xLen = xMax - xMin
        yLen = yMax - yMin
        
        xCen = centre[0]*xLen + xMin
        yCen = centre[1]*yLen + yMin
        
        xOff = xLen/2/zoom
        yOff = yLen/2/zoom
        
        xMinNew = xCen - xOff
        xMaxNew = xCen + xOff
        yMinNew = yCen - yOff
        yMaxNew = yCen + yOff
        x = [xMinNew, xMaxNew, xMaxNew, xMinNew, xMinNew]
        y = [yMinNew, yMinNew, yMaxNew, yMaxNew, yMinNew]
        
        self.plotLine(x, y, linestyle=linestyle, marker=None, label=label)
            
    def plotStressField(self, stressType, stressLimits='automatic', loadData=True, sigma=1, shape='default', numColors=10):
        times = sorted(self.blockData)
        cmap = plt.cm.viridis
        allX = []
        allY = []
        allZ = []
        filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'binaryData', self.fileName+'_'+stressType+'.dat')
        
        if shape=='default':
            shape = [(0,0), (10,0), (10,10), (0, 10)]
            
        calculate = True
        if loadData == True:
            try:
                print('Attempting to load interpolated {} stress grid from binary:'.format(stressType))
                stressGridTime = os.path.getmtime(filePath)
                compiledDataTime = os.path.getmtime(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'binaryData', self.fileName+'_binary.dat'))
                if stressGridTime > compiledDataTime:
                    allX, allY, allZ = pickle.load(open(filePath, 'rb'))
                    calculate = False
                    print('\tSuccess')
                else:
                    print('\tFailed... Binanry data out of date')
            except:
                print('\tFailed... No binary data found')
        if calculate == True:
            print('Interpolating {} stress grid:'.format(stressType))
            print('\tFor Frame #', end='')
            for i in range(len(times)):
                time = times[i]
                numString = str(i+1)+'/'+str(len(times))
                print(numString, end='')
                print('\b'*len(numString), end='')
                sys.stdout.flush()
                
                S11 = np.array(self.zoneS11(self.zoneData[time].keys(), time))/1e6
                S22 = np.array(self.zoneS22(self.zoneData[time].keys(), time))/1e6
                #S33 = np.array(self.zoneS33(self.zoneData[time].keys(), time))/1e6
                S12 = np.array(self.zoneS12(self.zoneData[time].keys(), time))/1e6
                if stressType == 'S11':
                    stress = S11
                elif stressType == 'S22':
                    stress = S22
                elif stressType == 'S33':
                    stress = S33
                elif stressType == 'S12':
                    stress = S12
                elif stressType == 'mises':
                    stress = np.sqrt(np.divide(np.power(S11-S22, 2) + np.power(S22-S33, 2) + np.power(S33-S11, 2)+6*(S12)))
                elif stressType == 'MaxP':
                    stress = 'blah'
                elif stressType == 'MinP':
                    stress = 'blah'
                elif stressType == 'IntP':
                    stress = 'blah'

                zoneX = []
                zoneY = []
                for zone in self.zoneData[time].keys():
                    gridPoints = self.zoneData[time][zone]['gridPoints']
                    gridPointX = 0
                    gridPointY = 0
                    for gridPoint in gridPoints:
                        gridPointX += self.gridPointData[time][gridPoint]['x']
                        gridPointY += self.gridPointData[time][gridPoint]['y']
                    zoneX.append(gridPointX/len(gridPoints))
                    zoneY.append(gridPointY/len(gridPoints))
                
                cornersX = [x[0] for x in shape]
                cornersY = [x[1] for x in shape]
                X, Y, Z = common.grid(zoneX, zoneY, stress, limits=[min(cornersX), max(cornersX), min(cornersY), max(cornersY)])
                allX.append(X)
                allY.append(Y)
                allZ.append(Z)
            print('')
            print('Saving interpolated {} stress grid to binary:'.format(stressType))
            pickle.dump([allX, allY, allZ], open(filePath, 'wb'))
            print('\tDone')

        if stressLimits == 'automatic':
            print('Assessing {} stress limits:'.format(stressType))
            zmin = min([min([num for num in list(frame.flatten()) if isinstance(num, float)]) for frame in allZ])
            zmax = max([max([num for num in list(frame.flatten()) if isinstance(num, float)]) for frame in allZ])
            print('\tDone')
        else:
            zmin = stressLimits[0]
            zmax = stressLimits[1]
        
        print('Smoothing {} stress field:'.format(stressType))
        print('\tFor Frame #', end='')

        for i in range(len(times)):
            numString = str(i+1)+'/'+str(len(times))
            print(numString, end='')
            print('\b'*len(numString), end='')
            sys.stdout.flush()
            time = times[i]
            X = allX[i]         
            Y = allY[i]
            Z = allZ[i]
            Z = gaussian_filter(Z, sigma)
            
            bbPath = mplPath.Path(np.array(shape))
            for j in range(len(X)):
                for k in range(len(X[j])):
                    if bbPath.contains_point((X[j,k], Y[j,k])) == False:
                        Z[j,k] = np.NaN
            for j in range(len(shape)-1):
                if shape[j][0] - shape[j+1][0] == 0 or shape[j][1] - shape[j+1][1] == 0:
                    pass
                else:
                    
                    for k in range(len(Y)):
                        row = list(Z[k])
                        edgeIndex = len(row)
                        for l in range(len(row)):
                            if str(row[l]) == str(np.NaN):
                                edgeIndex = l+1
                        if edgeIndex < len(row):
                            X[k, edgeIndex] = np.interp(Y[k, edgeIndex], [shape[j+1][1], shape[j][1]], [shape[j+1][0], shape[j][0]])
            
            im = self.axes.contourf(X, Y, Z, numColors, cmap=cmap, vmin=zmin, vmax=zmax, origin='lower')
            self.animationImages[i] += im.collections

        print('\nPlotting {} stress field:'.format(stressType))
        bounds = np.linspace(0,numColors,numColors+1)
        scaleLength = zmax-zmin
        bounds = bounds * scaleLength / (len(bounds)-1)+ zmin
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
        self.colorBar = colorbar.ColorbarBase(self.colorBarAxes, cmap=cmap, norm=norm)
        self.colorBar.set_label('MPa')
        print('\tDone')
        

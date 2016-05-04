#!/usr/bin/env python3
import pickle
from parameters import *
import numpy
from scipy.interpolate import griddata
import sys  
import os

def interpolateData(binaryDataFile):
    file = open(binaryDataFile, 'rb')
    if os.name == 'nt':
        rawTimeHistory = numpy.array(pickle.load(file, encoding='latin1')).transpose()
        rawStressHistory = numpy.array(pickle.load(file, encoding='latin1')).transpose()
        rawStrainHistory = numpy.array(pickle.load(file, encoding='latin1')).transpose()
    elif os.name == 'posix':
        rawTimeHistory = numpy.array(pickle.load(file)).transpose()
        rawStressHistory = numpy.array(pickle.load(file)).transpose()
        rawStrainHistory = numpy.array(pickle.load(file)).transpose()
    
    timeHistory = numpy.linspace(0, simulationTime, numberOfSteps+1)
    stressHistory = numpy.empty([3, numberOfSteps+1]);
    strainHistory = numpy.empty([3, numberOfSteps+1]);
    for i in range(3):
        stressHistory[i, :] = griddata(rawTimeHistory, rawStressHistory[i], timeHistory)
        strainHistory[i, :] = griddata(rawTimeHistory, rawStrainHistory[i], timeHistory)
    stressHistory = stressHistory.transpose()
    strainHistory = strainHistory.transpose()
    
    with open('output.dat', 'w') as f:
        f.write('time S11 S22 S12 LE11 LE22 LE12\n')
        for i in range(len(timeHistory)):
            f.write(str(timeHistory[i])+' ')
            for j in range(len(stressHistory[i])):
                f.write(str(stressHistory[i][j])+' ')
            for j in range(len(strainHistory[i])):
                f.write(str(strainHistory[i][j])+' ')
            f.write('\n')
            
    bundle = [timeHistory, stressHistory, strainHistory]
    bundleFileName = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'fittedHistory', sName+'_fittedHistory.pkl')
    # ostModelFileName = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'OstModel0.txt')
    # newSet = False
    # try:
        # with open(ostModelFileName, 'r') as trialsFile:
            # text = trialsFile.readlines()
            # if len(text) <=2:
                # newSet = True
    # except FileNotFoundError:
        # newSet = True
    # if newSet is False:
    # elif newSet is True:
        # with open(bundleFileName, 'wb') as fittedFile:
             # pickle.dump(bundle, fittedFile)
    with open(bundleFileName, 'ab') as fittedFile:
        pickle.dump(bundle, fittedFile)           
       
    
def main():
    interpolateData(os.path.join(os.getcwd(), 'rawHistory.pkl'))
    
if __name__ == '__main__':            
    main()

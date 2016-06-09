import os
import sys

print('*'*70)
print('Compiling UDEC Data Files')
print('*'*70)

print('Getting list of files in data directory...')
path = 'UpFracDEMData'
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
print('\tDone')

print('Isolating files for compilation...')
simulations = []
for file in files:
    index = file.rfind('.')
    simulationName = file[:index]
    extension = file[index+1:]
    if 'dat' in extension and len(extension) > 3:
        simulations.append(simulationName)
simulations = list(set(simulations))
simulations.sort()
print('\tDone')

print('Compiling data files for...')
for simulation in simulations:
    print('\t{0}...'.format(simulation), end='')
    sys.stdout.flush()
    simulationFiles = []
    for file in files:
        if 'dat' not in str(file[-3:]) and simulation in file:
            simulationFiles.append(file)
    with open(os.path.join(path, '{0}.dat'.format(simulation)), 'w') as fout:
        with open(os.path.join(path, simulationFiles[0]), 'r') as fin:
            fout.writelines(fin.readlines()[:2])
        for simulationFile in simulationFiles:
            with open(os.path.join(path, simulationFile), 'r') as fin:
                fout.writelines(fin.readlines()[2:])
    print('Done')    

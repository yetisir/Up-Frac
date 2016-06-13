topText = """#Configuration File for Ostrich Program
#ProgramType Levenberg-Marquardt
#ProgramType GeneticAlgorithm
#ProgramType PSO-GM
ProgramType ParticleSwarm

BeginFilePairs    
runAbaqus.temp.tpl	runAbaqus.py
EndFilePairs

ModelExecutable    simulationData.bat

ModelSubdir model

#Parameter Specification
BeginParams
#parameter	init.	low	    high	tx_in   tx_ost	tx_out
$$ostrichParameters
EndParams

#Observation Configuration
BeginObservations
#observation	value		weight	file		keyword		line	column
"""

bottomText = """
EndObservations

#Configuration for Levenberg-Marquardt algorithm
BeginLevMar
InitialLambda    10.0
LambdaScaleFactor    1.1
MoveLimit    0.1
AlgorithmConvergenceValue    0.01
LambdaPhiRatio    0.3
LambdaRelReduction    0.01
MaxLambdas    10
MaxIterations    20
EndLevMar

BeginMathAndStats
#DiffType    forward
#DiffRelIncrement    0.1
Default
#AllStats
#NoStats
#StdDev
#StdErr
#CorrCoeff
#Beale
#Linssen
#CooksD
#DFBETAS
#Confidence
#Sensitivity
EndMathAndStats

BeginExtraFiles
parameters.py
interpolateData.py
simulationData.py
vectorMath.py
jclean.bat
EndExtraFiles

BeginParticleSwarm
SwarmSize  24
NumGenerations  50
EndParticleSwarm

#BeginGeneticAlg
#PopulationSize 10
#MutationRate 0.05
#Survivors 1
#NumGenerations 50
#EndGeneticAlg"""

#Configuration File for Ostrich Program
ProgramType Levenberg-Marquardt
#ProgramType GeneticAlgorithm

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
obs1 		-2485425.088656 	1 	output.dat 	OST_NULL 	2 		3
obs2 		-3590896.637641 	1 	output.dat 	OST_NULL 	3 		3
obs3 		-4393074.412992 	1 	output.dat 	OST_NULL 	4 		3
obs4 		-5062913.521243 	1 	output.dat 	OST_NULL 	5 		3
obs5 		-5706079.755838 	1 	output.dat 	OST_NULL 	6 		3
obs6 		-6286673.570164 	1 	output.dat 	OST_NULL 	7 		3
obs7 		-6687907.077596 	1 	output.dat 	OST_NULL 	8 		3
obs8 		-7076626.005211 	1 	output.dat 	OST_NULL 	9 		3
obs9 		-7392863.894017 	1 	output.dat 	OST_NULL 	10 		3
obs10 		-7755356.350301 	1 	output.dat 	OST_NULL 	11 		3
obs11 		-8094267.970640 	1 	output.dat 	OST_NULL 	12 		3
obs12 		-8447415.341542 	1 	output.dat 	OST_NULL 	13 		3
obs13 		-8799095.177970 	1 	output.dat 	OST_NULL 	14 		3
obs14 		-8888994.584206 	1 	output.dat 	OST_NULL 	15 		3
obs15 		-9097291.687539 	1 	output.dat 	OST_NULL 	16 		3
obs16 		-9263381.326697 	1 	output.dat 	OST_NULL 	17 		3
obs17 		-9387978.734350 	1 	output.dat 	OST_NULL 	18 		3
obs18 		-9456519.067824 	1 	output.dat 	OST_NULL 	19 		3
obs19 		-9701678.500610 	1 	output.dat 	OST_NULL 	20 		3
obs20 		-9642177.635756 	1 	output.dat 	OST_NULL 	21 		3
obs21 		-9567692.057115 	1 	output.dat 	OST_NULL 	22 		3
obs22 		-9032461.531387 	1 	output.dat 	OST_NULL 	23 		3
obs23 		-8301834.918829 	1 	output.dat 	OST_NULL 	24 		3
obs24 		-7397909.979233 	1 	output.dat 	OST_NULL 	25 		3
obs25 		-6596900.473325 	1 	output.dat 	OST_NULL 	26 		3
obs26 		-5927306.680218 	1 	output.dat 	OST_NULL 	27 		3
obs27 		-5207842.801124 	1 	output.dat 	OST_NULL 	28 		3
obs28 		-4496037.782152 	1 	output.dat 	OST_NULL 	29 		3
obs29 		-3705240.789346 	1 	output.dat 	OST_NULL 	30 		3
obs30 		-2860328.104179 	1 	output.dat 	OST_NULL 	31 		3
obs31 		-2150909.830364 	1 	output.dat 	OST_NULL 	32 		3
obs32 		-1476353.226779 	1 	output.dat 	OST_NULL 	33 		3
obs33 		-1072442.588872 	1 	output.dat 	OST_NULL 	34 		3
obs34 		-771104.107505 	1 	output.dat 	OST_NULL 	35 		3
obs35 		-564386.599145 	1 	output.dat 	OST_NULL 	36 		3
obs36 		-375665.663553 	1 	output.dat 	OST_NULL 	37 		3
obs37 		-261847.552574 	1 	output.dat 	OST_NULL 	38 		3
obs38 		-188202.768732 	1 	output.dat 	OST_NULL 	39 		3
obs39 		-141683.056893 	1 	output.dat 	OST_NULL 	40 		3
obs40 		-95775.884947 	1 	output.dat 	OST_NULL 	41 		3
obs41 		-76132.268804 	1 	output.dat 	OST_NULL 	42 		3
obs42 		-60709.515680 	1 	output.dat 	OST_NULL 	43 		3
obs43 		-48672.464695 	1 	output.dat 	OST_NULL 	44 		3
obs44 		-39841.665191 	1 	output.dat 	OST_NULL 	45 		3
obs45 		-32623.869244 	1 	output.dat 	OST_NULL 	46 		3
obs46 		-26336.662647 	1 	output.dat 	OST_NULL 	47 		3
obs47 		-21643.960427 	1 	output.dat 	OST_NULL 	48 		3
obs48 		-17814.742402 	1 	output.dat 	OST_NULL 	49 		3
obs49 		-14610.785152 	1 	output.dat 	OST_NULL 	50 		3
obs50 		-12024.682060 	1 	output.dat 	OST_NULL 	51 		3

EndObservations

#Configuration for Levenberg-Marquardt algorithm
BeginLevMar
InitialLambda    10.0
LambdaScaleFactor    1.1
MoveLimit    0.1
AlgorithmConvergenceValue    0.0001
LambdaPhiRatio    0.3
LambdaRelReduction    0.01
MaxLambdas    10
MaxIterations    20
EndLevMar

BeginMathAndStats
DiffType    forward
DiffRelIncrement    0.01
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
EndExtraFiles

BeginGeneticAlg
PopulationSize 10
MutationRate 0.05
Survivors 1
NumGenerations 50
EndGeneticAlg
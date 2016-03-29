#Configuration File for Ostrich Program
ProgramType Levenberg-Marquardt
#ProgramType GeneticAlgorithm

BeginFilePairs    
parameters.tpl	parameters.py
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
obs1 		240460.888903 	1 	output.dat 	OST_NULL 	2 		3
obs2 		460785.282543 	1 	output.dat 	OST_NULL 	3 		3
obs3 		680037.687383 	1 	output.dat 	OST_NULL 	4 		3
obs4 		885816.840642 	1 	output.dat 	OST_NULL 	5 		3
obs5 		1093638.214501 	1 	output.dat 	OST_NULL 	6 		3
obs6 		1251312.145016 	1 	output.dat 	OST_NULL 	7 		3
obs7 		1435598.503897 	1 	output.dat 	OST_NULL 	8 		3
obs8 		1570954.154158 	1 	output.dat 	OST_NULL 	9 		3
obs9 		1724503.216477 	1 	output.dat 	OST_NULL 	10 		3
obs10 		1894479.900938 	1 	output.dat 	OST_NULL 	11 		3
obs11 		1910957.269478 	1 	output.dat 	OST_NULL 	12 		3
obs12 		1901588.512282 	1 	output.dat 	OST_NULL 	13 		3
obs13 		1765071.809928 	1 	output.dat 	OST_NULL 	14 		3
obs14 		1846769.099276 	1 	output.dat 	OST_NULL 	15 		3
obs15 		1934005.986044 	1 	output.dat 	OST_NULL 	16 		3
obs16 		1405684.858017 	1 	output.dat 	OST_NULL 	17 		3
obs17 		1255141.111437 	1 	output.dat 	OST_NULL 	18 		3
obs18 		1208142.295099 	1 	output.dat 	OST_NULL 	19 		3
obs19 		1254353.160573 	1 	output.dat 	OST_NULL 	20 		3
obs20 		1175551.923460 	1 	output.dat 	OST_NULL 	21 		3
obs21 		1111291.771143 	1 	output.dat 	OST_NULL 	22 		3
obs22 		1137064.938881 	1 	output.dat 	OST_NULL 	23 		3
obs23 		1137791.955999 	1 	output.dat 	OST_NULL 	24 		3
obs24 		1155747.412723 	1 	output.dat 	OST_NULL 	25 		3
obs25 		1161296.158585 	1 	output.dat 	OST_NULL 	26 		3
obs26 		1154100.581083 	1 	output.dat 	OST_NULL 	27 		3
obs27 		1130612.846068 	1 	output.dat 	OST_NULL 	28 		3
obs28 		1093480.522889 	1 	output.dat 	OST_NULL 	29 		3
obs29 		1042932.797770 	1 	output.dat 	OST_NULL 	30 		3
obs30 		977848.196755 	1 	output.dat 	OST_NULL 	31 		3
obs31 		906544.303871 	1 	output.dat 	OST_NULL 	32 		3
obs32 		835956.645854 	1 	output.dat 	OST_NULL 	33 		3
obs33 		765736.113688 	1 	output.dat 	OST_NULL 	34 		3
obs34 		696338.652681 	1 	output.dat 	OST_NULL 	35 		3
obs35 		626286.448495 	1 	output.dat 	OST_NULL 	36 		3
obs36 		559548.344599 	1 	output.dat 	OST_NULL 	37 		3
obs37 		492992.913659 	1 	output.dat 	OST_NULL 	38 		3
obs38 		425695.228972 	1 	output.dat 	OST_NULL 	39 		3
obs39 		360644.223755 	1 	output.dat 	OST_NULL 	40 		3
obs40 		295131.282716 	1 	output.dat 	OST_NULL 	41 		3
obs41 		227085.209149 	1 	output.dat 	OST_NULL 	42 		3
obs42 		168864.982740 	1 	output.dat 	OST_NULL 	43 		3
obs43 		100512.408313 	1 	output.dat 	OST_NULL 	44 		3
obs44 		68327.133051 	1 	output.dat 	OST_NULL 	45 		3
obs45 		-1708.960430 	1 	output.dat 	OST_NULL 	46 		3
obs46 		-73719.979703 	1 	output.dat 	OST_NULL 	47 		3
obs47 		-141733.947282 	1 	output.dat 	OST_NULL 	48 		3
obs48 		-220444.214614 	1 	output.dat 	OST_NULL 	49 		3
obs49 		-297386.199757 	1 	output.dat 	OST_NULL 	50 		3
obs50 		-381183.278704 	1 	output.dat 	OST_NULL 	51 		3

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
runAbaqus.py
interpolateData.py
simulationData.py
EndExtraFiles

BeginGeneticAlg
PopulationSize 10
MutationRate 0.05
Survivors 1
NumGenerations 50
EndGeneticAlg
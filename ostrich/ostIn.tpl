#Configuration File for Ostrich Program
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
obs1 		-4239066.125916 	1 	output.dat 	OST_NULL 	2 		3
obs2 		 -0.000387 	1 	output.dat 	OST_NULL 	2 		6
obs3 		-6409183.264753 	1 	output.dat 	OST_NULL 	3 		3
obs4 		 -0.000790 	1 	output.dat 	OST_NULL 	3 		6
obs5 		-7586702.343118 	1 	output.dat 	OST_NULL 	4 		3
obs6 		 -0.001174 	1 	output.dat 	OST_NULL 	4 		6
obs7 		-8767813.907269 	1 	output.dat 	OST_NULL 	5 		3
obs8 		 -0.001552 	1 	output.dat 	OST_NULL 	5 		6
obs9 		-9639833.166380 	1 	output.dat 	OST_NULL 	6 		3
obs10 		 -0.001913 	1 	output.dat 	OST_NULL 	6 		6
obs11 		-10139271.222076 	1 	output.dat 	OST_NULL 	7 		3
obs12 		 -0.002303 	1 	output.dat 	OST_NULL 	7 		6
obs13 		-10555826.407938 	1 	output.dat 	OST_NULL 	8 		3
obs14 		 -0.002694 	1 	output.dat 	OST_NULL 	8 		6
obs15 		-10978869.141169 	1 	output.dat 	OST_NULL 	9 		3
obs16 		 -0.003065 	1 	output.dat 	OST_NULL 	9 		6
obs17 		-11436590.227779 	1 	output.dat 	OST_NULL 	10 		3
obs18 		 -0.003437 	1 	output.dat 	OST_NULL 	10 		6
obs19 		-11265104.945073 	1 	output.dat 	OST_NULL 	11 		3
obs20 		 -0.003791 	1 	output.dat 	OST_NULL 	11 		6
obs21 		-11748101.753196 	1 	output.dat 	OST_NULL 	12 		3
obs22 		 -0.004157 	1 	output.dat 	OST_NULL 	12 		6
obs23 		-11959882.855808 	1 	output.dat 	OST_NULL 	13 		3
obs24 		 -0.004548 	1 	output.dat 	OST_NULL 	13 		6
obs25 		-12050492.478525 	1 	output.dat 	OST_NULL 	14 		3
obs26 		 -0.004959 	1 	output.dat 	OST_NULL 	14 		6
obs27 		-12282835.778080 	1 	output.dat 	OST_NULL 	15 		3
obs28 		 -0.005338 	1 	output.dat 	OST_NULL 	15 		6
obs29 		-12673684.409836 	1 	output.dat 	OST_NULL 	16 		3
obs30 		 -0.005719 	1 	output.dat 	OST_NULL 	16 		6
obs31 		-12951772.919702 	1 	output.dat 	OST_NULL 	17 		3
obs32 		 -0.006067 	1 	output.dat 	OST_NULL 	17 		6
obs33 		-13306592.261911 	1 	output.dat 	OST_NULL 	18 		3
obs34 		 -0.006396 	1 	output.dat 	OST_NULL 	18 		6
obs35 		-13580525.390872 	1 	output.dat 	OST_NULL 	19 		3
obs36 		 -0.006751 	1 	output.dat 	OST_NULL 	19 		6
obs37 		-13749969.477900 	1 	output.dat 	OST_NULL 	20 		3
obs38 		 -0.007107 	1 	output.dat 	OST_NULL 	20 		6
obs39 		-14064961.189465 	1 	output.dat 	OST_NULL 	21 		3
obs40 		 -0.007467 	1 	output.dat 	OST_NULL 	21 		6
obs41 		-13981662.602545 	1 	output.dat 	OST_NULL 	22 		3
obs42 		 -0.007793 	1 	output.dat 	OST_NULL 	22 		6
obs43 		-13092355.979852 	1 	output.dat 	OST_NULL 	23 		3
obs44 		 -0.008030 	1 	output.dat 	OST_NULL 	23 		6
obs45 		-12215035.892109 	1 	output.dat 	OST_NULL 	24 		3
obs46 		 -0.008191 	1 	output.dat 	OST_NULL 	24 		6
obs47 		-11305372.801854 	1 	output.dat 	OST_NULL 	25 		3
obs48 		 -0.008338 	1 	output.dat 	OST_NULL 	25 		6
obs49 		-10268432.017643 	1 	output.dat 	OST_NULL 	26 		3
obs50 		 -0.008338 	1 	output.dat 	OST_NULL 	26 		6
obs51 		-9241965.048071 	1 	output.dat 	OST_NULL 	27 		3
obs52 		 -0.008281 	1 	output.dat 	OST_NULL 	27 		6
obs53 		-8212450.162771 	1 	output.dat 	OST_NULL 	28 		3
obs54 		 -0.008175 	1 	output.dat 	OST_NULL 	28 		6
obs55 		-6989698.485177 	1 	output.dat 	OST_NULL 	29 		3
obs56 		 -0.007983 	1 	output.dat 	OST_NULL 	29 		6
obs57 		-5808533.500225 	1 	output.dat 	OST_NULL 	30 		3
obs58 		 -0.007722 	1 	output.dat 	OST_NULL 	30 		6
obs59 		-4506678.201743 	1 	output.dat 	OST_NULL 	31 		3
obs60 		 -0.007398 	1 	output.dat 	OST_NULL 	31 		6
obs61 		-3297429.952544 	1 	output.dat 	OST_NULL 	32 		3
obs62 		 -0.006972 	1 	output.dat 	OST_NULL 	32 		6
obs63 		-2274680.011437 	1 	output.dat 	OST_NULL 	33 		3
obs64 		 -0.006552 	1 	output.dat 	OST_NULL 	33 		6
obs65 		-1333071.183245 	1 	output.dat 	OST_NULL 	34 		3
obs66 		 -0.006104 	1 	output.dat 	OST_NULL 	34 		6
obs67 		-824596.291907 	1 	output.dat 	OST_NULL 	35 		3
obs68 		 -0.005727 	1 	output.dat 	OST_NULL 	35 		6
obs69 		-387080.707111 	1 	output.dat 	OST_NULL 	36 		3
obs70 		 -0.005408 	1 	output.dat 	OST_NULL 	36 		6
obs71 		-62235.557561 	1 	output.dat 	OST_NULL 	37 		3
obs72 		 -0.005116 	1 	output.dat 	OST_NULL 	37 		6
obs73 		189349.439395 	1 	output.dat 	OST_NULL 	38 		3
obs74 		 -0.004773 	1 	output.dat 	OST_NULL 	38 		6
obs75 		197534.000072 	1 	output.dat 	OST_NULL 	39 		3
obs76 		 -0.004396 	1 	output.dat 	OST_NULL 	39 		6
obs77 		240160.229664 	1 	output.dat 	OST_NULL 	40 		3
obs78 		 -0.004039 	1 	output.dat 	OST_NULL 	40 		6
obs79 		280239.524811 	1 	output.dat 	OST_NULL 	41 		3
obs80 		 -0.003671 	1 	output.dat 	OST_NULL 	41 		6
obs81 		307326.479233 	1 	output.dat 	OST_NULL 	42 		3
obs82 		 -0.003329 	1 	output.dat 	OST_NULL 	42 		6
obs83 		273195.179260 	1 	output.dat 	OST_NULL 	43 		3
obs84 		 -0.002965 	1 	output.dat 	OST_NULL 	43 		6
obs85 		192437.294384 	1 	output.dat 	OST_NULL 	44 		3
obs86 		 -0.002605 	1 	output.dat 	OST_NULL 	44 		6
obs87 		203110.205437 	1 	output.dat 	OST_NULL 	45 		3
obs88 		 -0.002259 	1 	output.dat 	OST_NULL 	45 		6
obs89 		182799.863342 	1 	output.dat 	OST_NULL 	46 		3
obs90 		 -0.001899 	1 	output.dat 	OST_NULL 	46 		6
obs91 		192815.911381 	1 	output.dat 	OST_NULL 	47 		3
obs92 		 -0.001550 	1 	output.dat 	OST_NULL 	47 		6
obs93 		173519.792498 	1 	output.dat 	OST_NULL 	48 		3
obs94 		 -0.001200 	1 	output.dat 	OST_NULL 	48 		6
obs95 		188995.213352 	1 	output.dat 	OST_NULL 	49 		3
obs96 		 -0.000850 	1 	output.dat 	OST_NULL 	49 		6
obs97 		188425.577568 	1 	output.dat 	OST_NULL 	50 		3
obs98 		 -0.000536 	1 	output.dat 	OST_NULL 	50 		6
obs99 		99077.954184 	1 	output.dat 	OST_NULL 	51 		3
obs100 		 -0.000227 	1 	output.dat 	OST_NULL 	51 		6
obs101 		-7230298.386940 	1 	output.dat 	OST_NULL 	53 		3
obs102 		 -0.000394 	1 	output.dat 	OST_NULL 	53 		6
obs103 		-11327691.137381 	1 	output.dat 	OST_NULL 	54 		3
obs104 		 -0.000784 	1 	output.dat 	OST_NULL 	54 		6
obs105 		-14766898.828761 	1 	output.dat 	OST_NULL 	55 		3
obs106 		 -0.001176 	1 	output.dat 	OST_NULL 	55 		6
obs107 		-17344599.035100 	1 	output.dat 	OST_NULL 	56 		3
obs108 		 -0.001567 	1 	output.dat 	OST_NULL 	56 		6
obs109 		-19228685.969619 	1 	output.dat 	OST_NULL 	57 		3
obs110 		 -0.001956 	1 	output.dat 	OST_NULL 	57 		6
obs111 		-20976687.030303 	1 	output.dat 	OST_NULL 	58 		3
obs112 		 -0.002330 	1 	output.dat 	OST_NULL 	58 		6
obs113 		-22737931.513959 	1 	output.dat 	OST_NULL 	59 		3
obs114 		 -0.002719 	1 	output.dat 	OST_NULL 	59 		6
obs115 		-24282735.577730 	1 	output.dat 	OST_NULL 	60 		3
obs116 		 -0.003110 	1 	output.dat 	OST_NULL 	60 		6
obs117 		-25655313.475998 	1 	output.dat 	OST_NULL 	61 		3
obs118 		 -0.003502 	1 	output.dat 	OST_NULL 	61 		6
obs119 		-27138861.983223 	1 	output.dat 	OST_NULL 	62 		3
obs120 		 -0.003881 	1 	output.dat 	OST_NULL 	62 		6
obs121 		-28148949.887778 	1 	output.dat 	OST_NULL 	63 		3
obs122 		 -0.004269 	1 	output.dat 	OST_NULL 	63 		6
obs123 		-29361902.566941 	1 	output.dat 	OST_NULL 	64 		3
obs124 		 -0.004653 	1 	output.dat 	OST_NULL 	64 		6
obs125 		-30389669.035378 	1 	output.dat 	OST_NULL 	65 		3
obs126 		 -0.005028 	1 	output.dat 	OST_NULL 	65 		6
obs127 		-31661379.883687 	1 	output.dat 	OST_NULL 	66 		3
obs128 		 -0.005412 	1 	output.dat 	OST_NULL 	66 		6
obs129 		-32430452.021661 	1 	output.dat 	OST_NULL 	67 		3
obs130 		 -0.005796 	1 	output.dat 	OST_NULL 	67 		6
obs131 		-33166920.197767 	1 	output.dat 	OST_NULL 	68 		3
obs132 		 -0.006175 	1 	output.dat 	OST_NULL 	68 		6
obs133 		-34117885.183491 	1 	output.dat 	OST_NULL 	69 		3
obs134 		 -0.006554 	1 	output.dat 	OST_NULL 	69 		6
obs135 		-34801572.176260 	1 	output.dat 	OST_NULL 	70 		3
obs136 		 -0.006939 	1 	output.dat 	OST_NULL 	70 		6
obs137 		-35805903.335633 	1 	output.dat 	OST_NULL 	71 		3
obs138 		 -0.007302 	1 	output.dat 	OST_NULL 	71 		6
obs139 		-36627572.237733 	1 	output.dat 	OST_NULL 	72 		3
obs140 		 -0.007683 	1 	output.dat 	OST_NULL 	72 		6
obs141 		-37236220.697700 	1 	output.dat 	OST_NULL 	73 		3
obs142 		 -0.008032 	1 	output.dat 	OST_NULL 	73 		6
obs143 		-37372571.488457 	1 	output.dat 	OST_NULL 	74 		3
obs144 		 -0.008293 	1 	output.dat 	OST_NULL 	74 		6
obs145 		-37249708.225029 	1 	output.dat 	OST_NULL 	75 		3
obs146 		 -0.008481 	1 	output.dat 	OST_NULL 	75 		6
obs147 		-37118240.802294 	1 	output.dat 	OST_NULL 	76 		3
obs148 		 -0.008596 	1 	output.dat 	OST_NULL 	76 		6
obs149 		-36616534.052217 	1 	output.dat 	OST_NULL 	77 		3
obs150 		 -0.008646 	1 	output.dat 	OST_NULL 	77 		6
obs151 		-35977848.026128 	1 	output.dat 	OST_NULL 	78 		3
obs152 		 -0.008611 	1 	output.dat 	OST_NULL 	78 		6
obs153 		-35184209.846559 	1 	output.dat 	OST_NULL 	79 		3
obs154 		 -0.008496 	1 	output.dat 	OST_NULL 	79 		6
obs155 		-34178030.111949 	1 	output.dat 	OST_NULL 	80 		3
obs156 		 -0.008303 	1 	output.dat 	OST_NULL 	80 		6
obs157 		-32921776.458135 	1 	output.dat 	OST_NULL 	81 		3
obs158 		 -0.008032 	1 	output.dat 	OST_NULL 	81 		6
obs159 		-31456183.103680 	1 	output.dat 	OST_NULL 	82 		3
obs160 		 -0.007685 	1 	output.dat 	OST_NULL 	82 		6
obs161 		-30057361.932410 	1 	output.dat 	OST_NULL 	83 		3
obs162 		 -0.007301 	1 	output.dat 	OST_NULL 	83 		6
obs163 		-28745287.778778 	1 	output.dat 	OST_NULL 	84 		3
obs164 		 -0.006913 	1 	output.dat 	OST_NULL 	84 		6
obs165 		-27487903.454246 	1 	output.dat 	OST_NULL 	85 		3
obs166 		 -0.006527 	1 	output.dat 	OST_NULL 	85 		6
obs167 		-26236229.662395 	1 	output.dat 	OST_NULL 	86 		3
obs168 		 -0.006136 	1 	output.dat 	OST_NULL 	86 		6
obs169 		-24956805.590237 	1 	output.dat 	OST_NULL 	87 		3
obs170 		 -0.005745 	1 	output.dat 	OST_NULL 	87 		6
obs171 		-23669664.250532 	1 	output.dat 	OST_NULL 	88 		3
obs172 		 -0.005356 	1 	output.dat 	OST_NULL 	88 		6
obs173 		-22408191.445866 	1 	output.dat 	OST_NULL 	89 		3
obs174 		 -0.004971 	1 	output.dat 	OST_NULL 	89 		6
obs175 		-21152062.690549 	1 	output.dat 	OST_NULL 	90 		3
obs176 		 -0.004588 	1 	output.dat 	OST_NULL 	90 		6
obs177 		-19865896.778549 	1 	output.dat 	OST_NULL 	91 		3
obs178 		 -0.004201 	1 	output.dat 	OST_NULL 	91 		6
obs179 		-18487642.028310 	1 	output.dat 	OST_NULL 	92 		3
obs180 		 -0.003815 	1 	output.dat 	OST_NULL 	92 		6
obs181 		-17074822.264469 	1 	output.dat 	OST_NULL 	93 		3
obs182 		 -0.003433 	1 	output.dat 	OST_NULL 	93 		6
obs183 		-15624609.023571 	1 	output.dat 	OST_NULL 	94 		3
obs184 		 -0.003052 	1 	output.dat 	OST_NULL 	94 		6
obs185 		-14197833.333776 	1 	output.dat 	OST_NULL 	95 		3
obs186 		 -0.002669 	1 	output.dat 	OST_NULL 	95 		6
obs187 		-12789929.671891 	1 	output.dat 	OST_NULL 	96 		3
obs188 		 -0.002289 	1 	output.dat 	OST_NULL 	96 		6
obs189 		-11381603.724776 	1 	output.dat 	OST_NULL 	97 		3
obs190 		 -0.001911 	1 	output.dat 	OST_NULL 	97 		6
obs191 		-9956095.042137 	1 	output.dat 	OST_NULL 	98 		3
obs192 		 -0.001529 	1 	output.dat 	OST_NULL 	98 		6
obs193 		-8372296.162141 	1 	output.dat 	OST_NULL 	99 		3
obs194 		 -0.001146 	1 	output.dat 	OST_NULL 	99 		6
obs195 		-6682538.934536 	1 	output.dat 	OST_NULL 	100 		3
obs196 		 -0.000770 	1 	output.dat 	OST_NULL 	100 		6
obs197 		-4693234.203367 	1 	output.dat 	OST_NULL 	101 		3
obs198 		 -0.000395 	1 	output.dat 	OST_NULL 	101 		6
obs199 		-1891796.613358 	1 	output.dat 	OST_NULL 	102 		3
obs200 		 -0.000010 	1 	output.dat 	OST_NULL 	102 		6
obs201 		-9797112.853158 	1 	output.dat 	OST_NULL 	104 		3
obs202 		 -0.000397 	1 	output.dat 	OST_NULL 	104 		6
obs203 		-14245992.456874 	1 	output.dat 	OST_NULL 	105 		3
obs204 		 -0.000790 	1 	output.dat 	OST_NULL 	105 		6
obs205 		-18353808.209478 	1 	output.dat 	OST_NULL 	106 		3
obs206 		 -0.001181 	1 	output.dat 	OST_NULL 	106 		6
obs207 		-22056693.663280 	1 	output.dat 	OST_NULL 	107 		3
obs208 		 -0.001572 	1 	output.dat 	OST_NULL 	107 		6
obs209 		-25213957.926210 	1 	output.dat 	OST_NULL 	108 		3
obs210 		 -0.001967 	1 	output.dat 	OST_NULL 	108 		6
obs211 		-27914334.043532 	1 	output.dat 	OST_NULL 	109 		3
obs212 		 -0.002358 	1 	output.dat 	OST_NULL 	109 		6
obs213 		-29997244.370046 	1 	output.dat 	OST_NULL 	110 		3
obs214 		 -0.002745 	1 	output.dat 	OST_NULL 	110 		6
obs215 		-32049328.603346 	1 	output.dat 	OST_NULL 	111 		3
obs216 		 -0.003125 	1 	output.dat 	OST_NULL 	111 		6
obs217 		-34120151.842684 	1 	output.dat 	OST_NULL 	112 		3
obs218 		 -0.003512 	1 	output.dat 	OST_NULL 	112 		6
obs219 		-36029272.574804 	1 	output.dat 	OST_NULL 	113 		3
obs220 		 -0.003901 	1 	output.dat 	OST_NULL 	113 		6
obs221 		-37850831.098771 	1 	output.dat 	OST_NULL 	114 		3
obs222 		 -0.004293 	1 	output.dat 	OST_NULL 	114 		6
obs223 		-39711545.345871 	1 	output.dat 	OST_NULL 	115 		3
obs224 		 -0.004682 	1 	output.dat 	OST_NULL 	115 		6
obs225 		-41459260.818258 	1 	output.dat 	OST_NULL 	116 		3
obs226 		 -0.005063 	1 	output.dat 	OST_NULL 	116 		6
obs227 		-43100439.459560 	1 	output.dat 	OST_NULL 	117 		3
obs228 		 -0.005450 	1 	output.dat 	OST_NULL 	117 		6
obs229 		-44408474.018369 	1 	output.dat 	OST_NULL 	118 		3
obs230 		 -0.005833 	1 	output.dat 	OST_NULL 	118 		6
obs231 		-45915154.606167 	1 	output.dat 	OST_NULL 	119 		3
obs232 		 -0.006217 	1 	output.dat 	OST_NULL 	119 		6
obs233 		-47033683.510120 	1 	output.dat 	OST_NULL 	120 		3
obs234 		 -0.006589 	1 	output.dat 	OST_NULL 	120 		6
obs235 		-48262371.767990 	1 	output.dat 	OST_NULL 	121 		3
obs236 		 -0.006974 	1 	output.dat 	OST_NULL 	121 		6
obs237 		-49515320.723772 	1 	output.dat 	OST_NULL 	122 		3
obs238 		 -0.007363 	1 	output.dat 	OST_NULL 	122 		6
obs239 		-50465969.786699 	1 	output.dat 	OST_NULL 	123 		3
obs240 		 -0.007751 	1 	output.dat 	OST_NULL 	123 		6
obs241 		-51294483.913514 	1 	output.dat 	OST_NULL 	124 		3
obs242 		 -0.008091 	1 	output.dat 	OST_NULL 	124 		6
obs243 		-51604692.366941 	1 	output.dat 	OST_NULL 	125 		3
obs244 		 -0.008360 	1 	output.dat 	OST_NULL 	125 		6
obs245 		-51711317.273508 	1 	output.dat 	OST_NULL 	126 		3
obs246 		 -0.008548 	1 	output.dat 	OST_NULL 	126 		6
obs247 		-51701027.983767 	1 	output.dat 	OST_NULL 	127 		3
obs248 		 -0.008668 	1 	output.dat 	OST_NULL 	127 		6
obs249 		-51281385.969638 	1 	output.dat 	OST_NULL 	128 		3
obs250 		 -0.008693 	1 	output.dat 	OST_NULL 	128 		6
obs251 		-50835041.729697 	1 	output.dat 	OST_NULL 	129 		3
obs252 		 -0.008654 	1 	output.dat 	OST_NULL 	129 		6
obs253 		-50048459.146445 	1 	output.dat 	OST_NULL 	130 		3
obs254 		 -0.008537 	1 	output.dat 	OST_NULL 	130 		6
obs255 		-48976552.934613 	1 	output.dat 	OST_NULL 	131 		3
obs256 		 -0.008343 	1 	output.dat 	OST_NULL 	131 		6
obs257 		-47628004.225348 	1 	output.dat 	OST_NULL 	132 		3
obs258 		 -0.008071 	1 	output.dat 	OST_NULL 	132 		6
obs259 		-45957937.927027 	1 	output.dat 	OST_NULL 	133 		3
obs260 		 -0.007722 	1 	output.dat 	OST_NULL 	133 		6
obs261 		-44295920.782297 	1 	output.dat 	OST_NULL 	134 		3
obs262 		 -0.007335 	1 	output.dat 	OST_NULL 	134 		6
obs263 		-42696611.473526 	1 	output.dat 	OST_NULL 	135 		3
obs264 		 -0.006947 	1 	output.dat 	OST_NULL 	135 		6
obs265 		-41150720.847035 	1 	output.dat 	OST_NULL 	136 		3
obs266 		 -0.006559 	1 	output.dat 	OST_NULL 	136 		6
obs267 		-39528368.511612 	1 	output.dat 	OST_NULL 	137 		3
obs268 		 -0.006171 	1 	output.dat 	OST_NULL 	137 		6
obs269 		-37909438.107774 	1 	output.dat 	OST_NULL 	138 		3
obs270 		 -0.005784 	1 	output.dat 	OST_NULL 	138 		6
obs271 		-36396689.545496 	1 	output.dat 	OST_NULL 	139 		3
obs272 		 -0.005402 	1 	output.dat 	OST_NULL 	139 		6
obs273 		-34717351.786094 	1 	output.dat 	OST_NULL 	140 		3
obs274 		 -0.005021 	1 	output.dat 	OST_NULL 	140 		6
obs275 		-32962213.952723 	1 	output.dat 	OST_NULL 	141 		3
obs276 		 -0.004637 	1 	output.dat 	OST_NULL 	141 		6
obs277 		-31197755.405226 	1 	output.dat 	OST_NULL 	142 		3
obs278 		 -0.004253 	1 	output.dat 	OST_NULL 	142 		6
obs279 		-29412385.712107 	1 	output.dat 	OST_NULL 	143 		3
obs280 		 -0.003870 	1 	output.dat 	OST_NULL 	143 		6
obs281 		-27553220.517937 	1 	output.dat 	OST_NULL 	144 		3
obs282 		 -0.003488 	1 	output.dat 	OST_NULL 	144 		6
obs283 		-25672310.927009 	1 	output.dat 	OST_NULL 	145 		3
obs284 		 -0.003103 	1 	output.dat 	OST_NULL 	145 		6
obs285 		-23744540.459863 	1 	output.dat 	OST_NULL 	146 		3
obs286 		 -0.002722 	1 	output.dat 	OST_NULL 	146 		6
obs287 		-21766401.115830 	1 	output.dat 	OST_NULL 	147 		3
obs288 		 -0.002338 	1 	output.dat 	OST_NULL 	147 		6
obs289 		-19580086.379152 	1 	output.dat 	OST_NULL 	148 		3
obs290 		 -0.001953 	1 	output.dat 	OST_NULL 	148 		6
obs291 		-17258640.392743 	1 	output.dat 	OST_NULL 	149 		3
obs292 		 -0.001567 	1 	output.dat 	OST_NULL 	149 		6
obs293 		-14701937.524105 	1 	output.dat 	OST_NULL 	150 		3
obs294 		 -0.001178 	1 	output.dat 	OST_NULL 	150 		6
obs295 		-11879893.705384 	1 	output.dat 	OST_NULL 	151 		3
obs296 		 -0.000788 	1 	output.dat 	OST_NULL 	151 		6
obs297 		-8499236.919778 	1 	output.dat 	OST_NULL 	152 		3
obs298 		 -0.000392 	1 	output.dat 	OST_NULL 	152 		6
obs299 		-4867921.259923 	1 	output.dat 	OST_NULL 	153 		3
obs300 		  0.000006 	1 	output.dat 	OST_NULL 	153 		6

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
EndExtraFiles

BeginParticleSwarm
SwarmSize  5
NumGenerations  10
EndParticleSwarm

#BeginGeneticAlg
#PopulationSize 10
#MutationRate 0.05
#Survivors 1
#NumGenerations 50
#EndGeneticAlg
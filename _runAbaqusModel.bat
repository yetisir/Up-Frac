python runAbaqusModel.py -f voronoiGranite -n voronoiGraniteVerify -r 1
CD OSTRICH
CALL copyTestScripts.bat
CD model0
CALL simulationData.bat
CD ..
CALL cleanup.bat
CD ..
 	
import os
from math import *
from caeModules import *
from odbAccess import *
from parameters import *
import pickle
import subprocess
from vectorMath import *
import time
          
def fWrite(stuff):
    with open('log.txt', 'a') as f:
        f.write(str(stuff)+'\n')
        
def sketchPart(name, gp):
    s = mdb.models['Model-1'].ConstrainedSketch(
        name='__profile__',sheetSize=10.0)
    for i in range(0, len(gp)-1):
        s.Line(point1=(gp[i][0], gp[i][1]), point2=(gp[i+1][0], gp[i+1][1]))
    p = mdb.models['Model-1'].Part(name=name, dimensionality=TWO_D_PLANAR,
                                   type=DEFORMABLE_BODY)
    p.BaseShell(sketch=s)
    del mdb.models['Model-1'].sketches['__profile__']
    
def tabulateVectors(vec1, vec2):
	vecLength = min(len(vec1), len(vec2))
	tabulatedData = []
	for i in range(vecLength):
		tabulatedData.append((vec1[i], vec2[i]))
	return tabulatedData
		
def concreteDamage(elasticModulus, poissonsRatio, peakYeildStress, peakYeildStrain,  initialCompressiveYeild, compressiveDamageScaling, initialTensileYeild, tLambda, tensileDamageScaling):
    materialName = 'Material-1'
    #****Concrete Damage Plasticity
    #dilationAngle = 10 #this will be same as UDEC****************************
    eccentricity = 0.1 #default
    fb0fc0 = 1.16 #default
    variableK = 6.700000E-01 #default
    viscousParameter = 0 #default
    #density = 2700# same as UDEC***************************************

    b = 1e6
    a = (initialCompressiveYeild - peakYeildStress)/peakYeildStrain**2
    compressiveYeildStress = add(multiply(a, power(subtract(inelasticStrain, peakYeildStrain), 2)), peakYeildStress)
    #compressiveYeildStress = [b if x < b else x for x in compressiveYeildStress]
    E = elasticModulus
    m = divide(1, add(divide(compressiveYeildStress, elasticModulus), inelasticStrain))
    m = min(m)*compressiveDamageScaling
    compressiveDamage = multiply(m, inelasticStrain)

    tensileYeildStress = multiply(initialTensileYeild, exp(multiply(tLambda, crackingStrain)))
    n = multiply(tensileDamageScaling, multiply(divide(log(subtract(1.00, divide(crackingStrain, add(divide(tensileYeildStress, elasticModulus), crackingStrain)))), log(add(1, crackingStrain))), -1))
    n[0] = elasticModulus/initialTensileYeild
    n = min(n)
    tensileDamage = subtract(1, divide(1, power(add(1, crackingStrain), n))) 
            
    mat = mdb.models['Model-1'].Material(name=materialName)
    mat.Density(table=((density, ), ))
    mat.Elastic(table=((elasticModulus, poissonsRatio), ))

    mat.ConcreteDamagedPlasticity(table=
        ((dilationAngle, eccentricity, fb0fc0, variableK, viscousParameter), ))
    mat.concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(tabulateVectors(compressiveYeildStress, inelasticStrain)))
    mat.concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(tabulateVectors(tensileYeildStress, crackingStrain)))
        
    mat.concreteDamagedPlasticity.ConcreteCompressionDamage(
        table=(tabulateVectors(compressiveDamage, inelasticStrain)))
    mat.concreteDamagedPlasticity.ConcreteTensionDamage(
        table=(tabulateVectors(tensileDamage, crackingStrain)))         

def druckerDamage(elasticModulus, poissonsRatio, frictionAngle, flowStressRatio, dilationAngle, initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain, yeildStrain1, yeildStrain2Diff, failureDisplacement):
    materialName = 'Material-1'
    
    #hardening_n = 0.5
    #compressiveYeildStress = add(hardening_A, multiply(hardening_B, power(inelasticStrain, hardening_n)))
    peakCompressiveYeild = initialCompressiveYeild+peakCompressiveYeildDiff
    
    alpha = (2*peakCompressiveYeild-initialCompressiveYeild+2*sqrt(peakCompressiveYeild*(peakCompressiveYeild-initialCompressiveYeild)))/initialCompressiveYeild
    beta = log((2*alpha)/(1+alpha))[0]/peakPlasticStrain

    plasticStrain = divide(range(0, 100), 2000)
    compressiveYeildStress = multiply(initialCompressiveYeild, subtract(multiply(1+alpha, exp(multiply(-beta, plasticStrain))), multiply(alpha, exp(multiply(-2*beta, plasticStrain)))))
    
    triaxiality = subtract(divide(range(0, 100), 25), 2)
    #yeildStrainMinus1 = yeildStrain0+yeildStrainMinus1Diff
    # johnson_D1 = (yeildStrainMinus1*yeildStrain1-yeildStrain0**2)/(yeildStrainMinus1+yeildStrain1-2*yeildStrain0)
    # johnson_D2 = -(yeildStrain0-yeildStrain1)*(yeildStrain0-yeildStrainMinus1)/(yeildStrainMinus1+yeildStrain1-2*yeildStrain0)
    # johnson_D3 = log(-(yeildStrain0-yeildStrain1)/(yeildStrain0-yeildStrainMinus1))[0]
    yeildStrain2 = yeildStrain2Diff+yeildStrain1
    johnson_D1 = 0
    johnson_D2 = yeildStrain1**3/yeildStrain2**2
    johnson_D3 = 4*log(yeildStrain2/yeildStrain1)[0]
    damageInitiationStrain = add(johnson_D1, multiply(johnson_D2, exp(multiply(-johnson_D3, triaxiality))))    
            
    mat = mdb.models['Model-1'].Material(name=materialName)
    mat.Density(table=((density, ), ))
    mat.Elastic(table=((elasticModulus, poissonsRatio), ))

    mat.DruckerPrager(shearCriterion=LINEAR, table=((frictionAngle, flowStressRatio, dilationAngle), ))
    mat.druckerPrager.DruckerPragerHardening(table=(tabulateVectors(compressiveYeildStress, plasticStrain)))
    mat.DuctileDamageInitiation(table=(tabulateVectors(damageInitiationStrain, triaxiality)))
    mat.ductileDamageInitiation.DamageEvolution(type=DISPLACEMENT, table=((failureDisplacement, ), ))		

def assignSection(name, part, location, material):
    mdb.models['Model-1'].HomogeneousSolidSection(name=name, material=material,
                                                  thickness=None)
    p = mdb.models['Model-1'].parts[part]
    f = p.faces
    faces = f.findAt((location, ))
    region = p.Set(faces=faces, name=name)
    p.SectionAssignment(region=region, sectionName=name, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

def meshPart(size, part, location, elementType, elementShape):
    p = mdb.models['Model-1'].parts[part]
    p.seedPart(size=size, deviationFactor=0.1, minSizeFactor=0.1)
    elemType = mesh.ElemType(elemCode=elementType)
    pickedRegions =(p.faces.findAt((location, )), )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType,))
    pickedRegions = p.faces.findAt((location, ))
    p.setMeshControls(regions=pickedRegions, elemShape=elementShape)
    p.generateMesh()

def createInstance(name, part):
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts[part]
    a.Instance(name=name, part=p, dependent=ON)

def applyVelocityBoundaryCondition(name, instance, step, location, v):
    a = mdb.models['Model-1'].rootAssembly
    edges1 = a.instances[instance].edges.findAt((location, ))
    region = a.Set(edges=edges1, name=name)
    # mdb.models['Model-1'].PeriodicAmplitude(name='Amp-1', timeSpan=STEP, 
        # frequency=pi/simulationTime, start=0.0, a_0=0, data=((0.0, 1.0), ))
    mdb.models['Model-1'].TabularAmplitude(name='Amp-1', timeSpan=STEP, 
        smooth=SOLVER_DEFAULT, data=velocityTable)
    mdb.models['Model-1'].VelocityBC(name=name, createStepName=step, 
        region=region, v1=v[0], v2=v[1], vr3=v[2], amplitude='Amp-1', 
        localCsys=None, distributionType=UNIFORM, fieldName='')  

def applyDisplacementBoundaryCondition(name, instance, step, location, u):
    a = mdb.models['Model-1'].rootAssembly
    edges1 = a.instances[instance].edges.findAt((location, ))
    region = a.Set(edges=edges1, name=name)
    mdb.models['Model-1'].DisplacementBC(name=name, createStepName=step, 
        region=region, u1=u[0], u2=u[1], ur3=u[2], amplitude=UNSET, 
        distributionType=UNIFORM, fieldName='', localCsys=None)    
        
# def applyConfiningStress(name, instance, step, location, stress):
    # a = mdb.models['Model-1'].rootAssembly
    # edges1 = a.instances[instance].edges.findAt((location, ))
    # region = a.Surface(side1Edges=edges1, name=name)
    # mdb.models['Model-1'].TabularAmplitude(name='Amp-2', timeSpan=STEP, 
        # smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (5, 1)))
    # mdb.models['Model-1'].Pressure(name=name, createStepName=step, 
        # region=region, distributionType=UNIFORM, field='', magnitude=stress, 
        # amplitude='Amp-2')
        
def applyGeostaticStress(name, instance, location, hStress, K=0.4):
    a = mdb.models['Model-1'].rootAssembly
    faces1 = a.instances[instance].faces.findAt((location, ))
    region = a.Set(faces=faces1, name=name)
    mdb.models['Model-1'].GeostaticStress(name=name, region=region, 
        stressMag1=-hStress/K, vCoord1=0, stressMag2=-hStress/K, vCoord2=10, 
        lateralCoeff1=K, lateralCoeff2=K)   

def applyBoundaryStress(name, instance, step, location, stress):
    a = mdb.models['Model-1'].rootAssembly
    edges1 = a.instances[instance].edges.findAt((location, ))
    region = a.Surface(side1Edges=edges1, name=name)
    mdb.models['Model-1'].Pressure(name=name, createStepName=step, 
        region=region, distributionType=UNIFORM, field='', magnitude=stress, 
        amplitude=UNSET)
        
def applyInitialStress(name, instance, location, cStress):
    a = mdb.models['Model-1'].rootAssembly
    faces1 = a.instances[instance].faces.findAt((location, ))
    region = a.Set(faces=faces1, name=name)
    mdb.models['Model-1'].Stress(name=name, region=region, 
        distributionType=UNIFORM, sigma11=-cStress, sigma22=-cStress/2, sigma33=-cStress, 
        sigma12=0, sigma13=None, sigma23=None)        
        
def createStaticStep(name, previous):
    mdb.models['Model-1'].StaticStep(name=name, previous=previous, timePeriod=simulationTime,
                                     maxNumInc=1000, initialInc=0.5, minInc=0.001,
                                     maxInc=0.5, matrixSolver=DIRECT,
                                     matrixStorage=UNSYMMETRIC, nlgeom=largeDef)

def createExplicitDynamicStep(name, previous):
    mdb.models['Model-1'].ExplicitDynamicsStep(name=name, previous=previous, 
                                                timePeriod=simulationTime, nlgeom=largeDef)

def createImplicitDynamicStep(name, previous):
    mdb.models['Model-1'].ImplicitDynamicsStep(name=name, previous=previous, nlgeom=largeDef)
                                                
def createGeostaticStep(name, previous):
    mdb.models['Model-1'].GeostaticStep(name=name, previous=previous, nlgeom=largeDef)

def applyGravity(magnitude, stepName):
    mdb.models['Model-1'].Gravity(name='Gravity', createStepName=stepName, comp2=magnitude,
                                  distributionType=UNIFORM, field='')
                                  
def applyConfiningStress(confiningStress):
    if confiningStress != 0:
        applyInitialStress('Geostatic', instanceName, sectionLocation, confiningStress)
        applyBoundaryStress('Left', instanceName, 'Step-1', boundaries['Left'], confiningStress)
        applyBoundaryStress('Right', instanceName, 'Step-1', boundaries['Right'], confiningStress)

def buildModel():
    partName = 'Block'
    materialName = 'Material-1'
    sectionName = 'Block'
    steps = ('Initial', 'Step-1', 'Step-2')

    sketchPart(partName, gridPoints)
    
    elasticModulus = 2.584811E+09
    poissonsRatio = 2.031272E-01
    frictionAngle = 5.408E+01
    flowStressRatio = 9.861088E-01
    dilationAngle = 1.235141E+01
    initialCompressiveYeild = 0.0540673E+06
    peakCompressiveYeildDiff = 1.496927E+06
    peakPlasticStrain = 1.515889E-02
    yeildStrain1 = 3.62e-4
    yeildStrain2Diff = 4.88e-2
    failureDisplacement = 0.10968E+00
    
    
    druckerDamage(elasticModulus, poissonsRatio, frictionAngle, flowStressRatio, dilationAngle, initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain, yeildStrain1, yeildStrain2Diff, failureDisplacement)
    assignSection(sectionName, partName, sectionLocation, materialName)
    meshPart(meshSize, partName, sectionLocation, elementType, elementShape)
    createInstance(instanceName, partName)

    # createGeostaticStep(steps[1], steps[0])
    createExplicitDynamicStep(steps[1],steps[0])
    # createExplicitDynamicStep(steps[1], steps[0])
    # createExplicitDynamicStep(steps[2],steps[1])

    #applyGravity(gravityMagnitude, stepName)
    # if confiningStress != 0:
        # applyConfiningStress('Right', instanceName, steps[1], boundaries['Right'], -confiningStress)
        # applyConfiningStress('Left', instanceName, steps[1], boundaries['Left'], -confiningStress)
    # applyGeostaticStress('Geostatic', instanceName, sectionLocation, confiningStress)
   
    applyDisplacementBoundaryCondition('Bottom', instanceName, steps[0], boundaries['Bottom'],
        (UNSET, SET, UNSET))
    # applyDisplacementBoundaryCondition('Top', instanceName, steps[0], boundaries['Top'], 
        # (UNSET, SET, UNSET))
    # mdb.models['Model-1'].boundaryConditions['Top'].setValuesInStep(stepName=steps[2], u2=FREED)

    applyVelocityBoundaryCondition('vTop', instanceName, steps[1], boundaries['Top'], (UNSET, v, UNSET))

def getStress(jobName, stepName, instanceName):
    odb = openOdb(jobName+'.odb')
    allElements = odb.rootAssembly.instances[instanceName].elements    
    allFrames = odb.steps[stepName].frames
    
    element = allElements[0]
    stressHistory = [[0 for x in range(3)] for x in range(len(allFrames))] 
    for i in range(len(allFrames)):
        stress = allFrames[i].fieldOutputs['S'].getSubset(position=CENTROID).values[0].data
        stressHistory[i][0] = stress[0]
        stressHistory[i][1] = stress[1]
        stressHistory[i][2] = stress[3]
    odb.close()
    return stressHistory

def getStrain(jobName, stepName, instanceName):
    odb = openOdb(jobName+'.odb')
    allElements = odb.rootAssembly.instances[instanceName].elements    
    allFrames = odb.steps[stepName].frames
    
    element = allElements[0]
    strainHistory = [[0 for x in range(3)] for x in range(len(allFrames))] 
    strainShift = allFrames[0].fieldOutputs['LE'].getSubset(position=CENTROID).values[0].data

    for i in range(len(allFrames)):
        strain = allFrames[i].fieldOutputs['LE'].getSubset(position=CENTROID).values[0].data
        strainHistory[i][0] = strain[0]#-strainShift[0]
        strainHistory[i][1] = strain[1]#-strainShift[1]
        strainHistory[i][2] = strain[3]#-strainShift[3]
    odb.close()
    return strainHistory
    
def getTime(jobName, stepName, instanceName):
    odb = openOdb(jobName+'.odb')
    allFrames = odb.steps[stepName].frames
    timeHistory = [allFrames[x].frameValue for x in range(len(allFrames))] 
    #for i in range(len(allFrames)):
    #    timeHistory[i] = allFrames[i].frameValue
    odb.close()
    return timeHistory
    
def main():
    #open('log.txt', 'w').close()
    buildModel()
    for i in range(len(confiningStress)):
        applyConfiningStress(confiningStress[i])
        jobName = 'Job-{0}'.format(i+1)
        mdb.Job(name=jobName, model='Model-1', description='', type=ANALYSIS, atTime=None,
                waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE,
                getMemoryFromAnalysis=True, explicitPrecision=SINGLE,
                nodalOutputPrecision=SINGLE, echoPrint=OFF,
                modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
                scratch='', parallelizationMethodExplicit=DOMAIN, numDomains=1, 
                activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)
        mdb.jobs[jobName].submit(consistencyChecking=OFF)
    
        while 1:
            try:
                timeHistory = getTime(jobName, 'Step-1', instanceName)
                stressHistory = getStress(jobName, 'Step-1', instanceName)
                strainHistory = getStrain(jobName, 'Step-1', instanceName)                
                with open('{0}_rawHistory.pkl'.format(jobName), 'wb') as file:
                    pickle.dump(timeHistory, file)
                    pickle.dump(stressHistory, file)
                    pickle.dump(strainHistory, file)
                break
            except:# FileNotFoundError:
                pass


if __name__ == '__main__': 
    attempts = 2
    while attempts >0:
        try:
            main()
            break
        except Exception as e:
            #os.system('jclean.bat')
            fWrite(e)
            attempts -= 1
                # with open('OstExeOut.txt', 'r') as f:
                    # for i in f.readlines():
                        # fWrite(i)
                # try:
                    # with open('Job-1.dat', 'r') as f:
                        # for i in f.readlines():
                            # fWrite(i)
                    # with open('Job-2.dat', 'r') as f:
                        # for i in f.readlines():
                            # fWrite(i)
                    # with open('Job-3.dat', 'r') as f:
                        # for i in f.readlines():
                            # fWrite(i)
                # except:pass
ostrichParameters = {dilationAngle:[5, 10, 15],  
modelParameters = {dilationAngle:10,
                                density:
                                mSize:
                                mName:
                                vString:
                                vel:
                                cobfStress:
                                simulationTime:}


def defineMaterial():
    #****Concrete Damage Plasticity
    dilationAngle = 10 #this will be same as UDEC
    eccentricity = 0.1 #default
    fb0fc0 = 1.16 #default
    variableK = 6.700000E-01 #default
    viscousParameter = 0 #default

    numStrainPoints = 100
    inelasticStrain = divide(range(0, numStrainPoints+1), numStrainPoints/0.0293071700239)
    h = $h
    k = $k
    d = $dd
    b = 1e6
    a = (d - k)/h**2
    compressiveYeildStress = add(multiply(a, power(subtract(inelasticStrain, h), 2)), k)
    compressiveYeildStress = [b if x < b else x for x in compressiveYeildStress]
    compressiveDamageScaling = $cd
    E = elasticModulus
    m = divide(1, add(divide(compressiveYeildStress, E), inelasticStrain))
    m = min(m)*compressiveDamageScaling
    compressiveDamage = multiply(m, inelasticStrain)

    if '(t)' in mName:
        crackingStrain = divide(range(0, numStrainPoints+1), numStrainPoints/0.0293071700239)
    elif '(c)' in mName:
        crackingStrain = divide(range(0, numStrainPoints+1), numStrainPoints/0.000456774923467)
    N = 2241357.0
    tLambda = -2210.0
    tensileYeildStress = multiply(N, exp(multiply(tLambda, crackingStrain)))
    tensileDamageScaling = 0.9284359
    n = multiply(tensileDamageScaling, multiply(divide(log(subtract(1.00, divide(crackingStrain, add(divide(tensileYeildStress, elasticModulus), crackingStrain)))), log(add(1, crackingStrain))), -1))
    n[0] = elasticModulus/N
    n = min(n)
    tensileDamage = subtract(1, divide(1, power(add(1, crackingStrain), n))) 



    mat = mdb.models['Model-1'].Material(name='concreteDamage')
    mat.ConcreteDamagedPlasticity(table=
        ((dilationAngle, eccentricity, fb0fc0, variableK, viscousParameter), ))
    mat.concreteDamagedPlasticity.ConcreteCompressionHardening(
        table=(tablulateVectors(compressiveYeildStress, inelasticStrain)))
    mat.concreteDamagedPlasticity.ConcreteTensionStiffening(
        table=(tablulateVectors(tensileYeildStress, crackingStrain)))
        
    mat.concreteDamagedPlasticity.ConcreteCompressionDamage(
        table=(tablulateVectors(compressiveDamage, inelasticStrain)))
    mat.concreteDamagedPlasticity.ConcreteTensionDamage(
        table=(tablulateVectors(tensileDamage, crackingStrain)))

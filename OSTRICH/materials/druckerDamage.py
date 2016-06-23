ostrichParameters = {   
                            'elasticModulus':{          'init':2.5e9,    'low':1e9,      'high':10e9},
                            'poissonsRatio':{           'init':0.2,     'low':0.15,     'high':0.45},
                            'frictionAngle':{           'init':54,      'low':45,       'high':70}, 
                            'flowStressRatio':{         'init':0.98,     'low':0.78,     'high':1},
                            'dilationAngle':{           'init':12.3,      'low':5,        'high':15},
                            'initialCompressiveYeild':{ 'init':54e3,     'low':1e3,    'high':100e3},
                            'peakCompressiveYeildDiff':{'init':1.5e6,     'low':0.5e6,    'high':5e6},
                            'peakPlasticStrain':{       'init':15e-3,   'low':5e-3,        'high':50e-3},
                            'yeildStrain1':{            'init':362e-6,    'low':10e-6,   'high':1000e-6},
                            'yeildStrain2':{            'init':48.8e-3,    'low':10e-3,   'high':1000e-3},
                            'failureDisplacement':{     'init':0.1,     'low':0,        'high':1}}
 
                
abaqusTemplate = '''
    elasticModulus = $elasticModulus
    poissonsRatio = $poissonsRatio
    frictionAngle = $frictionAngle
    flowStressRatio = $flowStressRatio
    dilationAngle = $dilationAngle
    initialCompressiveYeild = $initialCompressiveYeild
    peakCompressiveYeildDiff = $peakCompressiveYeildDiff
    peakPlasticStrain = $peakPlasticStrain
    yeildStrain1 = $yeildStrain1
    yeildStrain2Diff = $yeildStrain2
    failureDisplacement = $failureDisplacement
    druckerDamage(elasticModulus, poissonsRatio, frictionAngle, flowStressRatio, dilationAngle, initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain, yeildStrain1, yeildStrain2Diff, failureDisplacement)
    '''
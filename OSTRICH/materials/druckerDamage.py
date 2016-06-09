#these arrays shhould be tied to the material definitions
# materialParameters =  [['$elasticModulus', 
                # '$poissonsRatio'], 
                
                # ['$frictionAngle', 
                # # '$dilationAngle',
                # # '$initialTensileStrength',
                # '$hardening_A', 
                # '$hardening_B'],
                
                # ['$johnson_D2', 
                # '$johnson_D3', 
                # '$failureDisplacement']]
materialParameters =  [['$elasticModulus', 
                '$poissonsRatio',
                '$frictionAngle', 
                '$initialTensileStrength',
                '$dilationAngle',
                '$initialCompressiveYeild', 
                '$peakCompressiveYeildDiff',
                '$peakPlasticStrain', 
                '$johnson_D1', 
                '$johnson_D2', 
                '$johnson_D3', 
                '$failureDisplacement']]
                                
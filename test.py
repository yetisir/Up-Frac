from OSTRICH.vectorMath import *
johnson_D1 = 8.595829E-01
johnson_D2 = 3.398719E+00
johnson_D3 = 8.072387E+00
triaxiality = subtract(divide(range(0, 100), 25), 2)
damageInitiationStrain = add(johnson_D1, multiply(johnson_D2, exp(multiply(-johnson_D3, triaxiality))))    
print(triaxiality)
print(damageInitiationStrain)

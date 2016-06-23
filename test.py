from math import *
def tensilePlasticStrain(n):
    elasticModulus = 9.183612E+09
    tLambda = -3.897482E+02
    initialTensileYeild = 3.331734E+05

    

    approxStrain = 0.05

    return (initialTensileYeild*tLambda*exp(approxStrain*tLambda)*(1/(approxStrain + 1)**n - 1)*(approxStrain + 1)**n)/elasticModulus - (initialTensileYeild*n*exp(approxStrain*tLambda)*(approxStrain + 1)**n)/(elasticModulus*(approxStrain + 1)**(n + 1)) + (initialTensileYeild*n*exp(approxStrain*tLambda)*(1/(approxStrain + 1)**n - 1)*(approxStrain + 1)**(n - 1))/elasticModulus + 1

def compressivePlasticStrain(m):
    elasticModulus = 10e9
    initialCompressiveYeild = 1e6
    peakCompressiveYeildDiff = 5e6
    peakPlasticStrain = 3e-2
    
    peakCompressiveYeild = initialCompressiveYeild+peakCompressiveYeildDiff
    alpha = (2*peakCompressiveYeild-initialCompressiveYeild+2*sqrt(peakCompressiveYeild*(peakCompressiveYeild-initialCompressiveYeild)))/initialCompressiveYeild
    beta = log((2*alpha)/(1+alpha))/peakPlasticStrain
    approxStrain = 0.05

    return ((initialCompressiveYeild*approxStrain*m*(beta*exp(-beta*approxStrain)*(alpha - 1) + 2*alpha*beta*exp(-2*beta*approxStrain)))/(elasticModulus*(approxStrain*m - 1)) - (initialCompressiveYeild*m*(alpha*exp(-2*beta*approxStrain) + exp(-beta*approxStrain)*(alpha - 1)))/(elasticModulus*(approxStrain*m - 1)) + (initialCompressiveYeild*approxStrain*m**2*(alpha*exp(-2*beta*approxStrain) + exp(-beta*approxStrain)*(alpha - 1)))/(elasticModulus*(approxStrain*m - 1)**2) + 1)
    

    
def root(f, limits, tolerance, samples=10):
    dl = (limits[1]-limits[0])/samples
    n = [limits[0]]
    for i in range(1, samples+1):
        n.append(n[i-1]+dl) 
    i = 1
    while i < samples+1:
        val = f(n[i])
        input()
        print(val, n[i])
        if val < 0 and n[i-1]!=n[i] :
            nRefined = root(f, [n[i-1], n[i]],tolerance)
            n.append(nRefined)
            break
        if abs(val) < tolerance:
            break
        i += 1
    if i == samples+1:
        nRefined = root(f, [n[0], n[-1]*10],tolerance)
        n.append(nRefined)
    return n[-1]
    
#print(root(tensilePlasticStrain, [0, 10], 0.001))

#print(root(compressivePlasticStrain, [0, 1], 0.001))

for i in range(30):
    print(i, compressivePlasticStrain(i))

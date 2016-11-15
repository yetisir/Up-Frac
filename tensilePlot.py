import matplotlib.pyplot as plt
from OSTRICH.vectorMath import *

def compressiveBeta(initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain):
    peakCompressiveYeild = initialCompressiveYeild+peakCompressiveYeildDiff
    alpha = compressiveAlpha(initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain)
    return math.log((2*alpha)/(1+alpha))/peakPlasticStrain
    
def compressiveAlpha(initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain):
    peakCompressiveYeild = initialCompressiveYeild+peakCompressiveYeildDiff
    return (2*peakCompressiveYeild-initialCompressiveYeild+2*math.sqrt(peakCompressiveYeild*(peakCompressiveYeild-initialCompressiveYeild)))/initialCompressiveYeild

def main():       

    initialTensileYeild = 2    
    plasticStrain = divide(range(0, 100), 100/5)
    tLambda = -4
    tensileYeildStress = multiply(initialTensileYeild, exp(multiply(tLambda, plasticStrain)))
    plt.figure(figsize=(10,5))

    plt.plot(plasticStrain, tensileYeildStress, linewidth=2)
    plt.plot(0,  initialTensileYeild, 'r.', markersize=20)
    
    plt.text(0.1,  initialTensileYeild, '$(0, \sigma_t^{iy})$', fontsize='xx-large')
    plt.ylim([0, 3])
    plt.xlim([0, 5])
    
    plt.gca().get_xaxis().set_ticks([])
    plt.gca().get_yaxis().set_ticks([])    
    plt.xlabel('Plastic Strain', fontsize = 'large')
    plt.ylabel('Yield Stress',fontsize = 'large')

    plt.show()
    
    
if __name__ == '__main__':
    main()

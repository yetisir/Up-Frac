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

    initialCompressiveYeild = 2.2
    peakCompressiveYeildDiff = 1.46
    peakPlasticStrain = 0.8
    peakCompressiveYeild = initialCompressiveYeild+peakCompressiveYeildDiff
    
    alpha = compressiveAlpha(initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain)
    beta = compressiveBeta(initialCompressiveYeild, peakCompressiveYeildDiff, peakPlasticStrain)

    plasticStrain = divide(range(0, 100), 100/5)
    compressiveYeildStress = multiply(initialCompressiveYeild, subtract(multiply(1+alpha, exp(multiply(-beta, plasticStrain))), multiply(alpha, exp(multiply(-2*beta, plasticStrain)))))

    plt.plot(plasticStrain, compressiveYeildStress, linewidth=2)
    plt.plot(peakPlasticStrain,  peakCompressiveYeild, 'r.', markersize=20)
    plt.plot(0,  initialCompressiveYeild, 'r.', markersize=20)
    
    plt.xlim([-0.00, 5])
    plt.ylim([0, 5])
    plt.text(peakPlasticStrain*0.6,  peakCompressiveYeild*1.05, '$(\epsilon_c^{p}, \sigma_c^{p})$', fontsize='xx-large')
    plt.text(0.1,  initialCompressiveYeild, '$(0, \sigma_c^{iy})$', fontsize='xx-large')
    
    plt.gca().get_xaxis().set_ticks([])
    plt.gca().get_yaxis().set_ticks([])    
    plt.xlabel('Plastic Strain', fontsize = 'large')
    plt.ylabel('Yield Stress',fontsize = 'large')

    plt.show()
    
    
if __name__ == '__main__':
    main()
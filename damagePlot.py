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

    tensileDamageScaling = 6    
    plasticStrain = divide(range(0, 100), 100/5)
    tensileDamage = subtract(0.99, divide(1, power(add(1, plasticStrain), tensileDamageScaling))) 
    plt.figure(figsize=(10,5))
    plt.plot(plasticStrain, tensileDamage, linewidth=2)
    plt.plot([0,5], [0,0.5], linewidth=2)
    plt.plot([0,5],  [1,1], '-r', markersize=20)
    
    plt.text(0.2,  1.03, '$y=1$', fontsize='xx-large')
    plt.text(2.7,  0.2, 'Compressive Damage', fontsize='large')
    plt.text(0.3,  0.7, 'Tensile Damage', fontsize='large')
    plt.ylim([0, 1.5])
    plt.xlim([0, 4.9])
    
    plt.gca().get_xaxis().set_ticks([])
    plt.gca().get_yaxis().set_ticks([])    
    plt.xlabel('Plastic Strain', fontsize = 'large')
    plt.ylabel('Yield Stress',fontsize = 'large')

    plt.show()
    
    
if __name__ == '__main__':
    main()

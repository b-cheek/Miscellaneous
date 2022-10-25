##maxFactors=0
##num=0
##while maxFactors>=0:
##    factors=0
##    for n in range(2,(round(num/2)+1)):
##        if (int(num))%n==0:
##            if n==(num/n):
##                factors+=1
##                break
##            elif n>(num/n):
##                break
##            factors+=2
##    if factors>maxFactors:
##        print (num)
##        maxFactors=factors
##    num+=1

maxFactors=0
# num=520700
num=100
maxPfactors=0
maxFactorDiff=0
factorDiff=0
while maxFactors>=0:
    factors=0
    for n in range(2,(round(num/2)+1)):
        if (int(num))%n==0:
            if n==(num/n):
                factors+=1
                break
            elif n>(num/n):
                break
            factors+=2
    if factors>maxFactors:
        print (num)
        if maxFactors>0:
            factorDiff=factors-maxFactors
        if factorDiff>maxFactorDiff:
            maxFactorDiff=factorDiff
            print ("Largest increase in factors! Improved by", factorDiff, "factors")
        maxFactors=factors
    num+=1



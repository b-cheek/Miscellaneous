##Problem 6: Don't Change!

def quarters(val):
    print('')
    print ("$"+str(val))
    modVal=(float(val)%0.25)
    modVal=round(modVal,2)
    quotient=(float(val)-modVal)
    quotient=round(quotient,2)
    q=int((quotient)/0.25)
    q=round(q,2)
    print ("Quarters= "+str(q))
    return modVal

def dimes(val):
    modVal=(float(val)%0.1)
    modVal=round(modVal,2)
    quotient=(float(val)-modVal)
    quotient=round(quotient,2)
    d=int((quotient)/0.1)
    d=round(d,2)
    print ("Dimes= "+str(d))
    return modVal

def nickels(val):
    modVal=(float(val)%0.05)
    modVal=round(modVal,2)
    quotient=(float(val)-modVal)
    quotient=round(quotient,2)
    n=int((quotient)/0.05)
    n=round(n,2)
    print ("Nickels= "+str(n))
    return modVal

def pennies(val):
    modVal=(float(val)%0.01)
    modVal=round(modVal,2)
    quotient=(float(val)-modVal)
    quotient=round(quotient,2)
    p=int((quotient)/0.01)
    p=round(p,2)
    print ("Pennies= "+str(p))
    return modVal
    
times=int(input("How many times?"))
valList=[]
for i in range (0,times):
    val=str(input(''))
    val=(val[1:])
    valList.append(val)
for i in valList:
    pennies(nickels(dimes(quarters(i))))
        
        

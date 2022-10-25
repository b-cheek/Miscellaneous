##Problem 9: Pythagorean Theorem

def leg2(length):
    printTrip=True
    for i in range (2,length):
        if length<100:
            for j in range (length, (length*2)):
                if i**2 + (length)**2 == j**2:
                    triple=[]
                    triple.append(i)
                    triple.append(length)
                    triple.append(j)
                    for i in triple:
                        if int(i)>=1000:
                            printTrip=False
                    if printTrip==True:
                        print (triple)
                        
        elif length>=100:
            for j in range (length, 1000):
                if i**2 + (length)**2 == j**2:
                    triple=[]
                    triple.append(i)
                    triple.append(length)
                    triple.append(j)
                    for i in triple:
                        if int(i)>=1000:
                            printTrip=False
                    if printTrip==True:
                        print (triple)

def leg1(length):
    printTrip=True
    for i in range ((length),(length**2)):
        for j in range (length, 1000):
            if (length)**2 + i**2 == j**2:
                triple=[]
                triple.append(length)
                triple.append(i)
                triple.append(j)
                for i in triple:
                    if int(i)>=1000:
                        printTrip=False
                if printTrip==True:
                    print (triple)

def hyp(length):
    printTrip=True
    for i in range (0,length):
        for j in range (0,i):
            if j**2 + i**2 == (length)**2:
                triple=[]
                triple.append(j)
                triple.append(i)
                triple.append(length)
                for i in triple:
                    if int(i)>=1000:
                        printTrip=False
                if printTrip==True:
                    print (triple)
running=True
while running==True:
    length=int(input('what is the length of the side?'))
    if length==0:
        print ("The End")
        running=False
    else:
        hyp(length)
        leg2(length)
        leg1(length)
        print ('')
    
    

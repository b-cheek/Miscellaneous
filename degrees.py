##Problem 5: -40 Degrees?

convNum=int(input("How many conversions? "))
convList=[]
for i in range (0, convNum):
    temp=str(input(''))
    if (temp[-1:])=='C':
        tempDeg=((float(temp[:-2]))*(9/5)+32)
        conv=(str(temp)+' = '+(str(round(tempDeg, 1))+ " F"))
        convList.append(conv)
    elif (temp[-1:])=='F':
        tempDeg=((float(temp[:-2])-32)*(5/9))
        conv=(str(temp)+' = '+(str(round(tempDeg, 1))+ " C"))
        convList.append(conv)
for i in convList:
    print (i)

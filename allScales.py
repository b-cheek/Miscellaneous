from random import randrange

scales = []

def scaleTotal(scale):
    total=0
    for i in scale:
        total+=i
    return total

for i in range(0, 999999):
    if i%10000==1: print(i)
    curScale=[]
    while scaleTotal(curScale)<12:
        curScale.append(randrange(3)+1)
    if scaleTotal(curScale)==12 and curScale not in scales:
        succ=True
        for i in range(0, len(curScale)):
            if curScale[i]==curScale[i-1]:
                if (curScale[i]==1) or (curScale[i]==3): succ=False
            elif succ:
                if (curScale[i]==2) and (curScale[i-1]==3): succ=False
                elif (curScale[i]==3) and (curScale[i-1]==2): succ=False

        if succ:
            curScale.extend(curScale)
            for i in range(0,int(len(curScale)/2)):
                newScale = curScale[i:i+int(len(curScale)/2)]
                if newScale not in scales:
                    print(newScale)
                    scales.append(newScale)
            print("")
            scales.append("")

for i in scales:
    print(i)
input()

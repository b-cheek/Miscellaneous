import math
from collections import Counter

ListA = "Hello how are you? The weather is fine. I'd like to go for a walk.".split()
ListB = "bank, weather, sun, moon, fun, hi".split(",")

def cosdis(v1, v2):
    common = v1[1].intersection(v2[1])
    return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]

def word2vec(word):
    cw = Counter(word)
    sw = set(cw)
    lw = math.sqrt(sum(c * c for c in cw.values()))
    return cw, sw, lw

def removePunctuations(str_input):
    ret = []
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for char in str_input:
        if char not in punctuations:
            ret.append(char)

    return "".join(ret)


print("List A:\tListB:\tCosine Distance:")
for i in ListA:
    for j in ListB:
       print(i+"\t"+j, cosdis(word2vec(removePunctuations(i)), word2vec(removePunctuations(j))))

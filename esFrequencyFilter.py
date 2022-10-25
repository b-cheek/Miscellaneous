import re

fDict = open("FreqDictLemmas.txt", "r", encoding='utf-8')
fNotes = open("AllDecks.txt", "r", encoding="utf-8")
regex = '[a-zA-záéíóúüñ]+ [a-zA-záéíóúüñ]+ [a-zA-záéíóúüñ]+ [a-zA-záéíóúüñ]+|[a-zA-záéíóúüñ]+ [a-zA-záéíóúüñ]+ [a-zA-záéíóúüñ]+|[a-zA-záéíóúüñ]+ [a-zA-záéíóúüñ]+|[a-zA-záéíóúüñ]+'
freqDict = fDict.read()
notes = fNotes.read().lower()
freqArr = re.findall(regex, freqDict)
print(freqArr)
lemmaFreqArr = []
for i in range(1, len(freqArr), 2):
    print(i//2+1, freqArr[i])
    lemmaFreqArr.append(freqArr[i])
newLemmas = []
for i in lemmaFreqArr:
    for j in i.split(" "):
        if j not in notes and j not in newLemmas:
            if len(i.split(" "))>1:
                newLemmas.append(j + " from " + i)
            else:
                newLemmas.append(j)

for i in range(0, len(newLemmas)):
    print("<p>" + str(i+1) + ". " + newLemmas[i] + "</p>")
print (len(newLemmas))

fDict.close()
fNotes.close()

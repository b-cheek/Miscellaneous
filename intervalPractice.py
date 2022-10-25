import random

##notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
notesFlats = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"] #I would put Ab in front, but lining them up makes enharmonic checking easy
notesSharps = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
accidentals = ['♭', '♮', '♯']
intervalDict = ["m2", "M2", "m3", "M3", "P4", "tritone", "P5", "m6", "M6", "m7", "M7"]
run = True

while run:
##    startNote = random.randint(0,6) #just the letter name
##    startAccidental = random.randint(0,2)
    accidental = random.randint(0,1)
    chromaticNotes = (notesSharps if accidental==1 else notesFlats)
    startNote = random.randint(0,11) #Random chromatic index
    intervalDirection = bool(random.randint(0,1)) #True if up, False if down
    interval = random.randint(1,11) #spanning from m2 to M7
    intervalName = intervalDict[interval-1] #since a 2nd is only 1 above start note, adjust for indexing
    if not intervalDirection: interval = 12 - interval
    
    # if (len(interval)>2):
    #     intervalQuality = 'A'
    #     intervalDistance = 4

    # else:
    #     intervalQuality = interval[0]
    #     intervalDistance = int(interval[1])
    #     if (not intervalDirection): #if it's a down interval, change M3 to m6 etc
    #         intervalDistance = 9 - intervalDistance
    #         intervalQuality = ('m' if (intervalQuality=='M') else 'M')
                
##    endNote = notes[(startNote + intervalDistance - 1)%7]
    endNote = chromaticNotes[(startNote + interval)%12]
    
        

##    print(chromaticNotes[startNote], ("up" if intervalDirection else "down"), intervalName, interval, "=", endNote)
    # response = input((chromaticNotes[startNote], ("up" if intervalDirection else "down"), intervalName, "=: "))
    print(chromaticNotes[startNote], ("up" if intervalDirection else "down"), intervalName)
    response = input()
    if response==notesFlats[(startNote + interval)%12] or response==notesSharps[(startNote + interval)%12]:
        print("Correct!")
    elif response == "end":
        run = False
    else:
        print("Wrong :(")
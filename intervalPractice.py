import random

notesFlats = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab"] #I would put Ab in front, but lining them up makes enharmonic checking easy
notesSharps = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
accidentals = ['♭', '♮', '♯']
intervalDict = ["m2", "M2", "m3", "M3", "P4", "tritone", "P5", "m6", "M6", "m7", "M7"]
run = True
questions = correct = 0

while run:
    questions += 1
    accidental = random.randint(0,1)
    chromaticNotes = (notesSharps if accidental==1 else notesFlats)
    startNote = random.randint(0,11) #Random chromatic index
    intervalDirection = bool(random.randint(0,1)) #True if up, False if down
    interval = random.randint(1,11) #spanning from m2 to M7
    intervalName = intervalDict[interval-1] #since a 2nd is only 1 above start note, adjust for indexing
    if not intervalDirection: interval = 12 - interval
    
    endNote = chromaticNotes[(startNote + interval)%12]
    
    print(chromaticNotes[startNote], ("up" if intervalDirection else "down"), intervalName)
    response = input()
    if response.lower()==notesFlats[(startNote + interval)%12].lower() or response.lower()==notesSharps[(startNote + interval)%12].lower():
        print("Correct! O0O0O0O0O0O0O0O0O0")
        correct += 1
    elif response == "end":
        run = False
    else:
        print("Wrong :(", chromaticNotes[(startNote + interval)%12], "was correct\t*!*!*!*!*!*!*!*")
    print("\b" + str(correct) + "/" + str(questions), "(" + str(round(10000*correct/questions)/100) + "%\n")
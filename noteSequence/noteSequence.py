from music21 import note, interval, pitch
notes = """F3
C3
A4
Bb3
F4
Gb2
D3
Ab5
C#4
E3
F#4
E2
B5
B4
Gb3
A3
G#2
E4
F2
Ab4
B3""".split("\n")
intervals = [interval.Interval(noteStart=note.Note(notes[i]), noteEnd=note.Note(notes[i+1])).semitones for i in range(0,len(notes)-1)]
midis = [pitch.Pitch(i).midi for i in notes]
deltaIntervals = [intervals[i+1] - intervals[i] for i in range(0, len(intervals)-1)]
deltaIntervals2 = [deltaIntervals[i+1] - deltaIntervals[i] for i in range(0, len(deltaIntervals)-1)]
deltaIntervals3 = [deltaIntervals2[i+1] - deltaIntervals2[i] for i in range(0, len(deltaIntervals2)-1)]

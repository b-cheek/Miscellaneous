import xml.etree.ElementTree as ET
import os

# Parse xml files in MusicXML Lead Sheets folder
for filename in os.listdir('jazzChanges\MusicXML Lead Sheets'):
    tree = ET.parse('jazzChanges\MusicXML Lead Sheets/' + filename)
    root = tree.getroot()
    # Create list of measures
    measures = []
    chords = []
    chord_names = []
    for measure in tree.iter('measure'):
        measures.append(measure)

    for measure in measures:
        chords += measure.findall('harmony')
    
    for chord in chords:
        chord_names.append(chord.find('kind').text)
    print(filename)
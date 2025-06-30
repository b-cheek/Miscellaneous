import xml.etree.ElementTree as ET
import os
class Measure:
    def __init__(self, chord_name, repeat, coda, ending, rehearsal_mark, nav_marking, fine, segno):
        pass
class ChordSheet:
    def __init__(self):
        self.measures = []

# Parse xml files in MusicXML Lead Sheets folder
for filename in os.listdir('jazzChanges/MusicXML Lead Sheets'):
    tree = ET.parse('jazzChanges/MusicXML Lead Sheets/' + filename)
    root = tree.getroot()
    # Get metadata
    title = root.find('.//work-title').text
    composer = root.find('.//creator[@type="composer"]').text
    style = root.find('.//creator[@type="lyricist"]').text

    key = root.find('.//fifths').text + ' ' + root.find('.//mode').text

    # Create list of measures
    chord_sheet = ChordSheet()

    measures = []
    chords = []
    chord_names = []
    for measure in root.iter('measure'):
        measures.append(measure)

    cur_measure = 0
    repeat_to = 0
    take_repeat = True
    while cur_measure < len(measures):
        chord_sheet.measures.append(
            Measure()
        )

    #     if measures[cur_measure].find('./barline[@location="left"]/repeat[@direction="forward"]') is not None:
    #         repeat_to = cur_measure
    #     chords += measures[cur_measure].findall('harmony')

    #     if measures[cur_measure].find('./barline[@location="right"]/repeat[@direction="backward"]') is not None:
    #         if take_repeat:
    #             cur_measure = repeat_to
    #             take_repeat = False
    #         else:
    #             cur_measure += 1
    #             take_repeat = True

    #     else:
    #         cur_measure += 1
    
    # for chord in chords:
    #     chord_names.append(chord.find('kind').text)
    
    print(filename)
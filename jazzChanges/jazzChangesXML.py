import xml.etree.ElementTree as ET
import os

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
    measures = [] # each measure in the order (top down left right) they would occur on a lead sheet ignoring repeats, dc, etc
    chords = [] # each chord in the order it OCCURS, accounting for repeats, dc, etc
    ending_chords = [] # separate list for an ending that only occurs last time through (preceding chord + coda)
    # Note that for now I am doing a naive implementation to just get chords after final coda due to coda inconsistencies (see personal notes)
    chord_names = []
    for measure in root.iter('measure'):
        measures.append(measure)

    cur_measure = 0
    repeat_to = 0
    take_repeat = True
    while cur_measure < len(measures):
        if measures[cur_measure].find('./direction/direction-type/coda') is not None:
            last_coda = cur_measure # TODO: handle ds, dc al coda.
            # TODO: not implementing this yet because not sure how to stop normal measure progression from going into the coda.
            # Will work or non-ending roadmap stuff first (ds, dc, 1/2 ending)
        if measures[cur_measure].find('./barline[@location="left"]/repeat[@direction="forward"]') is not None:
            repeat_to = cur_measure
        chords += measures[cur_measure].findall('harmony')

        if measures[cur_measure].find('./barline[@location="right"]/repeat[@direction="backward"]') is not None:
            if take_repeat:
                cur_measure = repeat_to
                take_repeat = False
            else:
                cur_measure += 1
                take_repeat = True

        else:
            cur_measure += 1
    
    for chord in chords:
        chord_names.append(chord.find('kind').text)
    
    print(filename)
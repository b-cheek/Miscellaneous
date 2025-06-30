import xml.etree.ElementTree as ET
import os
from collections import Counter

counters = dict()

semitone_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

def get_semitone(chord):
    return semitone_map[chord.find('./root/root-step').text]\
         + int(chord.find('./root/root-alter').text)

def track_changes(chord_list):
    for i in range(len(chord_list) - 1):
        quality = chord_list[i].find('kind').text
        interval = (get_semitone(chord_list[i + 1]) - get_semitone(chord_list[i])) % 12
        next_quality = chord_list[i + 1].find('kind').text
        if quality not in counters:
            counters[quality] = Counter()
        counters[quality][(interval, next_quality)] += 1

# Parse xml files in MusicXML Lead Sheets folder
for filename in os.listdir('jazzChanges/tough sheets'):
    if filename in ['Cheek To Cheek.musicxml']: # Skip files that cause errors
        continue
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
    for measure in root.iter('measure'):
        measures.append(measure)

    cur_measure = 0
    repeat_to = 0
    repeat_num = 1
    repeat_measure = 0
    # last_coda = -1
    end_at_fine = False
    go_to_coda = False
    coda_measure = 0
    sign_measure = 0
    while cur_measure < len(measures):
        # Check for coda
        if measures[cur_measure].find('./direction/direction-type/coda') is not None:
            # last_coda = cur_measure # TODO: handle ds, dc al coda.
            # TODO: not implementing this yet because not sure how to stop normal measure progression from going into the coda.
            # Will work on non-ending roadmap stuff first (ds, dc, 1/2 ending)
            if go_to_coda:
                cur_measure = coda_measure # Coda should be set to repeat measure, maybe remove coda_measure var
                go_to_coda = False

        # Check for sign
        if measures[cur_measure].find('./direction/direction-type/segno') is not None:
            sign_measure = cur_measure

        # Check for forward repeat
        if measures[cur_measure].find('./barline[@location="left"]/repeat[@direction="forward"]') is not None:
            repeat_to = cur_measure

        # Check for ending
        if (e := measures[cur_measure].find('./barline/ending[@type="start"]')) is not None: 
            if int(e.get('number')) < repeat_num: # Go to correct ending
                cur_measure = repeat_measure + 1 # before adding chord because 1st ending skipped 2nd time
                continue
            if repeat_num == 2: #TODO: is if statement necessary?
                repeat_num = 1
        
        chords += filter(
            lambda chord: chord.find('kind').text != 'none',
            measures[cur_measure].findall('harmony')
        )

        # Check for fine
        if (d := measures[cur_measure].find('./direction/direction-type/words')) is not None:
            if d.text == 'Fine':
                if end_at_fine:
                    break

        # Check for repeat
        if measures[cur_measure].find('./barline[@location="right"]/repeat[@direction="backward"]') is not None:
            if repeat_num == 1:
                repeat_measure = cur_measure
                cur_measure = repeat_to
                repeat_num += 1
            elif repeat_num == 2: # TODO: Would love to generalize this but may not be necessary, >2 ending only seen in dc al 3rd situations
                cur_measure += 1
                repeat_num = 1
            else:
                raise Exception(f'Invalid repeat number: {repeat_num}')

        elif (d := measures[cur_measure].find('./direction/direction-type/words')) is not None: 
        # Check for D.C. / D.S (eventually)
        # I think this can safely be an elif? TODO: check on that
            if d.text == None:
                cur_measure += 1
                continue
            if 'D.' in d.text:
                if d.text == 'D.C. al 3rd':
                    repeat_measure = cur_measure #This gets cur_measure to jump to 3rd ending when it sees 1st ending
                    cur_measure = 0
                    repeat_num = 2 # So the first ending is skipped
                elif d.text == 'D.C. al 2nd': # seems to always have fine right after 2nd ending
                    cur_measure = 0
                    repeat_num = 2
                    end_at_fine = True
                elif d.text == 'D.S. al 2nd':
                    cur_measure = sign_measure
                    repeat_num = 2
                    end_at_fine = True
                elif d.text == 'D.C. al Fine':
                    cur_measure = 0
                    end_at_fine = True
                elif d.text == 'D.C. al Coda':
                    coda_measure = cur_measure + 1
                    cur_measure = 0
                    go_to_coda = True
                elif d.text == 'D.S. al Coda':
                    coda_measure = cur_measure + 1
                    cur_measure = sign_measure
                    go_to_coda = True
                elif d.text == 'D.S. al Fine':
                    cur_measure = sign_measure
                    end_at_fine = True
            # elif d.text == 'Fine':
            #     if end_at_fine:
            #         break
            #     else:
            #         cur_measure += 1
            else:
                cur_measure += 1

        else:
            cur_measure += 1
    
    # Add chord progression to counters
    track_changes(chords)
    
    print(filename)

# Write counter data to a csv file, with separate data sets with interval and next_quality joined and not joined
with open('jazzChanges/counter_data.csv', 'w') as f:
    f.write('quality,interval + next_quality,count,,quality,interval,next_quality,count\n')
    for quality in counters:
        for (interval, next_quality) in counters[quality]:
            f.write(quality + ',' + str(interval) + ' ' + next_quality + ',' + str(counters[quality][(interval, next_quality)]) + ',,'\
                  + quality + ',' + str(interval) + ',' + next_quality + ',' + str(counters[quality][(interval, next_quality)]) + '\n')
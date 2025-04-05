def clean_data(data):
    for i in range(len(data)):
        data[i] = data[i].lstrip()[:-1]

def get_element(element_name: str, data):
    if data == None:
        return None
    for i in range(len(data)):
        if "<" + element_name in data[i]:
            for j in range(i, len(data)):
                if "</" + element_name + ">" in data[j]:
                    if i == j:
                        start = data[j].find(">")
                        end = data[j].rfind("<")
                        element = data[j][start + 1: end]
                    else:
                        element = data[i + 1: j]
                    return element
                    i = j
                    break
    return None

def get_elements(element_name: str, data):
    elements = []
    for i in range(len(data)):
        if "<" + element_name in data[i]:
            for j in range(i, len(data)):
                if "</" + element_name + ">" in data[j]:
                    if i == j:
                        start = data[j].find(">")
                        end = data[j].rfind("<")
                        element = data[j][start + 1: end]
                    else:
                        element = data[i + 1: j]
                    elements.append(element)
                    i = j
                    break
    return elements

def duration_to_int(duration):
    if duration == "whole":
        return 1.0
    if duration == "half":
        return 0.5
    if duration == "quarter":
        return 0.25
    if duration == "eighth":
        return 0.125
    if duration == "sixthteenth":
        return 0.0625

def chord_to_note(chord_data):
    note_value = duration_to_int(get_element("durationType", chord_data))
    multiplier = get_element("dots", chord_data)
    if multiplier == "1":
        note_value *= 1.5
    if multiplier == None:
        pass
    pitch = int(get_element("pitch", chord_data))
    note = [pitch, note_value]
    return note

def separate_top_staff(measures_data):
    pieces = []
    start = 0
    for i in range(len(measures_data)):
        if get_element("subtype", get_element("BarLine", measures_data[i])) == "end":
            pieces.append(measures_data[start: i + 1])
            start = i + 1
    return pieces

def separate_bottom_staff(organized_staff, unorganized_staff):
    new = []
    start = 0
    for piece in organized_staff:
        new.append(unorganized_staff[start: start + len(piece)])
        start = start + len(piece)
    return new

def separate_voices(measure_data):
    chords = get_elements("Chord", measure_data)
    top_voice = []
    bottom_voice = []
    for chord in chords:
        if get_element("track", chord) == None:
            top_voice.append(chord)
        else:
            bottom_voice.append(chord)
    return [top_voice, bottom_voice]

def staff_to_notes(separated_staff):
    notes = []
    for piece in separated_staff:
        soprano = []
        alto = []
        for measure in piece:
            voices = separate_voices(measure)
            top_voice = voices[0]
            bottom_voice = voices[1]
            soprano_measure = []
            alto_measure = []
            for chord in top_voice:
                note = chord_to_note(chord)
                soprano_measure.append(note)
            for chord in bottom_voice:
                note = chord_to_note(chord)
                alto_measure.append(note)
            soprano.append(soprano_measure)
            alto.append(alto_measure)
        notes.append([soprano, alto])
    return notes

def data_to_notes(data):
    clean_data(data)
    Staves = get_elements("Staff", data)
    bottom_staff = Staves[-1]
    top_staff = Staves[-2]
    bottom_staff_measures = get_elements("Measure", bottom_staff)
    top_staff_measures = get_elements("Measure", top_staff)
    separated_top_staff = separate_top_staff(top_staff_measures)
    separated_bottom_staff = separate_bottom_staff((separated_top_staff), bottom_staff_measures)
    top_notes = staff_to_notes(separated_top_staff)
    bottom_notes = staff_to_notes(separated_bottom_staff)
    notes = []
    for i in range(len(top_notes)):
        top_piece = top_notes[i]
        bottom_piece = bottom_notes[i]
        notes.append(top_piece + bottom_piece)
    return notes   

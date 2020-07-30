# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

#NOTE_RESOLUTION = .02

# a small gap between notes that ensures the off notes fire before the on notes
NOTE_GAP = 0.01


from .. model.event import Event, NOTE_ON, NOTE_OFF
from .. model.chord import Chord
from .. model.note import Note

def evaluate_ties(note_list):

    # note_list is like [[ n1, n2, n3], [n4], [n5, n6]]

    results = []
    previous_notes = None

    for n in note_list:
        is_tie = False

        if n is None or len(n) == 0:
            results.append([])
        elif n[0] is None:
            results.append([])
        elif n[0].tie:
            is_tie = True

            if previous_notes is not None:
                for m in previous_notes:
                    m.length = m.length + n[0].length
            else:
                continue
            results.append([])
        else:
            results.append(n)

        if not is_tie:
            previous_notes = n

    return results

def evaluate_shifts(note_list, octave_shift, degree_shift, scale, scale_shift):
    if octave_shift == 0 and degree_shift == 0 and scale_shift == 0:
        #print("BAILING!")
        return note_list
    results = []
    for chord in note_list:
        chord_items = []
        for note in chord:
            n1 = None
            if octave_shift or scale_shift:
                n1 = note.transpose(octaves=octave_shift, degrees=degree_shift)
            if scale_shift:
                n1 = note.scale_transpose(scale, scale_shift)
            chord_items.append(n1)
        results.append(chord_items)
    return results

def round_partial(value, resolution):
    return round(value / resolution) * resolution

def chord_list_to_notes(old_list):

    results = []
    for x in old_list:

        bucket = []

        if type(x) == Chord:
            bucket = x.notes

        elif type(x) == list:

            for value in x:
                if type(value) == Chord:
                    bucket.extend(value.notes)
                else:
                    bucket.append(value)

        elif type(x) == Note:
            bucket.append(x)

        results.append(bucket)

    return results

def flatten(old_list):

    # incoming is a list of notes: [n1, n2, n3], [n4], [], [n5, n6]
    # output: [ n1, n2, n3, n4, n5, n6 ]

    results = []
    for x in old_list:
        for y in x:
            results.append(y)
    return results

def notes_to_events(clip, note_list): #, resolution=NOTE_RESOLUTION):

    # takes a note list like
    # [[n1, n2, n3], [n4, n5]]
    #
    # and returns a event list like:
    #
    # [e1_on, e2_on, e3_on], [], [], [e1_off, e2_off, e3_off], [], ...
    #
    # with a finer granularity than the original input stream based on NOTE_RESOLUTION

    results = []
    note_list = flatten(note_list)
    events = []

    for in_note in note_list:

        from .. model.chord import Chord
        from .. model.note import Note

        my_notes = None
        if type(in_note) == Note:
            my_notes = [ in_note ]
        elif type(in_note) == Chord:
            # an arp can sometimes generate chords from raw notes
            my_notes = in_note.notes
        else:
            raise Exception("unexpected input: %s" % note)

        for note in my_notes:

            event1 = Event(type=NOTE_ON, note=note, time=note.start_time, scale=note.from_scale)

            if event1.note.octave > clip.track.instrument.max_octave:
                event1.note.octave = clip.track.instrument.max_octave
            if event1.note.octave < clip.track.instrument.min_octave:
                event1.note.octave = clip.track.instrument.min_octave

            events.append(event1)

            event2 = Event(type=NOTE_OFF, note=note, time=note.end_time - NOTE_GAP, scale=note.from_scale, on_event=event1)
            events.append(event2)

    def sorter(event):

        if event.type == NOTE_OFF:
            return event.time - 0.0001

        return event.time

    events.sort(key=sorter)

    return events


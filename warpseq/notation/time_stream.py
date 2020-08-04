# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# various low level functions broken out of clip.py for clip evaluation
# (these could use some cleanup)

# a small gap between notes that ensures the off notes fire before the on notes
NOTE_GAP = 0.01

from ..api.exceptions import *
from ..model.chord import Chord
from ..model.event import NOTE_OFF, NOTE_ON, Event
from ..model.note import Note


# TODO: we can merge this with chord_list_to_notes and create less arrays
JUNK="""
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
"""

def _add_note_to_bucket(this_bucket, note, scale, t_start):
    note.from_scale = scale
    note.start_time = t_start
    #print("TS======%s" % note.start_time)
    note.end_time = round(t_start + note.length)
    #print("NS=%s/%s" % (note.start_time, note.end_time))
    note.from_scale = scale
    this_bucket.append(note)


def standardize_notes(old_list, scale, slot_duration, t_start):

    results = []
    previous_notes = []

    # incoming is a list of things that happen in each slots (each is a list)
    # each item may be a list of notes
    # or a chord
    # or a list containing ONE chord - which must be broken into notes

    for slot in old_list:

        this_bucket = []
        is_tie = False

        for obj in slot:

            if type(obj) == Chord:
                for note in obj.notes:
                    _add_note_to_bucket(this_bucket, note, scale, t_start)

            elif type(obj) == Note:
                if not obj.tie:
                    _add_note_to_bucket(this_bucket, obj, scale, t_start)
                else:
                    is_tie = True

            elif obj is not None:
                raise Exception("unexpected: %s" % obj)

        if is_tie:
            for p in previous_notes:
                p.length = p.length + slot_duration
        else:
            previous_notes = this_bucket

        results.append(this_bucket)

        t_start = t_start + slot_duration

    return results



def notes_to_events(clip, note_list): #, resolution=NOTE_RESOLUTION):

    # takes a note list like
    # [[n1, n2, n3], [n4, n5]]
    #
    # and returns a event list like:
    #
    # [e1_on, e2_on, e3_on], [], [], [e1_off, e2_off, e3_off], [], ...

    from ..model.chord import Chord
    from ..model.note import Note

    events = []

    max_o = clip.track.instrument.max_octave
    min_o = clip.track.instrument.min_octave

    for slot in note_list:

        for in_note in slot:

            if not in_note:
                my_notes = []
            elif type(in_note) == Note:
                my_notes = [ in_note ]
            else: # assume Chord
                my_notes = in_note.notes

            for note in my_notes:

                if note is not None and not note.tie:

                    event1 = Event(type=NOTE_ON, note=note, time=note.start_time, scale=note.from_scale)
                    if note.octave > max_o:
                        note.octave = max_o
                    if note.octave < min_o:
                        note.octave = min_o
                    events.append(event1)

                    event2 = Event(type=NOTE_OFF, note=note, time=note.end_time, scale=note.from_scale, on_event=event1)
                    events.append(event2)

                    event1.off_event = event2


    return events

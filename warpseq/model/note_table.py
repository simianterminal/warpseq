# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this is some support code for Note that can really be folded back into
# Note.

NOTE_TABLE = [
    ['C',0], ['Db',0], ['D',0], ['Eb',0], ['E',0], ['F',0], ['Gb',0], ['G',0], ['Ab',0], ['A',0], ['Bb',0], ['B',0],
    ['C',1], ['Db',1], ['D',1], ['Eb',1], ['E',1], ['F',1], ['Gb',1], ['G',1], ['Ab',1], ['A',1], ['Bb',1], ['B',1],
    ['C',2], ['Db',2], ['D',2], ['Eb',2], ['E',2], ['F',2], ['Gb',2], ['G',2], ['Ab',2], ['A',2], ['Bb',2], ['B',2],
    ['C',3], ['Db',3], ['D',3], ['Eb',3], ['E',3], ['F',3], ['Gb',3], ['G',3], ['Ab',3], ['A',3], ['Bb',3], ['B',3],
    ['C',4], ['Db',4], ['D',4], ['Eb',4], ['E',4], ['F',4], ['Gb',4], ['G',4], ['Ab',4], ['A',4], ['Bb',4], ['B',4],
    ['C',5], ['Db',5], ['D',5], ['Eb',5], ['E',5], ['F',5], ['Gb',5], ['G',5], ['Ab',5], ['A',5], ['Bb',5], ['B',5],
    ['C',6], ['Db',6], ['D',6], ['Eb',6], ['E',6], ['F',6], ['Gb',6], ['G',6], ['Ab',6], ['A',6], ['Bb',6], ['B',6],
    ['C',7], ['Db',7], ['D',7], ['Eb',7], ['E',7], ['F',7], ['Gb',7], ['G',7], ['Ab',7], ['A',7], ['Bb',7], ['B',7],
    ['C',8], ['Db',8], ['D',8], ['Eb',8], ['E',8], ['F',8], ['Gb',8], ['G',8], ['Ab',8], ['A',8], ['Bb',8], ['B',8],
    ['C',9], ['Db',9], ['D',9], ['Eb',9], ['E',9], ['F',9], ['Gb',9], ['G',9], ['Ab',9], ['A',9], ['Bb',9], ['B',9],
    ['C',10], ['Db',10], ['D',10], ['Eb',10], ['E',10], ['F',10], ['Gb',10], ['G',10], ['Ab',10], ['A',10], ['Bb',10], ['B',10],
    ['C',11], ['Db',11], ['D',11], ['Eb',11], ['E',11], ['F',11], ['Gb',11], ['G',11], ['Ab',11], ['A',11], ['Bb',11], ['B',11],
    ['C',12], ['Db',12], ['D',12], ['Eb',12], ['E',12], ['F',12], ['Gb',12], ['G',12], ['Ab',12], ['A',12], ['Bb',12], ['B',12],

    ['C', 13], ['Db', 13], ['D', 13], ['Eb', 13], ['E', 13], ['F', 13], ['Gb', 13], ['G', 13], ['Ab', 13], ['A', 13], ['Bb', 13], ['B', 13],
    ['C', 14], ['Db', 14], ['D', 14], ['Eb', 14], ['E', 14], ['F', 14], ['Gb', 14], ['G', 14], ['Ab', 14], ['A', 14], ['Bb', 14], ['B', 14],
    ['C', 15], ['Db', 15], ['D', 15], ['Eb', 15], ['E', 15], ['F', 15], ['Gb', 15], ['G', 15], ['Ab', 15], ['A', 15], ['Bb', 15], ['B', 15],

]

def offset(note, tones):

    # this supports fractional semitones, like 1.5

    # FIXME: this implementation is **TEMPORARY** and can be implemented without the table - when removed, delete this file

    if tones == 0:
        return note
    steps = 2 * tones
    steps = int(steps)
    n1 = note.copy()
    note_index = n1.note_number()
    new_note_index = note_index + steps
    try:
        lookup = NOTE_TABLE[new_note_index]
    except IndexError:
        print("FAILED INDEX: %s" % new_note_index)
        return note
    n1.name = lookup[0]
    n1.octave = lookup[1]
    return n1

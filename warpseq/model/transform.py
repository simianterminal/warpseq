# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a transform is a list of modifier expressions that can be used
# to build MIDI effects including Arps.

from ..notation.mod import ModExpression
from ..utils.utils import roller
from .base import NewReferenceObject


CHORDS = 'chords'
NOTES = 'notes'
BOTH = 'both'
APPLIES_CHOICES = [ CHORDS, NOTES, BOTH ]

class Transform(NewReferenceObject):

    __slots__ = [ 'name', 'slots', 'octave_slots', 'divide', 'applies_to', 'obj_id', '_mod', '_slot_mods' ]

    def __init__(self, name=None, slots=None, octave_slots=None, divide=1, obj_id=None, applies_to=None):
        self.name = name
        self.slots = slots
        self.octave_slots = octave_slots
        self.divide = divide
        self.applies_to = applies_to
        self.obj_id = obj_id
        self._mod = ModExpression(defer=False)
        self._slot_mods = roller(slots)

        if applies_to is None:
            applies_to = BOTH
        self.applies_to = applies_to

        assert applies_to in APPLIES_CHOICES

        super(Transform, self).__init__()


    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots,
            octave_slots = self.octave_slots,
            applies_to = self.applies_to,
            divide = self.divide
        )

    @classmethod
    def from_dict(cls, song, data):
        return Transform(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots'],
            octave_slots = data['slots'],
            applies_to = data.get('applies_to', None),
            divide = data.get('divide', None)
        )

    def process(self, scale, track, note_list, t_start, slot_duration):


        """
        Given a list of notes or chords, apply the transform expressions in *slots* to produce
        a new list of notes or chords.
        """

        from .note import Note

        self._mod.scale = scale
        self._mod.track = track

        # notes is like: [n1, n2, n3], [n4], [], [n5, n6]
        # for each slot, we divide it by _divide_
        # record the first note start time and first note end time
        # get the delta between start and end, divide by _divide_
        # tick through the start to end times incrementing by delta/_divide_ (new_note_width)
        # at each step, adjust by the values in slots, as a mod expression
        # compute the new note list for this particular slot
        # move to the next slot

        new_note_list = []
        applies_to = self.applies_to

        # TODO: consider a roller option that does not reset at the pattern boundary, but survives between patterns?
        # could be musically interesting for odd lengths

        #slot_modifications = roller(self.slots)

        #slot_duration = clip.

        start_time = t_start

        for notes2 in note_list:

            (actual_notes, is_chord) = _expand_notes(notes2)

            divide = self.divide

            if divide is None:
                # constructs an arp like transform that plays every note within the given slot time
                divide = len(actual_notes)

            skip = False
            chord_skip = False
            if is_chord:
                # leave chords unaffected if requested
                if applies_to not in [ BOTH, CHORDS ]:
                    skip = True
                    chord_skip = True
                    divide = 1
            else:
                # leave notes unaffected if requested
                if applies_to not in [ BOTH, NOTES ]:
                    skip = True
                    divide = 1



            if chord_skip:
               new_note_list.append(actual_notes)

            else:

                notes = actual_notes

                #new_notes = []


                if not notes: # None + len == 0:
                    # we don't attempt to transform rests
                    new_note_list.append([])
                    start_time = start_time + slot_duration
                    continue

                # compute the new time information for the divided notes


                new_delta = round(slot_duration / divide)

                # roll_notes picks values off the incoming note/chord list, it happens once each time a 'divide'
                # is looped through
                roll_notes = roller(notes)

                i_ct = 0

                for _ in range(0, divide):

                    i_ct = i_ct + 1

                    # grab a note that is playing from all notes that are playing
                    which_note = next(roll_notes) # .copy()

                    # apply the new time information

                    which_slot = next(self._slot_mods)

                    # calculate the new note using the mod expression

                    if not skip:
                        final_note = self._mod.do(which_note, which_slot)
                        if final_note is None:
                            continue
                    else:
                        # this handles if the transform was set to skip chords or skip individual notes
                        final_note = which_note.copy()

                    adjust_notes = [ final_note ]

                    if type(final_note) == Note:
                        final_note.start_time = start_time
                        final_note.end_time = round(start_time + (i_ct * new_delta))
                        final_note.length = new_delta
                    else:
                        # the transform *produced* a new chord
                        for x in final_note.notes:
                            x.start_time = start_time
                            x.end_time = round(start_time + (i_ct * new_delta))
                            x.length = new_delta

                    start_time = start_time + new_delta

                    # we return an array here based on further code in the pipeline expecting one
                    # this could probably use some cleanup for consistency.  The final_note object
                    # can technically be a Chord and not a note.

                    if type(final_note) == Note:
                        new_note_list.append([final_note])
                    else:
                        new_note_list.append(final_note.notes)

        # the new note list is the result of applying the transform. Because of the divides, the new
        # note list can be longer than the incoming note list, but each note in the list has time information.
        #
        # [[n1],[n2],[n3],[n4],[n5]]

        #print("------> NNL=%s" % new_note_list)
        return new_note_list

def _expand_notes(notes):

    # the list of notes coming out the system per step can look like:
    # [None] - a rest
    # [n1] - a single note
    # [n1,n2] - a bunch of arbitrary notes, usually from an extracted chord
    # [chord] - a chord object, usually from a transform that was not yet extracted
    # we need to convert this unilaterally to a list of notes

    from .note import Note
    from .chord import Chord

    # returns the notes and whether or not a chord was found

    ln = len(notes)

    if ln == 0:
        return (notes, False)

    n1 = notes[0]

    if type(n1) == Note:
        if ln == 1:
            return (notes, False)
        else:
            return (notes, True)

    # assume Chord - the system *cannot* return a list of multiple chords at present, but if it does
    # we'll need to remember to update this

    assert len(notes) == 1

    # the system should not construct a chord of only one note, so this shortcut is probably ok

    return (notes[0].notes, True)

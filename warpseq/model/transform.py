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

class Transform(NewReferenceObject):

    __slots__ = [ 'name', 'slots', 'octave_slots', 'divide', 'obj_id', "_mod", "_slot_mods" ]

    def __init__(self, name=None, slots=None, octave_slots=None, divide=1, obj_id=None):
        self.name = name
        self.slots = slots
        self.octave_slots = octave_slots
        self.divide = divide
        self.obj_id = obj_id
        self._mod = ModExpression(defer=False)
        self._slot_mods = roller(slots)

        super(Transform, self).__init__()


    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots,
            octave_slots = self.octave_slots
        )

    @classmethod
    def from_dict(cls, song, data):
        return Transform(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots'],
            octave_slots = data['slots']
        )

    def process(self, scale, track, note_list, t_start):

        """
        Given a list of notes or chords, apply the transform expressions in *slots* to produce
        a new list of notes or chords.
        """

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

        divide = self.divide
        new_note_list = []

        # TODO: consider a roller option that does not reset at the pattern boundary, but survives between patterns?
        # could be musically interesting for odd lengths

        #slot_modifications = roller(self.slots)

        #slot_duration = clip.

        start_time = t_start

        for notes in note_list:

            new_notes = []

            if len(notes) == 0:
                new_note_list.append(new_notes)
                continue

            # compute the new time information for the divided notes


            old_delta = notes[0].end_time - notes[0].start_time
            new_delta = round(old_delta / divide)

            # roll_notes picks values off the incoming note/chord list, it happens once each time a 'divide'
            # is looped through
            roll_notes = roller(notes)

            #start_time = notes[0].start_time

            for _ in range(0, divide):

                # grab a note that is playing from all notes that are playing
                which_note = next(roll_notes) # .copy()

                # apply the new time information


                # grab the next mod expression from this transform
                which_slot = next(self._slot_mods)

                # calculate the new note using the mod expression

                final_note = self._mod.do(which_note, which_slot)
                if final_note is None:
                    continue

                final_note.start_time = start_time
                final_note.end_time = start_time + new_delta
                final_note.length = new_delta

                start_time = start_time + new_delta

                # we return an array here based on further code in the pipeline expecting one
                # this could probably use some cleanup for consistency.  The final_note object
                # can technically be a Chord and not a note.

                new_note_list.append([final_note])

        # the new note list is the result of applying the transform. Because of the divides, the new
        # note list can be longer than the incoming note list, but each note in the list has time information.
        #
        # [[n1],[n2],[n3],[n4],[n5]]

        return new_note_list

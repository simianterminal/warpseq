from . base import ReferenceObject
from classforge import Class, Field
from .. utils.utils import roller
from .. notation.mod import ModExpression

class Arp(ReferenceObject):

    name = Field(type=str, required=True, nullable=False)
    slots = Field(type=list, default=None)
    octave_slots = Field(type=list, default=None)
    divide = Field(type=int, default=1, nullable=False)

    def on_init(self):
        # self._buffer = [ x for x in self.slots ]
        pass

    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots,
            octave_slots = self.octave_slots
        )

    @classmethod
    def from_dict(cls, song, data):
        return Arp(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots'],
            octave_slots = data['slots']
        )


    def process(self, song, scale, track, note_list):

        mod_expr = ModExpression()

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
        #print("ARP INPUT: %s" % note_list)

        # FIXME: we might want to have an option that resets the arp for arps not of the same length as divide
        # but right now, leaving this as is.

        slot_modifications = roller(self.slots)

        for notes in note_list:

            # print("ARP PROCESSING STEP: %s" % notes)

            new_notes = []

            if len(notes) == 0:
                new_note_list.append(new_notes)
                continue


            old_delta = notes[0].end_time - notes[0].start_time
            new_delta = round(old_delta / divide)
            #print("NEW_DELTA=%s" % new_delta)

            assert new_delta > 0

            roll_notes = roller(notes)

            start_time = notes[0].start_time

            for divisions in range(0, divide):

                which_note = next(roll_notes).copy()

                which_note.start_time = start_time
                which_note.end_time = start_time + new_delta
                which_note.length = new_delta

                #print("WN=%s/%s/%s" % (which_note.start_time, which_note.end_time, which_note.length))

                which_slot = next(slot_modifications)

                final_note = mod_expr.do(which_note, scale, track, which_slot)
                if final_note is None:
                    # print("MOD EXPRESSION SILENCED: %s" % which_slot)
                    continue

                # FIXME: while not possible now, in the future mod_expressions could return a chord
                # (and this would be awesome)
                # if so, we must insert all the notes in the chord

                start_time = start_time + new_delta

                # we return an array here based on the existing non-arpeggiated code path possibly returning
                # chords.  It's also true that eventually this MAY support returning chords FROM the arp
                # and if so, we need to return a list here anyway

                assert final_note.start_time is not None
                assert final_note.end_time is not None

                new_note_list.append([final_note])
                # print("ARP PRODUCED: %s" % final_note)


        # generate an iterator that rolls around the slots
        #


        return new_note_list


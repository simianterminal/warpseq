from . base import ReferenceObject
from classforge import Class, Field

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


    def process(self, song, note_list):
        print("** FIXME **: arpeggiator is not implemented **")

        # generate an iterator that rolls around the slots
        #


        return note_list


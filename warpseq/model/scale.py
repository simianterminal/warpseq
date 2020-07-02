from . base import BaseObject
from classforge import Class, Field

class Scale(BaseObject):

    name = Field(type=str, required=True, nullable=False)

    root = Field(type=str, required=True, nullable=False)
    octave = Field(type=int, required=False, nullable=True, default=None)

    slots = Field(type=list, required=True, nullable=False)

    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name,
            root = self.root,
            octave = self.octave,
            slots = self.slots
        )

    @classmethod
    def from_dict(cls, song, data):
        return Scale(
            obj_id = data['obj_id'],
            name = data['name'],
            root = data['root'],
            octave = data['octave'],
            slots = data['slots']
        )

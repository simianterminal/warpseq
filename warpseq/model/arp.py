from . base import BaseObject
from classforge import Class, Field

class Arp(BaseObject):

    name = Field(type=str, required=True, nullable=False)
    slots = Field(type=list, default=[])

    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots
        )

    @classmethod
    def from_dict(cls, song, data):
        return Arp(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots']
        )
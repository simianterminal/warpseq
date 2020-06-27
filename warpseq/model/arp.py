from . base import BaseObject
from classforge import Class, Field

class Arp(BaseObject):

    name = Field(type=str, required=True, nullable=False)
    slots = Field(type=list, default=[])

    def to_dict(self):
        return dict(
            name = self.name,
            slots = self.slots
        )

    @classmethod
    def from_dict(cls, song, data):
        return Arp(
            name = data['name'],
            slots = data['slots']
        )
from .base import ReferenceObject
from classforge import Class, Field
from .scale import Scale
from .arp import Arp

FORWARD='forward'
REVERSE='reverse'

DIRECTIONS = [
    FORWARD,
    REVERSE
]

class Pattern(ReferenceObject):

    name = Field(required=True, nullable=False)
    slots = Field(type=list)
    length = Field(type=int, default=None, nullable=True)

    arp = Field(type=Arp, default=None, nullable=True)
    tempo = Field(type=int, default=None, nullable=True)
    scale = Field(type=Scale, default=None, nullable=True)

    def on_init(self):
        super().on_init()

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots,
            length = self.length,
            tempo = self.tempo
        )
        if self.arp:
            result['arp'] = arp.name
        else:
            result['arp'] = None
        if self.scale:
            result['scale'] = scale.obj_id
        else:
            result['scale'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Pattern(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots'],
            length = data['length'],
            arp = song.find_arp(data['arp']),
            tempo = data['tempo'],
            scale = song.find_scale(data['scale'])
        )
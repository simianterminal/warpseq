from .base import BaseObject
from .pattern import Pattern
from classforge import Class, Field
from .arp import Arp
from .scale import Scale

class Clip(BaseObject):

    name = Field(type=str, required=True, nullable=False)
    scale = Field(type=Scale, required=False, nullable=True, default=None)
    pattern = Field(type=Pattern, required=False, default=None, nullable=True)
    length = Field(type=int, default=None, required=False, nullable=True)
    arp = Field(type=Arp, default=None, nullable=True)
    tempo = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=-1, nullable=True)

    def to_dict(self):
        result = dict(
            name = self.name,
            length = self.length,
            tempo = self.tempo,
            repeat = self.repeat
        )
        if self.pattern:
            result['pattern'] = self.pattern.name
        else:
            result['pattern'] = None
        if self.arp:
            result['arp'] = self.arp.name
        else:
            result['arp'] = None
        if self.scale:
            result['scale'] = self.scale.name
        else:
            result['scale'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Clip(
            name = data['name'],
            scale = song.find_scale(data['scale']),
            pattern = song.find_pattern(data['pattern']),
            length = data['length'],
            arp = song.find_arp(data['arp']),
            tempo = data['tempo'],
            repeat = data['repeat']
        )

    def get_effective_scale(self, scene=None, song=None):
        assert song is not None
        assert scale is not None
        # ask the clip, then pattern, then scene, then the song...
        raise NotImplementedError()

    def get_effective_arpegiattor(self):
        assert song is not None
        assert scale is not None
        # ask the clip, then pattern, then scene, then the song...
        raise NotImplementedError()

    def get_effective_tempo(self, scene=None, song=None):
        assert song is not None
        assert scale is not None
        # ask the clip, then pattern, then the scene, then the song...
        raise NotImplementedError()



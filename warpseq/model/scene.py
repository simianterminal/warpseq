from . base import BaseObject
from classforge import Class, Field

class Scene(BaseObject):

    from . scale import Scale

    name = Field(type=str, required=True, nullable=False)
    tempo = Field(type=int, default=None, nullable=True)
    scale = Field(type=Scale, default=None, nullable=True)

    auto_advance = Field(type=bool, default=None, nullable=True)
    measure_length = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=None, nullable=True)

    def to_dict(self):
        result = dict(
            name = self.name,
            tempo = self.tempo,
            auto_advance = self.auto_advance,
            measure_length = self.measure_length,
            repeat = self.repeat
        )
        if self.scale:
            result['scale'] = self.scale.name
        else:
            result['scale'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Scene(
            name = data['name'],
            tempo = data['tempo'],
            scale = song.find_scale(data['scale']),
            auto_advance = data['auto_advance'],
            measure_length = data['measure_length'],
            repeat = data['repeat']
        )
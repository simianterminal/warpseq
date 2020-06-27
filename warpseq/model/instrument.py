from .base import BaseObject
from classforge import Class, Field
from .device import Device

class Instrument(BaseObject):

    name = Field(type=str, required=True, nullable=False)
    channel = Field(type=int, required=True)
    device = Field(type=Device, required=False)

    min_octave = Field(type=int, required=False, default=0, nullable=False)
    base_octave = Field(type=int, required=True, default=3, nullable=False)
    max_octave = Field(type=int, required=True, default=8, nullable=False)

    def to_dict(self):
        result = dict(
            name = self.name,
            channel = self.channel,
            min_octave = self.min_octave,
            base_octave = self.base_octave,
            max_octave = self.max_octave
        )
        if self.device:
            result['device'] = self.device.name
        else:
            result['device'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Instrument(
            name = data['name'],
            channel = data['channel'],
            device = song.find_device(data['device']),
            min_octave = data['min_octave'],
            base_octave = data['base_octave'],
            max_octave = data['max_octave']
        )
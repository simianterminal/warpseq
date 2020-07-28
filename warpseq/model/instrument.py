from .base import ReferenceObject
from classforge import Class, Field
from .device import Device

class Instrument(ReferenceObject):

    name = Field(type=str, required=True, nullable=False)
    channel = Field(type=int, required=True)
    device = Field(type=Device, required=False)

    min_octave = Field(type=int, required=False, default=0, nullable=False)
    base_octave = Field(type=int, required=True, default=3, nullable=False)
    max_octave = Field(type=int, required=True, default=8, nullable=False)
    default_velocity = Field(type=int, required=False, default=120, nullable=False)
    muted = Field(type=bool, required=False, default=False, nullable=False)

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            channel = self.channel,
            min_octave = self.min_octave,
            base_octave = self.base_octave,
            max_octave = self.max_octave,
            default_velocity = self.default_velocity,
            muted = self.muted
        )
        if self.device:
            result['device'] = self.device.obj_id
        else:
            result['device'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Instrument(
            obj_id = data['obj_id'],
            name = data['name'],
            channel = data['channel'],
            device = song.find_device(data['device']),
            min_octave = data['min_octave'],
            base_octave = data['base_octave'],
            max_octave = data['max_octave'],
            default_velocity = data['default_velocity'],
            muted = data['muted']
        )
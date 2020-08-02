# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# an instrument adds a channel number to a MIDI device and has some
# parameters around supported note ranges. It can also be muted.

from classforge import Class, Field

from .base import NewReferenceObject
from .device import Device


class Instrument(NewReferenceObject):

    __slots__ = [ 'name', 'channel', 'device', 'min_octave', 'base_octave', 'max_octave', 'default_velocity', 'muted' ]

    def __init__(self, name=None, channel=None, device=None, min_octave=0, base_octave=3, max_octave=10, default_velocity=120, muted=False, obj_id=None):
        self.name = name
        self.channel = channel
        self.device = device
        self.min_octave = min_octave
        self.base_octave = base_octave
        self.max_octave = max_octave
        self.default_velocity = default_velocity
        self.muted = muted
        self.obj_id = obj_id

        super(Instrument,self).__init__()


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

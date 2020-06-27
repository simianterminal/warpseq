from . base import BaseObject
from classforge import Class, Field
from . instrument import Instrument

class Track(BaseObject):

    name = Field(type=str, required=True, nullable=False)

    muted = Field(type=bool, required=False, default=False)
    instrument = Field(type=Instrument, required=True, nullable=False)

    def to_dict(self):
        data = dict(
            name = self.name,
            muted = self.muted,
            instrument = self.instrument.name
        )
        return data


    @classmethod
    def from_dict(cls, song, data):
        return Track(
            name = data['name'],
            muted = data['muted'],
            instrument = song.find_instrument(data['instrument'])
        )
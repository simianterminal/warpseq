# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a device represents a physical or virtual MIDI interface

from classforge import Class, Field

from .base import ReferenceObject


class Device(ReferenceObject):

    name = Field(type=str, required=True)

    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name
        )

    @classmethod
    def from_dict(cls, song, data):
        return Device(
            obj_id = data['obj_id'],
            name = data['name']
        )

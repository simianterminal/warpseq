# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a device represents a physical or virtual MIDI interface

from classforge import Class, Field

from .base import NewReferenceObject

class Device(NewReferenceObject):

    __slots__ = [ 'name', 'obj_id' ]

    def __init__(self, name=None, obj_id=None):
        self.name = name
        self.obj_id = obj_id
        super(Device,self).__init__()

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

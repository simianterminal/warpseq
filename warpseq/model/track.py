# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a track is a vertical row of clips that share a common instrument.
# a track can also be muted.

from .base import NewReferenceObject
from .instrument import Instrument

class Track(NewReferenceObject):

    __slots__ = [ 'name', 'muted', 'instrument', 'clip_ids', 'obj_id' ]

    def __init__(self, name=None, muted=False, instrument=None, clip_ids=None, obj_id=None):
        self.name = name
        self.muted = muted
        self.instrument = instrument
        self.clip_ids = clip_ids
        self.obj_id = obj_id


        if self.clip_ids is None:
            self.clip_ids = []

        super(Track, self).__init__()

    def has_clip(self, clip):
        """
        Is this clip part of this track?
        """
        assert clip is not None
        return clip.obj_id in self.clip_ids

    def add_clip(self, clip):
        """
        Adds a clip to a track.  Use from song.py - not directly.
        """
        assert clip is not None
        if clip.obj_id not in self.clip_ids:
            self.clip_ids.append(clip.obj_id)

    def remove_clip(self, clip):
        """
        Remove a clip from this track. Use from song.py - not directly.
        """
        assert clip is not None
        self.clip_ids = [ c for c in self.clip_ids if c != clip.obj_id ]

    def to_dict(self):
        data = dict(
            obj_id = self.obj_id,
            name = self.name,
            muted = self.muted,
            instrument = self.instrument.obj_id,
            clip_ids = self.clip_ids,
        )
        return data


    @classmethod
    def from_dict(cls, song, data):

        instrument = song.find_instrument(data['instrument'])
        assert instrument is not None

        return Track(
            obj_id = data['obj_id'],
            name = data['name'],
            muted = data['muted'],
            instrument = instrument,
            clip_ids = data['clip_ids']
        )

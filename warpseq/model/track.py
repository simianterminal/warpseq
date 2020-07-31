# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a track is a vertical row of clips that share a common instrument.
# a track can also be muted.

from . base import ReferenceObject
from classforge import Class, Field
from . instrument import Instrument

class Track(ReferenceObject):

    name = Field(type=str, required=True, nullable=False)

    muted = Field(type=bool, required=False, default=False)
    instrument = Field(type=Instrument, required=True, nullable=False)

    # internal state
    clip_ids = Field(type=list, default=None, required=False, nullable=False)

    def on_init(self):
        """
        Allocates internal storage so the track can know what clips are included.
        """
        if self.clip_ids is None:
            self.clip_ids = []
        super().on_init()

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
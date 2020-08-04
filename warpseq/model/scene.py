# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a scene is a set of clips that usually play together at the same time.

from .base import NewReferenceObject

class Scene(NewReferenceObject):

    from . scale import Scale

    __slots__ = [ 'scene', 'name', 'scale', 'auto_advance', 'rate', 'clip_ids', 'obj_id' ]

    def __init__(self, name=None, scene=None, scale=None, auto_advance=False, rate=1, clip_ids=None, obj_id=None):
        self.name = name
        self.scene = scene
        self.scale = scale
        self.auto_advance = auto_advance
        self.rate = rate
        self.clip_ids = clip_ids
        self.obj_id = obj_id

        if self.clip_ids is None:
            self.clip_ids = []

        super(Scene, self).__init__()

    def clips(self, song):
        """
        Return the clips in the scene.
        """
        results = [ song.find_clip(x) for x in self.clip_ids ]
        results = [ r for r in results if r is not None ]
        return results

    def add_clip(self, clip):
        """
        Add a clip to the scene.  This is used by song.py and should not
        be called directly.
        """
        if clip.obj_id not in self.clip_ids:
            self.clip_ids.append(clip.obj_id)

    def has_clip(self, clip):
        """
        Is a clip part of this scene?
        """
        return clip.obj_id in self.clip_ids

    def remove_clip(self, clip):
        """
        Disassociate a clip from this scene.  This is used by song.py and should
        not be used directly.
        """
        self.clip_ids = [ c for c in self.clip_ids if c != clip.obj_id ]

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            auto_advance = self.auto_advance,
            clip_ids = self.clip_ids,
            rate = self.rate,
        )
        if self.scale:
            result['scale'] = self.scale.obj_id
        else:
            result['scale'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Scene(
            obj_id = data['obj_id'],
            name = data['name'],
            scale = song.find_scale(data['scale']),
            auto_advance = data['auto_advance'],
            clip_ids = data['clip_ids'],
            rate = data["rate"],
        )

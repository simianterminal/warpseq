from . base import ReferenceObject
from classforge import Class, Field

class Scene(ReferenceObject):

    from . scale import Scale

    name = Field(type=str, required=True, nullable=False)
    scale = Field(type=Scale, default=None, nullable=True)
    auto_advance = Field(type=bool, default=True, nullable=False)
    rate = Field(type=float, default=1, nullable=False)

    # internal state
    clip_ids = Field(type=list, default=None, required=False, nullable=False)

    def on_init(self):
        if self.clip_ids is None:
            self.clip_ids = []
        super().on_init()

    def clips(self, song):
        results = [ song.find_clip(x) for x in self.clip_ids ]
        results = [ r for r in results if r is not None ]
        return results

    def add_clip(self, clip):
        assert clip is not None
        if clip.obj_id not in self.clip_ids:
            assert clip.obj_id is not None
            self.clip_ids.append(clip.obj_id)

    def has_clip(self, clip):
        assert clip is not None
        return clip.obj_id in self.clip_ids

    def remove_clip(self, clip):
        assert clip is not None
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
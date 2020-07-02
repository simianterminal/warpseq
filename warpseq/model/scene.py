from . base import BaseObject
from classforge import Class, Field

class Scene(BaseObject):

    from . scale import Scale

    name = Field(type=str, required=True, nullable=False)
    tempo = Field(type=int, default=None, nullable=True)
    scale = Field(type=Scale, default=None, nullable=True)

    auto_advance = Field(type=bool, default=None, nullable=True)
    measure_length = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=None, nullable=True)

    clip_ids = Field(type=list, required=True, nullable=False)

    def clips(self, song):
        results = [ song.find_clip(x) for x in self.clip_ids ]
        results = [ r for r in results if r is not None ]
        return results

    def add_clip(self, clip):
        assert clip is not None
        if clip.obj_id not in self.clip_ids:
            assert clip.obj_id is not None
            self.clip_ids.append(clip.obj_id)

    def remove_clip(self, clip):
        assert clip is not None
        self.clip_ids = [ c for c in self.clip_ids if c != clip.obj_id ]

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            tempo = self.tempo,
            auto_advance = self.auto_advance,
            measure_length = self.measure_length,
            repeat = self.repeat,
            clip_ids = self.clip_ids,
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
            tempo = data['tempo'],
            scale = song.find_scale(data['scale']),
            auto_advance = data['auto_advance'],
            measure_length = data['measure_length'],
            repeat = data['repeat'],
            clip_ids = data['clip_ids']
        )
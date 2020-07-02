from .base import BaseObject
from .pattern import Pattern
from classforge import Class, Field
from .arp import Arp
from .scale import Scale

class Clip(BaseObject):

    name = Field(type=str, required=True, nullable=False)
    scale = Field(type=Scale, required=False, nullable=True, default=None)
    pattern = Field(type=Pattern, required=False, default=None, nullable=True)
    length = Field(type=int, default=None, required=False, nullable=True)
    arp = Field(type=Arp, default=None, nullable=True)
    tempo = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=-1, nullable=True)

    track_ids = Field(type=list, default=[], required=True, nullable=False)
    scene_ids = Field(type=list, default=[], required=True, nullable=False)

    def scenes(self, song):
        return [ song.find_scene(x) for x in self.scene_ids ]

    def tracks(self, song):
        return [ song.find_track(x) for x in self.track_ids ]

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            length = self.length,
            tempo = self.tempo,
            repeat = self.repeat,
            track_ids = self.track_ids,
            scene_ids = self.scene_ids
        )
        if self.pattern:
            result['pattern'] = self.pattern.obj_id
        else:
            result['pattern'] = None
        if self.arp:
            result['arp'] = self.arp.obj_id
        else:
            result['arp'] = None
        if self.scale:
            result['scale'] = self.scale.obj_id
        else:
            result['scale'] = None
        return result

    def copy(self):

        new_id = self.new_object_id()

        return Clip(
            obj_id = new_id,
            name = self.name,
            pattern = self.pattern,
            length = self.length,
            arp = self.arp,
            tempo = self.tempo,
            repeat = self.repeat,
            track_ids = [],
            scene_ids = [],
        )

    @classmethod
    def from_dict(cls, song, data):
        return Clip(
            obj_id = data['obj_id'],
            name = data['name'],
            scale = song.find_scale(data['scale']),
            pattern = song.find_pattern(data['pattern']),
            length = data['length'],
            arp = song.find_arp(data['arp']),
            tempo = data['tempo'],
            repeat = data['repeat'],
            track_ids = data['track_ids'],
            scene_ids = data['scene_ids']
        )

    def add_scene(self, scene):
        if scene.obj_id not in self.scene_ids:
            self.scene_ids.append(scene.obj_id)

    def remove_scene(self, scene):
        self.scene_ids = [ s for s in self.scene_ids if s != scene.obj_id ]

    def add_track(self, track):
        if track.obj_id not in self.track_ids:
            self.track_ids.append(track.obj_id)

    def remove_track(self, track):
        self.track_ids = [ t for t in self.track_ids if t != track.obj_id ]

    #def get_effective_scale(self, scene=None, song=None):
    #    assert song is not None
    #    assert scale is not None
    #    # ask the clip, then pattern, then scene, then the song...
    #    raise NotImplementedError()

    #def get_effective_arpegiattor(self):
    #    assert song is not None
    #    assert scale is not None
    #    # ask the clip, then pattern, then scene, then the song...
    #    raise NotImplementedError()

    #def get_effective_tempo(self, scene=None, song=None):
    #    assert song is not None
    #    assert scale is not None
    #    # ask the clip, then pattern, then the scene, then the song...
    #    raise NotImplementedError()

    #def get_events(self, scene=None, song=None):



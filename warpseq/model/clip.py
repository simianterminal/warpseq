from .base import BaseObject
from .pattern import Pattern
from classforge import Class, Field
from .arp import Arp
from .scale import Scale

class Clip(BaseObject):

    from . track import Track
    from . scene import Scene

    name = Field(type=str, required=True, nullable=False)
    scale = Field(type=Scale, required=False, nullable=True, default=None)
    pattern = Field(type=Pattern, required=False, default=None, nullable=True)
    length = Field(type=int, default=None, required=False, nullable=True)
    arp = Field(type=Arp, default=None, nullable=True)
    tempo = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=-1, nullable=True)

    track = Field(type=Track, default=None, required=False, nullable=True)
    scene = Field(type=Scene, default=None, required=False, nullable=True)

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
        if self.track:
            result['track'] = self.track.obj_id
        else:
            result['track'] = None
        if self.scene:
            result['scene'] = self.scene.obj_id
        else:
            result['scene'] = None
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
            track = song.find_track(data['track']),
            scene = song.find_scene(data['scene'])
        )

    def actual_scale(self, song):
        assert song is not None

        assert self.scene is not None

        if self.scale:
            return self.scale
        if self.scene.scale:
            return self.scene.scale
        if song.scale:
            return song.scale
        return Exception("?")

    def actual_arp(self, song):

        assert self.track is not None

        if self.arp is not None:
            return self.arp
        if self.track.arp is not None:
            return self.arp
        raise Exception("?")

    def actual_tempo(self, song):

        if self.tempo is not None:
            return self.tempo
        if self.scene.tempo is not None:
            return self.scene.tempo
        if self.song.tempo is not None:
            return self.song.tempo

        raise Exception("?")


    def get_notes(self, song):

        scale = self.actual_scale(song)
        arp = self.actual_arp(song)


        # FIXME: move our scale logic from '_OLD_theory' into the new scale class!
        # FIXME: port the 'note' class...
        # FIXME: apply it here...



    #    assert song is not None
    #    assert scale is not None
    #    # ask the clip, then pattern, then scene, then the song...
    #    raise NotImplementedError()

    #def get_effective_tempo(self, scene=None, song=None):
    #    assert song is not None
    #    assert scale is not None
    #    # ask the clip, then pattern, then the scene, then the song...
    #    raise NotImplementedError()

    def get_events(self, song):

        notes = self.get_notes(song)

        # FIXME ... convert to events...





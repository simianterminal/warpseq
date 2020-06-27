from . base import BaseObject
from classforge import Class, Field
from .scale import Scale
import json

class Song(BaseObject):

    name = Field(type=str, required=True, nullable=False)
    scale = Field(type=Scale, required=False, nullable=True)
    tempo = Field(type=int, default=120, required=False, nullable=False)

    # these should likely be dicts, but names can change, so if we change them they should have remove methods.
    devices = Field(type=dict, required=False, default={}, nullable=False)
    instruments = Field(type=dict, required=False, default={}, nullable=False)
    scales = Field(type=dict, required=False, default={}, nullable=False)
    scenes = Field(type=dict, required=False, default={}, nullable=False)
    tracks = Field(type=dict, required=False, default={}, nullable=False)
    grid = Field(type=dict, required=False, default={}, nullable=False)
    clips = Field(type=dict, required=False, default={}, nullable=False)
    arps = Field(type=dict, required=False, default={}, nullable=False)
    patterns = Field(type=dict, required=False, default={}, nullable=False)

    auto_advance = Field(type=bool, default=False, nullable=True)
    measure_length = Field(type=int, default=15, nullable=True)
    repeat = Field(type=int, default=None, nullable=True)

    def find_device(self, name):
        return self.devices.get(name, None)

    def find_instrument(self, name):
        return self.instruments.get(name, None)

    def find_scale(self, name):
        return self.scales.get(name, None)

    def find_scene(self, name):
        return self.scenes.get(name, None)

    def find_track(self, name):
        return self.tracks.get(name, None)

    def find_clip(self, name):
        return self.clips.get(name, None)

    def find_arp(self, name):
        return self.arps.get(name, None)

    def find_pattern(self, name):
        return self.patterns.get(name, None)

    def to_dict(self):
        result = dict(
            name = self.name,
            tempo = self.tempo,
            auto_advance = self.auto_advance,
            measure_length = self.measure_length,
            repeat = self.repeat,
            devices = { k :  v.to_dict() for (k,v) in self.devices.items() },
            instruments = { k : v.to_dict() for (k, v) in self.instruments.items()},
            scales = { k :  v.to_dict() for (k, v) in self.scales.items()},
            scenes = { k : v.to_dict() for (k, v) in self.scenes.items()},
            tracks = {  k : v.to_dict() for (k, v) in self.tracks.items()},
            grid = self.grid,
            arps = { k : v.to_dict() for (k, v) in self.arps.items()},
            patterns = { k : v.to_dict() for (k, v) in self.patterns.items()},
            clips = { k : v.to_dict() for (k,v) in self.clips.items() }
        )
        if self.scale:
            result['scale'] = self.scale.name
        else:
            result['scale'] = None
        return result

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    @classmethod
    def from_dict(cls, data):

        song = Song(name=data['name'])

        from . device import Device
        from . instrument import Instrument
        from . scale import Scale
        from . scene import Scene
        from . track import Track
        from . clip import Clip
        from . arp import Arp
        from . pattern import Pattern

        song.scales = { k : Scale.from_dict(song, v) for (k,v) in data['scales'].items() }
        song.devices = { k : Device.from_dict(song, v) for (k,v) in data['devices'].items() }
        song.instruments =  { k : Instrument.from_dict(song, v) for (k,v) in data['instruments'].items() }

        song.scenes = { k : Scene.from_dict(song, v) for (k,v) in data['scenes'].items() }
        song.tracks = { k : Track.from_dict(song, v) for (k,v) in data['tracks'].items() }
        song.arps =  { k : Arp.from_dict(song, v) for (k,v) in data['arps'].items() }
        song.patterns =  { k : Pattern.from_dict(song, v) for (k,v) in data['patterns'].items() }
        song.clips =  { k : Clip.from_dict(song, v) for (k,v) in data['clips'].items() }

        song.scale = song.find_scale(data['scale'])
        song.tempo = data['tempo']
        song.auto_advance = data['auto_advance']
        song.measure_length = data['measure_length']
        song.repeat = data['repeat']

        song.grid =  { k : v for (k,v) in data['grid'].items() }

        return song

    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        return Song.from_dict(data)

    def _get_clip_index(self, scene=None, track=None):
        assert scene is not None
        assert track is not None
        index = "%s/%s" % (scene.name, track.name)
        return index

    def assign_clip(self, scene=None, track=None, clip=None):
        index = self._get_clip_index(scene=scene, track=track)
        self.grid[index] = clip.name

    def unassign_clip(self, scene=None, track=None):
        index = self._get_clip_index(scene=scene, track=track)
        if index in self.grid:
            del self.grid[index]

    def get_clip(self, scene=None, track=None):
        index = self._get_clip_index(scene=scene, track=track)
        if index in self.grid:
            clip_name = self.grid[index]
            return self.clips[clip_name]
        return None

    def add_clips(self, clips):
        for x in clips:
             self.clips[x.name] = x

    def remove_clip(self, clip):
        self.clips[clip.name]

    def rename_clip(self, clip, new_name):
        raise NotImplementedError()

    def add_devices(self, devices):
        for x in devices:
            self.devices[x.name] = x

    def remove_device(self, device):
        del self.devices[device.name]

    def rename_device(self, device, new_name):
        raise NotImplementedError()

    def add_instruments(self, instruments):
        for x in instruments:
            self.instruments[x.name] = x

    def remove_instrument(self, instrument):
        del self.instruments[instrument.name]

    def rename_instrument(self, instrument, new_name):
        raise NotImplementedError()

    def add_scales(self, scales):
        for x in scales:
            self.scales[x.name] = x

    def remove_scale(self, scale):
        del self.scales[scale.name]

    def rename_scale(self, scale, new_name):
        raise NotImplementedError()

    def add_tracks(self, tracks):
        for x in tracks:
            self.tracks[x.name] = x

    def remove_track(self, track):
        del self.tracks[track.name]

    def rename_track(self, track, new_name):
        raise NotImplementedError()

    def add_scenes(self, scenes):
        for x in scenes:
            self.scenes[x.name] = x

    def remove_scene(self, scene):
        del self.scenes[scene.name]

    def rename_scene(self, scene, new_name):
        raise NotImplementedError()

    def add_patterns(self, patterns):
        for x in patterns:
            self.patterns[x.name] = x

    def remove_pattern(self, pattern):
        del self.patterns[pattern.name]

    def rename_pattern(self, pattern, new_name):
        raise NotImplementedError()

    def add_arps(self, arps):
        for x in arps:
            self.arps[x.name] = x

    def remove_arp(self, arp):
        del self.arps[arp.name]

    def rename_arp(self, arp, new_name):
        raise NotImplementedError()

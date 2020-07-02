from . base import BaseObject
from classforge import Class, Field
from .scale import Scale
import json

FORMAT_VERSION = 0.1

class Song(BaseObject):

    name = Field(type=str, required=True, nullable=False)
    scale = Field(type=Scale, required=False, nullable=True)
    tempo = Field(type=int, default=120, required=False, nullable=False)

    # these should likely be dicts, but names can change, so if we change them they should have remove methods.
    devices = Field(type=dict, required=False, nullable=False)
    instruments = Field(type=dict, required=False, nullable=False)
    scales = Field(type=dict, required=False, nullable=False)

    scenes = Field(type=list, required=False, nullable=False)
    tracks = Field(type=list, required=False, nullable=False)

    clips = Field(type=dict, required=False, nullable=False)
    arps = Field(type=dict, required=False, nullable=False)
    patterns = Field(type=dict, required=False, nullable=False)

    auto_advance = Field(type=bool, default=False, nullable=True)
    measure_length = Field(type=int, default=15, nullable=True)
    repeat = Field(type=int, default=None, nullable=True)

    def find_device(self, obj_id):
        return self.devices.get(obj_id, None)

    def find_instrument(self, obj_id):
        return self.instruments.get(str(obj_id), None)

    def find_scale(self, obj_id):
        return self.scales.get(str(obj_id), None)

    def find_scene(self, obj_id):
        assert obj_id is not None
        assert type(obj_id) in [str,int]
        matching = [ x for x in self.scenes if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None
        assert len(matching) == 1
        return matching[0]

    def find_track(self, obj_id):
        assert obj_id is not None
        assert type(obj_id) in [str,int]
        matching = [ x for x in self.tracks if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None
        assert len(matching) == 1
        return matching[0]

    def find_clip(self, obj_id):
        return self.clips.get(str(obj_id), None)

    def find_arp(self, obj_id):
        return self.arps.get(str(obj_id), None)

    def find_pattern(self, obj_id):
        return self.patterns.get(str(obj_id), None)

    def to_dict(self):

        from . base import COUNTER

        result = dict(
            obj_id = self.obj_id,
            FORMAT_VERSION = FORMAT_VERSION,
            OBJ_COUNTER = COUNTER,
            name = self.name,
            tempo = self.tempo,
            auto_advance = self.auto_advance,
            measure_length = self.measure_length,
            repeat = self.repeat,
            devices = { str(k) :  v.to_dict() for (k,v) in self.devices.items() },
            instruments = { str(k) : v.to_dict() for (k, v) in self.instruments.items()},
            scales = { str(k) :  v.to_dict() for (k, v) in self.scales.items()},
            scenes = [ v.to_dict() for v in self.scenes ],
            tracks = [ v.to_dict() for v in self.tracks ],
            arps = { str(k) : v.to_dict() for (k, v) in self.arps.items()},
            patterns = { str(k) : v.to_dict() for (k, v) in self.patterns.items()},
            clips = { str(k) : v.to_dict() for (k,v) in self.clips.items() }
        )
        if self.scale:
            result['scale'] = self.scale.obj_id
        else:
            result['scale'] = None
        return result

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    @classmethod
    def from_dict(cls, data):

        song = Song(name=data['name'])

        from . base import COUNTER

        format_version = data.get('FORMAT_VERSION', 0)
        if format_version > FORMAT_VERSION:
            print("can not open data from a newer version of this program")

        COUNTER = data['OBJ_COUNTER']

        song.obj_id = data['obj_id']

        from . device import Device
        from . instrument import Instrument
        from . scale import Scale
        from . scene import Scene
        from . track import Track
        from . clip import Clip
        from . arp import Arp
        from . pattern import Pattern

        song.scales = { str(k) : Scale.from_dict(song, v) for (k,v) in data['scales'].items() }
        song.devices = { str(k) : Device.from_dict(song, v) for (k,v) in data['devices'].items() }
        song.instruments =  { str(k) : Instrument.from_dict(song, v) for (k,v) in data['instruments'].items() }

        song.scenes = [ Scene.from_dict(song, v) for v in data['scenes'] ]
        song.tracks = [ Track.from_dict(song, v) for v in data['tracks'] ]

        song.arps =  { str(k) : Arp.from_dict(song, v) for (k,v) in data['arps'].items() }
        song.patterns =  { str(k) : Pattern.from_dict(song, v) for (k,v) in data['patterns'].items() }
        song.clips =  { str(k) : Clip.from_dict(song, v) for (k,v) in data['clips'].items() }

        song.scale = song.find_scale(data['scale'])
        song.tempo = data['tempo']
        song.auto_advance = data['auto_advance']
        song.measure_length = data['measure_length']
        song.repeat = data['repeat']

        return song

    @classmethod
    def from_json(cls, data):
        data = json.loads(data)
        return Song.from_dict(data)

    # the grid should probably be a class?

    def _get_clip_index(self, scene=None, track=None):
        assert scene is not None
        assert track is not None
        index = "%s/%s" % (scene.obj_id, track.obj_id)
        return index

    def assign_clip(self, scene=None, track=None, clip=None):
        previous = self.get_clip_for_scene_and_track(scene=scene, track=track)
        if previous:
            self.unassign_clip(scene=scene, track=track, clip=clip)
        clip.add_track(track)
        clip.add_scene(scene)
        track.add_clip(clip)
        scene.add_clip(clip)
        return clip

    def unassign_clip(self, scene=None, track=None, clip=None):
        assert scene is not None
        assert track is not None
        assert clip is not None
        track.remove_clip(clip)
        scene.remove_clip(clip)
        clip.remove_track(track)
        clip.remove_scene(scene)
        return clip

    def get_clip_for_scene_and_track(self, scene=None, track=None):
        assert scene is not None
        assert track is not None
        results = []
        clips = scene.clips(self)
        for clip in clips:
            if track.has_clip(clip):
                results.append(clip)
        return self.one(results)

    def add_clips(self, clips):
        for x in clips:
            self.clips[str(x.obj_id)] = x

    # FIXME: methods like has_clip/ has_track, not this low level

    def remove_clip(self, clip):
        scenes = clip.scenes(self)
        tracks = clip.tracks(self)
        for s in scenes:
            scenes.remove_clip(c)
        for t in tracks:
            t.remove_clip(t)



    def add_devices(self, devices):
        for x in devices:
            self.devices[str(x.obj_id)] = x

    def remove_device(self, device):
        del self.devices[str(device.obj_id)]

    def add_instruments(self, instruments):
        for x in instruments:
            self.instruments[str(x.obj_id)] = x

    def remove_instrument(self, instrument):
        del self.instruments[str(instrument.obj_id)]

    def add_scales(self, scales):
        for x in scales:
            self.scales[str(x.obj_id)] = x

    def remove_scale(self, scale):
        del self.scales[str(scale.obj_id)]

    def add_tracks(self, tracks):
        self.tracks.extend(tracks)

    def remove_track(self, track):
        self.tracks = [ t for t in self.tracks if t.obj_id != track.obj_id ]

    def add_scenes(self, scenes):
        self.scenes.extend(scenes)

    def remove_scene(self, scene):
        self.scenes = [ s for s in self.scenes if s.obj_id != scene.obj_id ]

    def add_patterns(self, patterns):
        for x in patterns:
            self.patterns[str(x.obj_id)] = x

    def remove_pattern(self, pattern):
        del self.patterns[str(pattern.obj_id)]

    def add_arps(self, arps):
        assert type(arps) == list
        for x in arps:
            self.arps[str(x.obj_id)] = x

    def remove_arp(self, arp):
        del self.arps[str(arp.obj_id)]

# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the song is the fundamental unit of saving/loading in Warp and contains
# all object types.

import json

from classforge import Class, Field

from ..api import exceptions
from .base import NewReferenceObject
from .scale import Scale

FORMAT_VERSION = 0.1

class Song(NewReferenceObject):

    __slots__ = [ 'name', 'clips', 'scale', 'tempo', 'devices', 'instruments', 'scales', 'scenes', 'tracks', 'transforms', 'patterns', 'obj_id' ]

    #name = Field(type=str, required=True, nullable=False)
    #scale = Field(type=Scale, required=False, nullable=True)
    #tempo = Field(type=int, default=120, required=False, nullable=False)

    # mostly internal state, use add_remove to access
    #devices = Field(type=dict, required=False, nullable=False)
    #instruments = Field(type=dict, required=False, nullable=False)
    #scales = Field(type=dict, required=False, nullable=False)
    #scenes = Field(type=list, required=False, nullable=False)
    #tracks = Field(type=list, required=False, nullable=False)
    #clips = Field(type=dict, required=False, nullable=False)
    #transforms = Field(type=dict, required=False, nullable=False)
    #patterns = Field(type=dict, required=False, nullable=False)

    def __init__(self, name=None, clips = None, scale=None, tempo=120, devices=None, instruments=None, scales=None, scenes=None, tracks=None, transforms=None, patterns=None, obj_id=None):

        self.name = name
        self.clips = clips
        self.scale = scale
        self.tempo = tempo
        self.devices = devices
        self.instruments = instruments
        self.scales = scales
        self.scenes = scenes
        self.tracks = tracks
        self.transforms = transforms
        self.patterns = patterns
        self.obj_id = obj_id

        super(Song, self).__init__()

        self.reset(clear=False)

    def reset(self, clear=True):
        if clear or self.devices is None:
            self.devices = dict()
        if clear or self.instruments is None:
            self.instruments = dict()
        if clear or self.scales is None:
            self.scales = dict()
        if clear or self.tracks is None:
            self.tracks = []
        if clear or self.scenes is None:
            self.scenes = []
        if clear or self.clips is None:
            self.clips = dict()
        if clear or self.transforms is None:
            self.transforms = dict()
        if clear or self.patterns is None:
            self.patterns = dict()

    def find_device(self, obj_id):
        """
        Returns the device with the given object ID.
        This method and others like this are used for save/load support.
        """
        return self.devices.get(obj_id, None)

    def find_instrument(self, obj_id):
        """
        Returns the instrument with the given object ID.
        """
        return self.instruments.get(str(obj_id), None)

    def find_scale(self, obj_id):
        """
        Returns the scale with the given object ID.
        """
        return self.scales.get(str(obj_id), None)

    def find_scene(self, obj_id):
        """
        Returns the scene with the given object ID.
        """
        matching = [ x for x in self.scenes if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None
        return matching[0]

    def find_track(self, obj_id):
        """
        Returns the track with the given object ID.
        """
        matching = [ x for x in self.tracks if str(x.obj_id) == str(obj_id) ]
        if len(matching) == 0:
            return None
        return matching[0]

    def find_clip(self, obj_id):
        """
        Returns the clip with the given object ID.
        """
        return self.clips.get(str(obj_id), None)

    def find_clip_by_name(self, name):
        """
        Returns the clip with the given name.
        """
        for (k,v) in self.clips.items():
            if v.name == name:
                return v
        return None

    def find_transform(self, obj_id):
        """
        Returns the transform with the given object ID.
        """
        x = self.transforms.get(str(obj_id), None)
        return x

    def find_pattern(self, obj_id):
        """
        Returns the pattern with the given object ID.
        """
        return self.patterns.get(str(obj_id), None)

    def to_dict(self):
        """
        Returns the data for the entire song file.
        This can be reversed with from_dict.
        """
        from . base import COUNTER
        result = dict(
            obj_id = self.obj_id,
            FORMAT_VERSION = FORMAT_VERSION,
            OBJ_COUNTER = COUNTER,
            name = self.name,
            tempo = self.tempo,
            devices = { str(k) :  v.to_dict() for (k,v) in self.devices.items() },
            instruments = { str(k) : v.to_dict() for (k, v) in self.instruments.items()},
            scales = { str(k) :  v.to_dict() for (k, v) in self.scales.items()},
            scenes = [ v.to_dict() for v in self.scenes ],
            tracks = [ v.to_dict() for v in self.tracks ],
            transforms = { str(k) : v.to_dict() for (k, v) in self.transforms.items()},
            patterns = { str(k) : v.to_dict() for (k, v) in self.patterns.items()},
            clips = { str(k) : v.to_dict() for (k,v) in self.clips.items() }
        )
        if self.scale:
            result['scale'] = self.scale.obj_id
        else:
            result['scale'] = None
        return result

    def to_json(self):
        """
        Returns a saveable JSON version of the song file.
        """
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    @classmethod
    def from_dict(cls, data):
        """
        Loads a song from a dictionary.
        This must support PAST but not FUTURE versions of the program.
        """

        song = Song(name=data['name'])

        from . base import COUNTER

        format_version = data.get('FORMAT_VERSION', 0)
        if format_version > FORMAT_VERSION:
            # FIXME:  change exception type
            print("can not open data from a newer version of this program")

        COUNTER = data['OBJ_COUNTER']

        song.obj_id = data['obj_id']

        from . device import Device
        from . instrument import Instrument
        from . scale import Scale
        from . scene import Scene
        from . track import Track
        from . clip import Clip
        from . transform import Transform
        from . pattern import Pattern

        song.scales = { str(k) : Scale.from_dict(song, v) for (k,v) in data['scales'].items() }
        song.devices = { str(k) : Device.from_dict(song, v) for (k,v) in data['devices'].items() }
        song.instruments =  { str(k) : Instrument.from_dict(song, v) for (k,v) in data['instruments'].items() }

        song.scenes = [ Scene.from_dict(song, v) for v in data['scenes'] ]
        song.tracks = [ Track.from_dict(song, v) for v in data['tracks'] ]

        song.transforms =  {str(k) : Transform.from_dict(song, v) for (k, v) in data['transforms'].items()}
        song.patterns =  { str(k) : Pattern.from_dict(song, v) for (k,v) in data['patterns'].items() }
        song.clips =  { str(k) : Clip.from_dict(song, v) for (k,v) in data['clips'].items() }

        song.scale = song.find_scale(data['scale'])
        song.tempo = data['tempo']

        return song

    def next_scene(self, scene):
        """
        Returns the scene that is positioned after this one in the song.
        This uses the scene array, implying (FIMXE) we need a method to reorder scenes.
        """
        index = None
        for (i,x) in enumerate(self.scenes):
            if x.obj_id == scene.obj_id:
                index = i
                break
        index = index + 1
        if index >= len(self.scenes):
            return None
        return self.scenes[index]

    @classmethod
    def from_json(cls, data):
        """
        Loads the song from JSON data, such as from a save file.
        """
        data = json.loads(data)
        return Song.from_dict(data)

    def _get_clip_index(self, scene=None, track=None):
        """
        Internal storage of clip uses a dict where the key is the combination of
        the scene and track object IDs.
        """
        index = "%s/%s" % (scene.obj_id, track.obj_id)
        return index

    def add_clip(self, scene=None, track=None, clip=None):
        """
        Adds a clip at the intersection of a scene and track.
        """

        # calling code must *COPY* the clip before assigning, because a clip must be added
        # to the clip list and *ALSO* knows its scene and track.

        previous = self.get_clip_for_scene_and_track(scene=scene, track=track)
        if previous and clip.obj_id == previous.obj_id:
            return

        if previous:
            self.remove_clip(scene=scene, track=track)

        self.clips[str(clip.obj_id)] = clip

        clip.track = track
        clip.scene = scene

        #assert clip.scene is not None

        track.add_clip(clip)
        scene.add_clip(clip)

        #assert clip.track is not None
        #assert clip.scene is not None

        return clip

    def remove_clip(self, scene=None, track=None):
        """
        Deletes a clip.  The name isn't used - specify the scene and track.
        """

        # removing a clip returns a clip object that can be used with *assign* to add the
        # clip back.

        #assert scene is not None
        #assert track is not None

        clip = self.get_clip_for_scene_and_track(scene=scene, track=track)
        if clip is None:
            return None

        track.remove_clip(clip)
        scene.remove_clip(clip)

        clip.track = None
        clip.scene = None

        del self.clips[clip.obj_id]

        return clip

    def get_clips_for_scene(self, scene=None):
        """
        Returns all clips in a given scene.
        """
        return scene.clips()

    def get_clip_for_scene_and_track(self, scene=None, track=None):
        """
        Returns the clip at the intersection of the scene and track.
        """
        #assert scene is not None
        #assert track is not None
        results = []
        clips = scene.clips(self)
        for clip in clips:
            if track.has_clip(clip):
                results.append(clip)
        return self.one(results)

    def add_devices(self, devices):
        """
        Adds some device objects to the song.
        """
        for x in devices:
            self.devices[str(x.obj_id)] = x

    def remove_device(self, device):
        """
        Removes a device from the song.
        """
        del self.devices[str(device.obj_id)]

    def add_instruments(self, instruments):
        """
        Adds some instrument objects to the song
        """
        for x in instruments:
            self.instruments[str(x.obj_id)] = x

    def remove_instrument(self, instrument):
        """
        Removes an instrument object from the song.
        """
        del self.instruments[str(instrument.obj_id)]

    def add_scales(self, scales):
        """
        Adds some scale objects to a song.
        """
        for x in scales:
            self.scales[str(x.obj_id)] = x

    def remove_scale(self, scale):
        """
        Removes a scale object from the song.
        """
        del self.scales[str(scale.obj_id)]

    def add_tracks(self, tracks):
        """
        Adds some track objects to the song.
        """
        self.tracks.extend(tracks)

    def remove_track(self, track):
        """
        Remove a track object from the song.
        """
        self.tracks = [ t for t in self.tracks if t.obj_id != track.obj_id ]

    def add_scenes(self, scenes):
        """
        Adds some scene objects to the song.
        """
        self.scenes.extend(scenes)

    def remove_scene(self, scene):
        """
        Removes a scene object from the song.
        """
        self.scenes = [ s for s in self.scenes if s.obj_id != scene.obj_id ]

    def add_patterns(self, patterns):
        """
        Adds some pattern objects to the song.
        """
        for x in patterns:
            self.patterns[str(x.obj_id)] = x

    def remove_pattern(self, pattern):
        """
        Removes a pattern object from the song.
        """
        del self.patterns[str(pattern.obj_id)]

    def add_transforms(self, transforms):
        """
        Adds some transform objects to the song.
        """
        #assert type(transforms) == list
        for x in transforms:
            self.transforms[str(x.obj_id)] = x

    def remove_transform(self, transform):
        """
        Removes a transform object from the song.
        """
        del self.transforms[str(transform.obj_id)]

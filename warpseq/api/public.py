# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this implements the public Python API for WarpSeq.
# see examples/api/*.py for usage

import sys
import traceback

import rtmidi

from ..model.clip import Clip
from ..model.device import Device
from ..model.instrument import Instrument
from ..model.note import Note
from ..model.pattern import Pattern
from ..model.scale import Scale, scale_types
from ..model.scene import Scene
from ..model.song import Song
from ..model.track import Track
from ..model.transform import Transform
from ..playback.engine.realtime_engine import RealtimeEngine
from ..playback.multi_player import MultiPlayer
from .callbacks import Callbacks, DefaultCallback
from .exceptions import *
from .support import BaseApi

# =====================================================================================================================

midi_out = rtmidi.MidiOut()
MIDI_PORTS = midi_out.get_ports()

# =====================================================================================================================

class CollectionApi(BaseApi):

    def remove(self, name):
        return self._generic_remove(name)

# =====================================================================================================================

class Devices(CollectionApi):

    object_class    = Device
    public_fields   = [ 'name' ]
    song_collection = 'devices'
    add_method      = 'add_devices'
    add_required    = [ ]
    edit_required   = None
    remove_method   = 'remove_device'
    nullable_edits  = [ ]

    def __init__(self, public_api, song):
        super().__init__(public_api, song)
        self.auto_add_discovered()

    def list_available(self):
        """
        Return the names of all available MIDI devices the program can use.
        """
        return MIDI_PORTS

    def add(self, name):
        if name not in self.list_available():
            raise MIDIConfigError("MIDI device named (%s) is not available on this computer" % name)
        return self._generic_add(name, locals())

    def auto_add_discovered(self):
        for x in self.list_available():
            if not self.lookup(x):
                self.add(x)

# =====================================================================================================================

class Instruments(CollectionApi):

    object_class    = Instrument
    public_fields   = [ 'name', 'channel', 'device', 'muted']
    song_collection = 'instruments'
    add_method      = 'add_instruments'
    add_required    = [ 'channel', 'device']
    edit_required   = [ ]
    remove_method   = 'remove_instrument'
    nullable_edits  = [ ]

    def add(self, name, channel:int=None, device:str=None, min_octave:int=0, max_octave:int=10, base_octave:int=3, muted:bool=False):
        device = self.api.devices.lookup(device, require=True)
        return self._generic_add(name, locals())

    def edit(self, name, new_name:str=None, channel:int=None, device:str=None, min_octave:int=None, max_octave:int=None, base_octave:int=None, muted:bool=None):
        device = self.api.devices.lookup(device, require=True)
        return self._generic_edit(name, locals())

# =====================================================================================================================

class Tracks(CollectionApi):

    object_class    = Track
    public_fields   = [ 'name', 'instrument', 'track' ]
    song_collection = 'tracks'
    add_method      = 'add_tracks'
    add_required    = [ 'instrument', 'muted']
    edit_required   = [ ]
    remove_method   = 'remove_track'
    nullable_edits  = [ ]

    def add(self, name, instrument:str=None, muted:bool=False):
        instrument = self.api.instruments.lookup(instrument, require=True)
        return self._generic_add(name, locals())

    def edit(self, name, new_name:str=None, instrument:str=None, muted:bool=False):
        instrument = self.api.instruments.lookup(instrument, require=False)
        return self._generic_edit(name, locals())

# =====================================================================================================================

class Scales(CollectionApi):

    object_class    = Scale
    public_fields   = [ 'name', 'scale_type', 'slots' ] # this is somewhat ignored because of the methods below
    song_collection = 'scales'
    add_method      = 'add_scales'
    add_required    = [ ]
    edit_required   = [ ]
    remove_method   = 'remove_track'
    nullable_edits  = [ 'scale_type', 'slots', 'note', 'octave' ]

    def _check_params(self, params, for_edit=False):
        slots = params['slots']
        root = self._get_note(params)
        params['root'] = root
        scale_type = params['scale_type']
        if scale_type is None and slots is None:
            if not for_edit:
                raise InvalidInput("either scale_type or slots is required")
        if slots is not None and scale_type is not None:
            raise InvalidInput("scale_type and slots are mutually exclusive")
        del params['note']
        del params['octave']

    def _get_note(self, params):
        note = params['note']
        octave = params['octave']
        if note and (octave is not None):
            return Note(name=note, octave=octave)
        else:
            return None

    def _update_details(self, details, obj):
        if obj.root:
            details['note'] = obj.root.name
            details['octave'] = obj.root.octave
        else:
            details['note'] = None
            details['octave'] = None

    def add(self, name, note:str=None, octave:int=None, scale_type:str=None, slots:list=None):
        params = locals()
        self._check_params(params)
        return self._generic_add(name, params)

    def edit(self, name, new_name:str=None, note:str=None, octave:int=None, scale_type:str=None, slots:list=None):
        params = locals()
        self._check_params(params, for_edit=True)
        return self._generic_edit(name, params)

    def scale_types(self):
        return scale_types()

# =====================================================================================================================

class Transforms(CollectionApi):

    object_class     = Transform
    public_fields    = [ 'name', 'slots', 'octave_slots', 'divide' ]
    song_collection  = 'transforms'
    add_method       = 'add_transforms'
    add_required     = [ 'slots' ]
    edit_required    = [ ]
    remove_method    = 'remove_transform'
    nullable_edits   = [ ]

    def add(self, name, slots:list=None, octave_slots:list=None, divide:int=1):
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name, new_name:str=None, slots:list=None, octave_slots:list=None, divide:int=1):
        params = locals()
        return self._generic_edit(name, params)


# =====================================================================================================================

class Patterns(CollectionApi):

    object_class    = Pattern
    public_fields   = [ 'name', 'slots', 'octave_shift', 'scale', 'rate' ]
    song_collection = 'patterns'
    add_method      = 'add_patterns'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_pattern'
    nullable_edits   = [ 'tempo', 'scale ']

    def add(self, name, slots:list=None, rate=1):
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name, new_name:str=None, slots:list=None):
        params = locals()
        return self._generic_edit(name, params)

# =====================================================================================================================

class Scenes(CollectionApi):

    object_class    = Scene
    public_fields   = [ 'name', 'scale', 'auto_advance' ]
    song_collection = 'scenes'
    add_method      = 'add_scenes'
    add_required    = [ ]
    edit_required   = [ ]
    remove_method   = 'remove_scene'
    nullable_edits  = [ 'tempo', 'scale' ]

    def add(self, name, scale:str=None, auto_advance:bool=None, rate:int=1):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_add(name, params)

    def edit(self, name, new_name:str=None, scale:str=None, auto_advance:bool=None, rate:int=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        return self._generic_edit(name, params)

# =====================================================================================================================

class Clips(CollectionApi):

    object_class    = Clip
    public_fields   = [ 'name', 'scene', 'track', 'patterns',
                        'tempo_shifts', 'next_clip', 'transforms',
                        'repeat' ]
    song_collection = 'clips'
    add_method      = 'add_clip'
    add_required    = [ 'scene', 'track', 'patterns' ]
    edit_required   = [ 'scene', 'track' ]
    remove_method   = 'remove_clip'
    nullable_edits  = [ 'tempo', 'repeat' ]

    # this is relatively dark because the clips are anything but generic, living at the intersection of a 2D
    # grid and the names are not unique

    def _lookup_transforms(self, alist):
        results = []
        for x in alist:
            if type(x) == list:
                results.append([ self.api.transforms.lookup(i, require=True) for i in x])
            else:
                results.append(self.api.transforms.lookup(x))
        return results

    def add(self, name, scene:str=None, track:str=None, patterns:list=None,
            tempo_shifts:list=None, next_clip:str=None,
            transforms:list=None, repeat:int=None, auto_scene_advance:bool=False, scales:list=None, rate:int=1):

        if patterns:
            patterns = [ self.api.patterns.lookup(p, require=True) for p in patterns ]
        if transforms:
            transforms = self._lookup_transforms(transforms)
        if scales:
            scales = [ self.api.scales.lookup(s, require=True) for s in scales ]
        params = locals()

        clip = Clip(name=name, patterns=patterns, tempo_shifts=tempo_shifts, next_clip=next_clip,
                 transforms=transforms, auto_scene_advance=auto_scene_advance, repeat=repeat, scales=scales, rate=rate)

        scene = self.api.scenes.lookup(scene, require=True)
        track = self.api.tracks.lookup(track, require=True)

        self.song.add_clip(scene=scene, track=track, clip=clip)
        return self._ok()


    def edit(self, name:str=None, new_name:str=None, scene: str = None, track:str = None, patterns: list = None,
            tempo_shifts: list = None, next_clip:str = None,
            transforms:list = None, repeat:int=None, auto_scene_advance:bool=False, scales:list=None, rate:int=None):

        scene = self.api.scenes.lookup(scene, require=True)
        track = self.api.tracks.lookup(track, require=True)

        params = locals()

        if patterns:
            params["patterns"] = [ self.api.patterns.lookup(p, require=True) for p in patterns ]
        if transforms:
            params["transforms"] = self._lookup_transforms(transforms)
        if scales:
            params["scales"] = [ self.api.scales.lookup(s, require=True) for s in scales ]

        if new_name is not None:
            params["name"] = params["new_name"]
        else:
            del params["name"]
        del params["new_name"]

        if params["next_clip"]:
            # validate but keep it a string
            self.api.clips.lookup(params["next_clip"], require=True)


        obj = self.song.get_clip_for_scene_and_track(scene, track)
        if obj is None:
            raise InvalidInput("clip not found for scene (%s) and track (%s)" % (scene.name, track.name))

        for (k,v) in params.items():
            if k == 'self':
                continue
            if k in self.__class__.nullable_edits or v is not None:
                setattr(obj, k, v)

        return self._ok()

    def remove(self, scene:str=None, track:str=None):

        scene = self.api.scenes.lookup(scene, require=True)
        track = self.api.tracks.lookup(track, require=True)
        self.song.remove_clip(scene,track)
        return self._ok()

    def _short_details(self, obj):
        return dict(name=obj.name, scene=obj.scene.name, track=obj.track.name)


# =====================================================================================================================

class Player(object):

    def __init__(self, public_api, song):
        self.public_api = public_api
        self.song = song
        self.multi_player = MultiPlayer(song=song, engine_class=RealtimeEngine)

    def play_scene(self, scene):
        scene = self.public_api.scenes.lookup(scene, require=True)
        self.multi_player.play_scene(scene)

    def play_clips(self, clips):
        clips = [ c for c in self.public_api.clips.lookup(c, require=True) ]
        self.multi_player.add_clips(clips)

    def stop_clips(self, clips):
        clips = [ c for c in self.public_api.clips.lookup(c, require=True) ]
        for c in clips:
            self.multi_player.remove_clip(c)

    def stop(self):
        self.multi_player.stop()

    def advance(self, milliseconds=2):
        self.multi_player.advance(milliseconds)

    def loop(self, scene_name, abort=True, stop_if_empty=True):

        self.multi_player.stop_if_empty = stop_if_empty
        self.play_scene(scene_name)

        try:
            while True:
                self.advance(1)
        except KeyboardInterrupt:
            self.public_api._callbacks.keyboard_interrupt()
            self.stop()
            if abort:
                sys.exit(0)
        except AllClipsDone:
            self.public_api._callbacks.all_clips_done()
            if abort:
                sys.exit(0)
        except WarpException:
            traceback.print_exc()
            try:
                self.stop()
            except:
                pass
            if abort:
                sys.exit(0)

# =====================================================================================================================

class SongApi(object):

    def __init__(self, public_api, song):
        self.public_api = public_api
        self.song = song

    def edit(self, tempo:int=None, scale:str=None):
        if tempo:
            self.song.tempo = tempo
        if scale:
            scale = self.public_api.scales.lookup(scale, require=True)
            self.song.scale = scale



# =====================================================================================================================

class Api(object):

    def __init__(self, default_callbacks=True):
        self._reset()
        self._callbacks = Callbacks()

        if default_callbacks:
            self._callbacks.clear()
            self._callbacks.register(DefaultCallback())

    def _reset(self):
        self._filename = None
        self._song = Song(name='')
        self._setup_api()

    def _setup_api(self):
        self.song = SongApi(self, self._song)
        self.devices = Devices(self, self._song)
        self.instruments = Instruments(self, self._song)
        self.scales  = Scales(self, self._song)
        self.patterns = Patterns(self, self._song)
        self.transforms = Transforms(self, self._song)
        self.scenes = Scenes(self, self._song)
        self.tracks = Tracks(self, self._song)
        self.clips = Clips(self, self._song)
        self.player = Player(self, self._song)

    # ------------------------------------------------------------------------------------------------------------------
    # FIXME: implement all of these to enable the UI

    #def new(self):
    #    # TODO: no way to edit the 'name' of the song, which isn't the same as the filename, do we even need one?
    #    self._reset()

    def load(self, filename:str):
        fh = open(filename, "r")
        data = fh.read()
        fh.close()
        self._song = Song.from_json(data)
        self._filename = filename
        self._setup_api()

    def save(self):
        if not self._filename:
            raise InvalidUsage("no filename set, use save_as")
        data = self._song.to_json()
        fh = open(self._filename, "w+")
        fh.write(data)
        fh.close()

    def save_as(self, filename:str):
        self._filename = filename
        self.save()

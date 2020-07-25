import rtmidi

from .. model.song import Song
from .. model.device import Device
from .. model.instrument import Instrument
from .. model.pattern import Pattern
from .. model.transform  import Transform
from .. model.track import Track
from .. model.scene import Scene
from .. model.clip import Clip

from . exceptions import  *
from . support import BaseApi

# =====================================================================================================================

midi_out = rtmidi.MidiOut()
MIDI_PORTS = midi_out.get_ports()

# =====================================================================================================================

class CollectionApi(BaseApi):

    def all(self):
        return self._generic_all()

    def list_names(self):
        self._generic_list_names()

    def remove(self, name):
        self._generic_remove(name)

# =====================================================================================================================

class Devices(CollectionApi):

    object_class    = Device
    song_collection = 'devices'
    add_method      = 'add_devices'
    add_required    = [ ]
    edit_required   = None
    remove_method   = 'remove_device'
    storage_dict    = True

    def list_available(self):
        return MIDI_PORTS

    def add(self, name):
        if name not in self.list_available():
            raise InvalidInput("MIDI device named (%s) is not available on this computer" % name)
        self._generic_add(name, locals())

# =====================================================================================================================

class Instruments(CollectionApi):

    object_class    = Instrument
    song_collection = 'instruments'
    add_method      = 'add_instruments'
    add_required    = [ 'channel', 'device']
    edit_required   = [ ]
    remove_method   = 'remove_instrument'
    storage_dict    = True

    def add(self, name, channel:int=None, device:str=None, min_octave:int=0, max_octave:int=10, base_octave:int=3):
        device = Devices(self.song)._lookup(device)
        self._generic_add(name, locals())

    def edit(self, name, channel:int=None, device:str=None, min_octave:int=None, max_octave:int=None, base_octave:int=None):
        device = Devices(self.song)._lookup(device)
        self._generic_edit(name, locals())

# =====================================================================================================================

class Patterns(CollectionApi):

    object_class    = Pattern
    song_collection = 'patterns'
    add_method      = 'add_patterns'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_pattern'
    storage_dict    = True

# =====================================================================================================================

class Transforms(CollectionApi):

    object_class     = Transform
    song_collection  = 'transforms'
    add_method       = 'add_transforms'
    add_required     = [ 'slots' ]
    edit_required    = [ ]
    remove_method    = 'remove_transform'
    storage_dict     = True

# =====================================================================================================================

class Tracks(CollectionApi):

    object_class    = Track
    song_collection = 'tracks'
    add_method      = 'add_tracks'
    add_required    = [ 'instrument', 'channel']
    edit_required   = [ ]
    remove_method   = 'remove_track'
    storage_dict    = False

# =====================================================================================================================

class Scenes(CollectionApi):

    object_class    = Scene
    song_collection = 'scenes'
    add_method      = 'add_scenes'
    add_required    = [ ]
    edit_required   = [ ]
    remove_method   = 'remove_scene'
    storage_dict    = False

# =====================================================================================================================


class Clips(CollectionApi):

    object_class    = Clip
    song_collection = 'clips'
    add_method      = None
    add_required    = [ 'scene', 'track' ]
    edit_required   = [ 'scene', 'track' ]
    remove_method   = 'remove_clip'
    storage_dict    = False

# =====================================================================================================================

class Player(object):

    def __init__(self, song):
        self.song = song

# =====================================================================================================================

class Api(object):

    def __init__(self):

        self.new()
        self.devices = Devices(self)
        self.instruments = Instruments(self)
        self.patterns = Patterns(self)
        self.transforms = Transforms(self)
        self.scenes = Scenes(self)
        self.clips = Clips(self)
        self.player = Player(self)

    # ------------------------------------------------------------------------------------------------------------------

    def new(self, name:str='song'):
        self.song = Song(name=name)

    def load(self, filename:str):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def save_as(self, filename:str):
        raise NotImplementedError()

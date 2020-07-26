import rtmidi

from .. model.song import Song
from .. model.device import Device
from .. model.instrument import Instrument
from .. model.scale import Scale
from .. model.pattern import Pattern
from .. model.transform  import Transform
from .. model.track import Track
from .. model.scene import Scene
from .. model.clip import Clip
from .. model.note import Note

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
    public_fields   = [ 'name' ]
    song_collection = 'devices'
    add_method      = 'add_devices'
    add_required    = [ ]
    edit_required   = None
    remove_method   = 'remove_device'

    def __init__(self, public_api, song):
        super().__init__(public_api, song)
        self.auto_add_discovered()

    def list_available(self):
        return MIDI_PORTS

    def add(self, name):
        if name not in self.list_available():
            raise InvalidInput("MIDI device named (%s) is not available on this computer" % name)
        self._generic_add(name, locals())

    def auto_add_discovered(self):
        for x in self.list_available():
            if not self.lookup(x):
                self.add(x)


# =====================================================================================================================

class Instruments(CollectionApi):

    object_class    = Instrument
    public_fields   = [ 'name', 'channel', 'device' ]
    song_collection = 'instruments'
    add_method      = 'add_instruments'
    add_required    = [ 'channel', 'device']
    edit_required   = [ ]
    remove_method   = 'remove_instrument'

    def add(self, name, channel:int=None, device:str=None, min_octave:int=0, max_octave:int=10, base_octave:int=3):
        device = self.api.devices.lookup(device, require=True)
        self._generic_add(name, locals())

    def edit(self, name, new_name:str=None, channel:int=None, device:str=None, min_octave:int=None, max_octave:int=None, base_octave:int=None):
        device = self.api.devices.lookup(device, require=True)
        self._generic_edit(name, locals())

# =====================================================================================================================

class Tracks(CollectionApi):

    object_class    = Track
    public_fields   = [ 'name', 'instrument', 'track' ]
    song_collection = 'tracks'
    add_method      = 'add_tracks'
    add_required    = [ 'instrument', 'muted']
    edit_required   = [ ]
    remove_method   = 'remove_track'

    def add(self, name, instrument:str=None, muted:bool=False):
        instrument = self.api.instruments.lookup(instrument, require=True)
        self._generic_add(name, locals())

    def edit(self, name, new_name:str=None, instrument:str=None, muted:bool=False):
        instrument = self.api.instruments.lookup(instrument, require=False)
        self._generic_edit(name, locals())

# =====================================================================================================================

class Scales(CollectionApi):

    object_class    = Scale
    public_fields   = [ 'name', 'scale_type', 'slots' ] # FIXME: may need work
    song_collection = 'scales'
    add_method      = 'add_scales'
    add_required    = [ ]
    edit_required   = [ ]
    remove_method   = 'remove_track'

    def _check_params(self, params, for_edit=False):
        slots = params['slots']
        root = self._get_note(params)
        params['root'] = root
        if root is None and slots is None:
            if not for_edit:
                raise InvalidInput("either root+octave+scale_type or slots is required")
            else:
                del params['root']
                del params['slots']
        if root is not None and slots is not None:
            raise InputInput("root/octave/scale_type and slots are mutually exclusive")
        del params['note']
        del params['octave']

    def _get_note(self, params):
        note = params['note']
        octave = params['octave']
        scale_type = params['scale_type']
        if note and octave and scale_type:
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
        self._generic_add(name, params)

    def edit(self, name, new_name:str=None, note:str=None, octave:int=None, scale_type:str=None, slots:list=None):
        params = locals()
        self._check_params(params, for_edit=True)
        self._generic_edit(name, params)

# =====================================================================================================================

class Transforms(CollectionApi):

    object_class     = Transform
    public_fields    = [ 'name', 'slots', 'octave_slots', 'divide' ]
    song_collection  = 'transforms'
    add_method       = 'add_transforms'
    add_required     = [ 'slots' ]
    edit_required    = [ ]
    remove_method    = 'remove_transform'

    def add(self, name, slots:list=None, octave_slots:list=None, divide:int=1):
        params = locals()
        print("PARAMS=%s" % params)
        self._generic_add(name, params)

    def edit(self, name, slots:list=None, octave_slots:list=None, divide:int=1):
        params = locals()
        print("PARAMS2=%s" % params)
        self._generic_edit(name, params)


# =====================================================================================================================

class Patterns(CollectionApi):

    #name = Field(required=True, nullable=False)
    #slots = Field(type=list, required=True, nullable=False)
    #length = Field(type=int, default=None, nullable=True)
    #length = Field(type=int, default=None, nullable=True)
    #octave_shift = Field(type=int, default=0, nullable=False)
    #tempo = Field(type=int, default=None, nullable=True)
    #scale = Field(type=Scale, default=None, nullable=True)

    object_class    = Pattern
    public_fields   = [ 'name', 'slots', 'length', 'octave_shift', 'tempo', 'scale' ]
    song_collection = 'patterns'
    add_method      = 'add_patterns'
    add_required    = [ 'slots' ]
    edit_required   = [ ]
    remove_method   = 'remove_pattern'

    def add(self, name, slots:list=None, length:int=None, octave_shift:int=0, tempo:int=None, scale=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        self._generic_add(name, params)

    def edit(self, name, slots:list=None, length:int=None, octave_shift:int=0, tempo:int=None, scale=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        self._generic_edit(name, params)

# =====================================================================================================================

class Scenes(CollectionApi):

    object_class    = Scene
    public_fields   = [ 'name', 'tempo', 'scale', 'auto_advance' ]
    song_collection = 'scenes'
    add_method      = 'add_scenes'
    add_required    = [ ]
    edit_required   = [ ]
    remove_method   = 'remove_scene'


    def add(self, name, tempo:int=None, scale:str=None, auto_advance:bool=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        self._generic_add(name, params)

    def edit(self, name, tempo:int=None, scale:str=None, auto_advance:bool=None):
        if scale:
            scale = self.api.scales.lookup(scale, require=True)
        params = locals()
        self._generic_edit(name, params)


# =====================================================================================================================


class Clips(CollectionApi):

    object_class    = Clip
    public_fields   = [ 'FIXME' ]
    song_collection = 'clips'
    add_method      = None
    add_required    = [ 'scene', 'track' ]
    edit_required   = [ 'scene', 'track' ]
    remove_method   = 'remove_clip'

# =====================================================================================================================

class Player(object):

    def __init__(self, public_api, song):
        self.public_api = public_api
        self.song = song

# =====================================================================================================================

class Api(object):

    def __init__(self):
        self.song = Song(name='')
        self.devices = Devices(self, self.song)
        self.instruments = Instruments(self, self.song)
        self.scales  = Scales(self, self.song)
        self.patterns = Patterns(self, self.song)
        self.transforms = Transforms(self, self.song)
        self.scenes = Scenes(self, self.song)
        self.tracks = Tracks(self, self.song)
        self.clips = Clips(self, self.song)
        self.player = Player(self, self.song)

    # ------------------------------------------------------------------------------------------------------------------

    def new(self):
        # TODO: no way to edit the 'name' of the song, which isn't the same as the filename, do we even need one?
        self.song.reset()

    def load(self, filename:str):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def save_as(self, filename:str):
        raise NotImplementedError()

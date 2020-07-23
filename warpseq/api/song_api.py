import rtmidi
from .. model.song import Song

midi_out = rtmidi.MidiOut()
MIDI_PORTS = midi_out.get_ports()

class SongApi(object):

    def __init__(self):
        self.new()

    # ------------------------------------------------------------------------------------------------------------------

    def load(self, filename):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def new(self, name='song'):
        self.song = Song(name=name)

    def save_as(self, filename):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------

    # Device:
    # name = Field(type=str, required=True)

    def get_devices(self):
        return MIDI_PORTS

    def add_device(self, name):
        print(locals())

    def edit_device(self, name):
        # set only if parameters aren't None
        pass

    def remove_device(self, name):
        pass

    # ------------------------------------------------------------------------------------------------------------------

    # Instrument:
    # name = Field(type=str, required=True, nullable=False)
    # channel = Field(type=int, required=True)
    # device = Field(type=Device, required=False)
    # min_octave = Field(type=int, required=False, default=0, nullable=False)
    # base_octave = Field(type=int, required=True, default=3, nullable=False)
    # max_octave = Field(type=int, required=True, default=8, nullable=False)
    # default_velocity = Field(type=int, required=False, default=120, nullable=False)

    def get_instruments(self):
        pass

    def add_instrument(self, name, channel=None, device=None, min_octave=0, base_octave=3, max_octave=10, default_velocity=200):
        print(locals())
        pass

    def edit_instrument(self, name, channel=None, device=None, min_octave=None, base_octave=None, max_octave=None, default_velocity=None):
        # set only if not None
        pass

    def remove_instrument(self, name):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    # pattern

    def add_pattern(self, name=None):
        pass

    def edit_pattern(self, name=None):
        pass

    def remove_pattern(self, name=None):
        pass

    # arp
    # track

    # def add_track(self):
    #    pass

    # scene
    # clip
    # player

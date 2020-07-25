
from classforge import Field
from warpseq.model.base import BaseObject
from warpseq.model.event import NOTE_ON, NOTE_OFF
import rtmidi as rtmidi
from warpseq.model.registers import register_playing_note, unregister_playing_note
from  ... notation.mod import ModExpression


MIDI_NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_NOTE_ON = 0x90
# 1001cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_POLYPHONIC_PRESSURE = AFTERTOUCH = 0xA0
# 1010cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_CONTROLLER_CHANGE = 0xB0 # see Channel Mode Messages!!!
# 1011cccc 0ccccccc 0vvvvvvv (channel, controller, value)
MIDI_PROGRAM_CHANGE = 0xC0
# 1100cccc 0ppppppp (channel, program)
MIDI_CHANNEL_PRESSURE = 0xD0
# 1101cccc 0ppppppp (channel, pressure)
MIDI_PITCH_BEND = 0xE0
# 1110cccc 0vvvvvvv 0wwwwwww (channel, value-lo, value-hi)
MIDI_NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
MIDI_NOTE_ON = 0x90

class RealtimeEngine(BaseObject):

    from ... model.song import Song
    from ... model.track import Track
    from ... model.clip import Clip
    from ... model.scale import Scale

    # input
    song = Field(type=Song,  required=True, nullable=False)
    track = Field(type=Track, required=True, nullable=False)
    clip = Field(type=Clip, required=True, nullable=False)

    # calculated
    channel = Field(type=int)
    device = Field()
    midi_out = Field()
    instrument = Field()
    midi_port = Field()
    mod_expressions = Field()

    count_on = Field(default=0)
    count_off = Field(default=0)

    # informational/state
    time_index = Field(type=int)

    def on_init(self):

        self.instrument = self.track.instrument
        self.channel = self.instrument.channel
        self.device = self.instrument.device
        self.mod_expressions = ModExpression(defer=True)
        self.midi_out = rtmidi.MidiOut()

        ports = self.midi_out.get_ports()
        index = 0
        for p in ports:
            if p == self.device.name:
                self.midi_port = index
                break
            index = index + 1

        # FIXME: custom exception type here

        if self.midi_port is None:
            print("available devices:")
            for p in ports:
                print("%s" % p)
            raise Exception("device named (%s) not found" % self.device.name)


        self.midi_out.open_port(self.midi_port)

        self.time_index = 0
        pass

    def _note_data(self, event):
        velocity = event.note.velocity
        if velocity is None:
            velocity = self.track.instrument.default_velocity
        return (event.note.note_number(), velocity)

    def channel_message(self, command, *data, ch=None):
        """Send a MIDI channel mode message."""
        command = (command & 0xf0) | ((ch if ch else self.channel) - 1 & 0xf)
        msg = [command] + [value & 0x7f for value in data]
        self.midi_out.send_message(msg)

    def _control_change(self, cc, value):
        self.channel_message(MIDI_CONTROLLER_CHANGE, cc, value)

    def _send_message(self, msg):
        self.midi_out.send_message(msg)


    def play(self, event):

        if event.type == NOTE_ON and event.note.flags['deferred'] == True:
            exprs = event.note.flags['deferred_expressions']
            for expr in exprs:
                event.note = self.mod_expressions.do(event.note, event.note.from_scale, self.track, expr)

        if not event.note:
            return

        if event.type == NOTE_ON:
            (note_number, velocity) = self._note_data(event)
            self.count_on = self.count_on + 1
            register_playing_note(self.track, event.note)

            if not self.track.muted:

                for (channel, value) in event.note.flags['cc'].items():
                    channel = int(channel)
                    self._control_change(channel, value)

                result = [ MIDI_NOTE_ON | self.channel - 1, note_number, velocity]
                self._send_message(result)

        elif event.type == NOTE_OFF:
            (note_number, velocity) = self._note_data(event.on_event)
            self.count_off = self.count_off + 1

            unregister_playing_note(self.track, event.on_event.note)
            result = [ MIDI_NOTE_OFF | self.channel - 1, note_number, velocity]
            self._send_message(result)

    def note_time_index(self, time_index):
        self.time_index = time_index


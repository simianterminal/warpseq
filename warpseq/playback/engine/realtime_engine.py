OLD = """
# copyright 2016-2020, Michael DeHaan <michael@michaeldehaan.net>

import time
import os

# this has been successfully tested with an Apple IAC Driver
# open Apple Audio MIDI setup if you have a Mac.
# https://pypi.python.org/pypi/rtmidi-python
import rtmidi_python as rtmidi

import camp.playback.constants as C

def get_ports():
    midi_out = rtmidi.MidiOut(b'out')
    available_ports = midi_out.ports
    return available_ports

def get_bus():
    ports = get_ports()
    port_num = os.environ.get("CAMP_MIDI_BUS", len(ports) -1)
    return int(port_num)

class Midi(object):

    # currently this mostly just tests rtmidi.  This may change.

    def __init__(self):

        midi_out = rtmidi.MidiOut(b'out')
        midi_out.open_port(get_bus())
        self.midi_out = midi_out

    #def _volume(self, channel, volume):
    #    cc = CONTROL_CHANGE | channel
    #    return [cc, volume & 0x7F]

    def note_off(self, channel, note_number, velocity):
        result = [ C.NOTE_OFF | channel - 1, note_number, velocity ]
        return result

    def note_on(self, channel, note_number, velocity):
        result =  [ C.NOTE_ON | channel - 1, note_number, velocity ]
        return result

    def play_event(self, event):
        print(event)
        self.midi_out.send_message(event)

    def playback_test(self):

        note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
        note_off = [0x80, 60, 0]
        self.midi_out.send_message(note_on)
        time.sleep(0.5)
        self.midi_out.send_message(note_off)
        print("OK!")

"""


from classforge import Field

from warpseq.model.base import BaseObject
from warpseq.model.event import NOTE_ON, NOTE_OFF
# this has been successfully tested with an Apple IAC Driver
# open Apple Audio MIDI setup if you have a Mac.
# https://pypi.python.org/pypi/rtmidi-python
import rtmidi as rtmidi
from warpseq.model.registers import register_playing_note, unregister_playing_note
from  ... notation.mod import ModExpression

#TIME_INTERVAL = 10

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

# FIXME: implement MIDI CCs, pass through velocity info from note objects

class RealtimeEngine(BaseObject):

    from ... model.song import Song
    from ... model.track import Track
    from ... model.clip import Clip
    from ... model.scale import Scale

    # input
    song = Field(type=Song,  required=True, nullable=False)
    scale = Field(type=Scale, required=True, nullable=False)
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

        if self.midi_port is None:
            print("available devices:")
            for p in ports:
                print("%s" % p)
            raise Exception("device named (%s) not found" % self.device.name)


        self.midi_out.open_port(self.midi_port)

        self.time_index = 0
        pass

    def _note_data(self, event):

        #event.note = event.note.transpose(octaves=self.instrument.base_octave)
        # FIXME: do we need to test here that the note is within the range of min_octave and max_octave ?

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

        # octave shifts are from the instrument!
        # min_octave = 0, base_octave = 3, max_octave = 8

        #if event.type == NOTE_ON and event.note.flags['deferred'] == True:
        #    #print("*** PROCESSING DEFERRED FLAGS ***")
        #    exprs = event.note.flags['deferred_expressions']
        #    for expr in exprs:
        #        #print("PROCESSING DEFERRED EXPR: %s" % expr)
        #        event.note = self.mod_expressions.do(event.note, self.scale, self.track, expr)

        if event.type == NOTE_ON:
            (note_number, velocity) = self._note_data(event)

            #print("NN ON=%s" % note_number)
            self.count_on = self.count_on + 1
            #print("REGISTERING: %s")
            register_playing_note(self.track, event.note)
            if not self.track.muted:

                for (channel, value) in event.note.flags['cc'].items():
                    # usually there won't be any
                    channel = int(channel)
                    self._control_change(channel, value)

                result = [ MIDI_NOTE_ON | self.channel - 1, note_number, velocity]
                self._send_message(result)



        elif event.type == NOTE_OFF:
            (note_number, velocity) = self._note_data(event.on_event)
            #print("NN OFF=%s" % note_number)
            self.count_off = self.count_off + 1

            unregister_playing_note(self.track, event.on_event.note)
            result = [ MIDI_NOTE_OFF | self.channel - 1, note_number, velocity]
            self._send_message(result)

        #print("ON/OFF: %s/%s" % (self.count_on, self.count_off))


    def note_advance(self, milliseconds):
        pass

    def note_time_index(self, time_index):
        self.time_index = time_index


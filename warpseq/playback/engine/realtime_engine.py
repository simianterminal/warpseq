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

class RealtimeEngine(BaseObject):

    from ... model.song import Song
    from ... model.track import Track

    # input
    song = Field(type=Song,  required=True, nullable=False)
    track = Field(type=Track, required=True, nullable=False)

    # calculated
    channel = Field(type=int)
    device = Field()
    midi_out = Field()
    instrument = Field()
    midi_port = Field()

    # informational/state
    time_index = Field(type=int)

    def on_init(self):

        self.instrument = self.track.instrument
        self.channel = self.instrument.channel
        self.device = self.instrument.device

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

    def _note_number(self, event):
        return event.note.note_number()

    def _send_message(self, msg):
        self.midi_out.send_message(msg)


    def play(self, event):

        if event.type == NOTE_ON:
            velocity = 100
            note_number = self._note_number(event)
            result = [ MIDI_NOTE_ON | self.channel - 1, note_number, velocity]
            self._send_message(result)

        elif event.type == NOTE_OFF:
            velocity = 100
            note_number = self._note_number(event)
            result = [ MIDI_NOTE_OFF | self.channel - 1, note_number, velocity]
            self._send_message(result)


    def note_advance(self, milliseconds):
        pass

    def note_time_index(self, time_index):
        self.time_index = time_index


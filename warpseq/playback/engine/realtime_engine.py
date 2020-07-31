# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class is used by the player code to send MIDI events to hardware
# it contains some logic to convert chords to note events and must also
# process deferred mod-expressions caused by late-binding intra-track
# events.

from classforge import Field
from warpseq.model.base import BaseObject
from warpseq.model.event import NOTE_ON, NOTE_OFF
import rtmidi as rtmidi
from warpseq.model.registers import register_playing_note, unregister_playing_note
from  ... notation.mod import ModExpression
from warpseq.api.callbacks import Callbacks
from warpseq.api.exceptions import *

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
    callbacks = Field()

    def on_init(self):

        """
        Creates a handle to our MIDI library and verifies the device.
        """

        self.instrument = self.track.instrument
        self.channel = self.instrument.channel
        self.device = self.instrument.device
        self.mod_expressions = ModExpression(defer=True)
        self.midi_out = rtmidi.MidiOut()
        self.callbacks = Callbacks()

        ports = self.midi_out.get_ports()
        index = 0
        for p in ports:
            if p == self.device.name:
                self.midi_port = index
                break
            index = index + 1


        if self.midi_port is None:

            # FIXME: custom exception type here
            raise MIDIConfigError("MIDI device named (%s) not found, available choices: %s" % (self.device.name, ports))

        self.midi_out.open_port(self.midi_port)

    def _note_data(self, event):
        """
        return the note number and velocity for an event.
        use the default track velocity if not provided
        """
        # FIXME: velocity should be subject to min/max checking
        velocity = event.note.velocity
        if velocity is None:
            velocity = self.track.instrument.default_velocity
        return (event.note.note_number(), velocity)

    def channel_message(self, command, *data, ch=None):
        """
        send a MIDI channel mode message.
        """
        command = (command & 0xf0) | ((ch if ch else self.channel) - 1 & 0xf)
        msg = [command] + [value & 0x7f for value in data]
        self.midi_out.send_message(msg)

    def _control_change(self, cc, value):
        """
        send a MIDI control change
        FIXME: this should have min/max logic here
        """
        self.channel_message(MIDI_CONTROLLER_CHANGE, cc, value)

    def _send_message(self, msg):
        self.midi_out.send_message(msg)


    def play(self, event):

        # TODO: refactor into smaller functions

        from ... model.chord import Chord
        from ... model.event import Event, NOTE_OFF, NOTE_ON

        # deferred events happen when there are intra-track events such as replacing the note
        # with the currently playing note from a guide track (see docs). In this case we must
        # re-evaluate all mod expressions... we do not need to re-evaluate the track expressions
        # because the mod expression does throw away the note value and capture the value from
        # the guide track...

        if event.type == NOTE_ON and event.note.flags['deferred'] == True:
            exprs = event.note.flags['deferred_expressions']
            for expr in exprs:
                value = self.mod_expressions.do(event.note, event.scale, self.track, expr)
                if value is None:
                    return
                event.note = value

        # it is possible for mod expressions to take notes and return Chords. We have to do
        # cleanup here to turn this back into a list of notes.

        if type(event.note) == Chord:
            for x in event.note.notes:
                evt = event.copy()
                evt.note = x
                evt.note.flags['deferred'] = False
                self.play(evt)
            return

        if not event.note:
            # mod expressions might result in a silence event
            return

        if event.type == NOTE_ON:

            self.callbacks.on_note_on(event)
            (note_number, velocity) = self._note_data(event)
            self.count_on = self.count_on + 1
            register_playing_note(self.track, event.note)

            if not self.track.muted and not self.track.instrument.muted:

                for (channel, value) in event.note.flags['cc'].items():
                    channel = int(channel)
                    self._control_change(channel, value)

                result = [ MIDI_NOTE_ON | self.channel - 1, note_number, velocity]
                self._send_message(result)

        elif event.type == NOTE_OFF:

            # similar logic to the above: there is a chance we have an event tied to a chord, and we then need to silence
            # all notes in that chord separately.

            if type(event.on_event.note) == Chord:
                for x in event.on_event.note.notes:
                    evt = event.copy()
                    assert type(x) != Chord
                    evt.on_event = Event(time = event.on_event.time, scale=event.scale, note = x, type=event.on_event.type, on_event=None)
                    self.play(evt)
                return

            self.callbacks.on_note_off(event)

            (note_number, velocity) = self._note_data(event.on_event)
            self.count_off = self.count_off + 1

            unregister_playing_note(self.track, event.on_event.note)
            result = [ MIDI_NOTE_OFF | self.channel - 1, note_number, velocity]
            self._send_message(result)



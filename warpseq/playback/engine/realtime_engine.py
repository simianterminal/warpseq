# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class is used by the player code to send MIDI events to hardware
# it contains some logic to convert chords to note events and must also
# process deferred mod-expressions caused by late-binding intra-track
# events.

#import rtmidi as rtmidi

from ...api.callbacks import Callbacks
from ...api.exceptions import *
from ...model.registers import register_playing_note, unregister_playing_note
from ...notation.mod import ModExpression


import mido

#mido.set_backend('mido.backends.portmidi')


#MIDI_NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
#MIDI_NOTE_ON = 0x90
# 1001cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
#MIDI_POLYPHONIC_PRESSURE = AFTERTOUCH = 0xA0
# 1010cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
#MIDI_CONTROLLER_CHANGE = 0xB0 # see Channel Mode Messages!!!
# 1011cccc 0ccccccc 0vvvvvvv (channel, controller, value)
#MIDI_PROGRAM_CHANGE = 0xC0
# 1100cccc 0ppppppp (channel, program)
#MIDI_CHANNEL_PRESSURE = 0xD0
# 1101cccc 0ppppppp (channel, pressure)
#MIDI_PITCH_BEND = 0xE0
# 1110cccc 0vvvvvvv 0wwwwwww (channel, value-lo, value-hi)
#MIDI_NOTE_OFF = 0x80
# 1000cccc 0nnnnnnn 0vvvvvvv (channel, note, velocity)
#MIDI_NOTE_ON = 0x90


MIDO_CONTROLLER_CHANGE = 'control_change'
MIDO_NOTE_ON = 'note_on'
MIDO_NOTE_OFF = 'note_off'

from ...model.chord import Chord
from ...model.event import Event, NOTE_OFF, NOTE_ON

class RealtimeEngine(object):

    __slots__ = ['song','track','clip','channel','device','midi_out','instrument','midi_port','mod_expressions','callbacks','on_count','player','on_ct']

    def __init__(self, song=None, track=None, clip=None, player=None):

        self.song = song
        self.track = track
        self.clip = clip
        self.on_ct = 0

        self.instrument = self.track.instrument
        self.channel = self.instrument.channel
        self.device = self.instrument.device
        self.mod_expressions = ModExpression(defer=True, track=self.track)

        self.player = player
        self.callbacks = Callbacks()

        self.midi_out = self.device.get_midi_out()


    def play(self, event):



        # deferred events happen when there are intra-track events such as replacing the note
        # with the currently playing note from a guide track (see docs). In this case we must
        # re-evaluate all mod expressions... we do not need to re-evaluate the track expressions
        # because the mod expression does throw away the note value and capture the value from
        # the guide track...


        if event.type == NOTE_ON and event.note.flags['deferred'] == True:

            # we have to process deferred expressions twice because of the mod events
            # UNLESS we pair the off event.

            self.mod_expressions.scale = event.scale

            exprs = event.note.flags['deferred_expressions']
            for expr in exprs:

                assert event.note.from_scale is not None
                self.mod_expressions.scale = event.note.from_scale

                value = self.mod_expressions.do(event.note, expr)
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
            return

        if event.type == NOTE_ON:

            velocity = event.note.velocity
            if velocity is None:
                velocity = self.instrument.default_velocity
            note_number = event.note.note_number()

            register_playing_note(self.track, event.note)

            if self.track.muted or self.instrument.muted:
                return

            if event.note.octave > self.instrument.max_octave or note_number > 127:
                return

            if event.note.octave < self.instrument.min_octave or note_number < 0:
                return

            for (control, value) in event.note.flags['cc'].items():
                control = int(control)
                #command = (MIDI_CONTROLLER_CHANGE & 0xf0) | (self.channel - 1 & 0xf)
                #self.midi_out.send_message([command, channel & 0x7f, value & 0x7f])
                msg = mido.Message(MIDO_CONTROLLER_CHANGE, channel=self.channel-1, control=control, value=value)
                self.midi_out.send(msg)


            #print("ON (%s): %s" % (self.on_ct, event.note))
            self.on_ct = self.on_ct + 1
            self.player.inject_off_event(event)


            #self.midi_out.send_message([ MIDI_NOTE_ON | self.channel - 1, note_number, velocity])

            msg = mido.Message(MIDO_NOTE_ON, note=note_number, velocity=velocity, channel=self.channel-1)
            self.midi_out.send(msg)


        elif event.type == NOTE_OFF:

            # similar logic to the above: there is a chance we have an event tied to a chord, and we then need to silence
            # all notes in that chord separately.

            if type(event.on_event.note) == Chord:
                for x in event.on_event.note.notes:
                    evt = event.copy()
                    evt.on_event = Event(time = event.on_event.time, scale=event.scale, note = x, type=event.on_event.type, on_event=None)
                    self.play(evt)
                return

            velocity = event.note.velocity
            if velocity is None:
                velocity = self.instrument.default_velocity
            note_number = event.on_event.note.note_number()


            unregister_playing_note(self.track, event.on_event.note)

            if self.track.muted or self.instrument.muted:
                return

            #print("OFF (%s): %s" % (self.on_ct, event.on_event.note))
            self.on_ct = self.on_ct - 1
            #self.midi_out.send_message([ MIDI_NOTE_OFF | self.channel - 1, note_number, velocity])

            msg = mido.Message(MIDO_NOTE_OFF, note=note_number, velocity=velocity, channel=self.channel-1)
            self.midi_out.send(msg)

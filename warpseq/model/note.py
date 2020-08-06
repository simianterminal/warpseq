# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# modelling of notes, including step math necessary for creating
# chords and understanding scales.

import re

from ..api.exceptions import *
from ..utils.utils import roll_left, roll_right
from . note_table import NOTE_TABLE
from .base import BaseObject
import functools

DEFAULT_VELOCITY = 120

NOTES          = [ 'C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A', 'Bb', 'B' ]
EQUIVALENCE    = [ 'C',  'C#', 'D', 'D#', 'E',  'F',  'F#', 'G',  'G#', 'A', 'A#', 'B' ]
EQUIVALENCE_SET = set(EQUIVALENCE)
UP_HALF_STEP   = roll_left(NOTES)
DOWN_HALF_STEP = roll_right(NOTES)

SCALE_DEGREES_TO_STEPS = {
   '0'  : 0, # people may enter this meaning "do nothing", but really it is 1.
   '1'  : 0, # C (if C major)
   'b2' : 0.5,
   '2'  : 1, # D
   'b3' : 1.5,
   '3'  : 2, # E
   '4'  : 2.5, # F
   'b5' : 3,
   '5'  : 3.5, # G
   'b6' : 4,
   '6'  : 4.5, # A
   'b7' : 5,
   '7'  : 5.5, # B
   '8'  : 6
}

class Note(object):

    __slots__ = [ 'name', 'octave', 'tie', 'length', 'start_time', 'end_time', 'flags', 'velocity', 'from_scale' ]

    def __init__(self, name=None, octave=None, tie=False, length=None, start_time=None, end_time=None, flags=None, velocity=DEFAULT_VELOCITY, from_scale=None):

         self.octave = octave
         self.tie = tie
         self.length = length
         self.start_time = start_time
         self.end_time = end_time
         self.flags = flags
         self.velocity = velocity
         self.from_scale = from_scale

         if name in EQUIVALENCE_SET:
             name = NOTES[EQUIVALENCE.index(name)]
         self.name = name

         if self.flags is None:
             self.flags = {
                'deferred' : False,
                'deferred_expressions' : [],
                'cc' : {}
             }

    def copy(self):
        """
        Returns a new Note with the same data as the current Note
        """
        return Note(name=self.name,
                    octave=self.octave,
                    tie=self.tie,
                    length=self.length,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    velocity=self.velocity,
                    from_scale=self.from_scale,
                    flags={
                        'deferred' : self.flags['deferred'],
                        'deferred_expressions' : self.flags['deferred_expressions'].copy(),
                        'cc' : self.flags['cc'].copy()
                    }
        )

    def chordify(self, chord_type):
        """
        Returns a chord of a given type using this note as the root note.
        """
        from . chord import Chord
        return Chord(root=self, chord_type=chord_type, from_scale=self.from_scale)

    def _equivalence(self, name):
        """
        Normalize note names on input, C# -> Db, etc
        Internally everything uses flats.
        """
        if name in EQUIVALENCE:
            return NOTES[EQUIVALENCE.index(name)]
        return name


    def scale_transpose(self, scale_obj, steps):
        """
        Return the note N steps up (or down) within the current scale.
        """

        snn = self.note_number()
        scale_notes = scale_obj.get_notes()
        note_numbers = scale_obj.get_note_numbers()

        index = None
        for (i,x) in enumerate(note_numbers):
            if x >= snn:
                index = i
                break

        # index of None will crash the program but shouldn't happen

        scale_note = scale_notes[index + steps]

        return Note(name=scale_note.name, octave=scale_note.octave, length=self.length, start_time=self.start_time,
                    end_time=self.end_time, tie=self.tie, flags=self.flags, from_scale=scale_obj)


    def with_velocity(self, velocity):
        """
        Return a copy of this note with the set velocity
        """
        n1 = self.copy()
        n1.velocity = velocity
        return n1

    def with_octave(self, octave):
        """
        Return a copy of this note with the set octave.
        """
        n1 = self.copy()
        n1.octave = octave
        return n1

    def with_cc(self, channel, value):
        """
        Return a copy of the note with the set MIDI CC value.
        """
        n1 = self.copy()
        n1.flags["cc"][str(channel)] = value
        return n1

    def transpose(self, steps=0, semitones=0, degrees=0, octaves=0):
        """
        Returns a note a given number of steps or octaves or (other things) higher.
        steps -- half step as 0.5, whole step as 1, or any combination.  The most basic way to do things.
        semitones - 1 semitone is simply a half step.  Provided to keep some implementations more music-literate.
        octaves - 6 whole steps, or 12 half steps.  Easy enough.
        degrees - scale degrees, to keep scale definition somewhat music literate.  "3" is a third, "b3" is a flat third, "3#" is an augmented third, etc.
        You can combine all of them at the same time if you really want (why?), in which case they are additive.
        """

        degree_steps = SCALE_DEGREES_TO_STEPS[str(degrees)]
        steps = steps + (semitones * 0.5) + degree_steps

        result = self.copy()
        if steps:
            # this is in an in-place edit because the note was already copied
            (result.name, result.octave) = NOTE_TABLE[result.note_number() + int(2 * steps)]
        if octaves:
            result.octave = result.octave + octaves
        return result

    def note_number(self):
        """
        What order is this note on the keyboard?
        """
        return NOTES.index(self.name) + (12 * self.octave)

    def __repr__(self):
        return "Note<%s|%s,len=%s,time=%s/%s,cc=%s,tie=%s>" % (self.name, self.octave, self.length, self.start_time, self.end_time, self.flags['cc'], self.tie)



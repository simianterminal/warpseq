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
from . import note_table
from .base import BaseObject
import functools

DEFAULT_VELOCITY = 120
NOTE_SHORTCUT_REGEX = re.compile("([A-Za-z#]+)([0-9]*)")

NOTES          = [ 'C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A', 'Bb', 'B' ]
EQUIVALENCE    = [ 'C',  'C#', 'D', 'D#', 'E',  'F',  'F#', 'G',  'G#', 'A', 'A#', 'B' ]
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

    #name = Field(type=str)
    #octave = Field(type=int, default=4, nullable=True)
    #tie = Field(type=bool, default=False)
    ##length = Field(type=int, default=None)
    #start_time = Field(type=int, default=None)
    #end_time = Field(type=int, default=None)
    #flags = Field(type=dict, default=None, required=False)
    #velocity = Field(type=int, default=DEFAULT_VELOCITY, required=False)
    #from_scale = Field(default=None)

    def __init__(self, name=None, octave=None, tie=None, length=None, start_time=None, end_time=None, flags=None, velocity=None, from_scale=None):
         self.name = name
         self.octave = octave
         self.tie = tie
         self.length = length
         self.start_time = start_time
         self.end_time = end_time
         self.flags = flags
         self.velocity = velocity
         self.from_scale = from_scale

         self.name =  self._equivalence(self.name)
         if self.flags is None:
             self.flags = {}
             self.flags['deferred'] = False
             self.flags['deferred_expressions'] = []
             self.flags['cc'] = dict()
         # super().on_init()

    def copy(self):
        """
        Returns a new Note with the same data as the current Note
        """
        n1 = Note(name=self.name,
                    octave=self.octave,
                    tie=self.tie,
                    length=self.length,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    velocity=self.velocity,
                    flags={})
        n1.flags['deferred'] = self.flags['deferred']
        n1.flags['deferred_expressions'] = self.flags['deferred_expressions'].copy()
        n1.flags['cc'] = self.flags['cc'].copy()
        return n1

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

    def _scale_degrees_to_steps(self, input):
        """
        A 3rd "3" is 3 steps, but a "b3" (minor third) is 2.5 and a "#3" (augmented third) is 3.5
        This is used in scale.py to make defining scales easier.
        See https://en.wikipedia.org/wiki/List_of_musical_scales_and_modes
        """
        return SCALE_DEGREES_TO_STEPS[str(input)]


    def scale_transpose(self, scale_obj, steps):
        """
        Return the note N steps up (or down) within the current scale.
        """

        #assert scale is not None
        #assert steps is not None

        snn = self.note_number()

        scale_notes = scale_obj.generate(length=120)
        #print("SCALE_NOTES=%s" % scale_notes)
        note_numbers = [ x.note_number() for x in scale_notes ]
        #print("NN=%s" % note_numbers)
        #print("NN=%s" % note_numbers)
        #print("SNN=%s" % snn)

        index = None
        for (i,x) in enumerate(note_numbers):
            if snn >= x:
                index = i

        new_index = index + steps
        #print("NEW INDEX=%s" % index)

        scale_note = scale_notes[new_index]
        return Note(name=scale_note.name, octave=scale_note.octave, length=self.length, start_time=self.start_time,
                    end_time=self.end_time, tie=self.tie, flags=self.flags, from_scale=scale_obj)


    def with_velocity(self, velocity):
        """
        Return a copy of this note with the set velocity
        """
        n1 = self # .copy()
        n1.velocity = velocity
        return n1

    def with_octave(self, octave):
        """
        Return a copy of this note with the set octave.
        """
        n1 = self # .copy()
        n1.octave = octave
        return n1

    def with_cc(self, channel, value):
        """
        Return a copy of the note with the set MIDI CC value.
        """
        n1 = self # .copy()
        n1.flags["cc"][str(channel)] = value
        return n1

    def _offset(self, semitones):
        """
        Calls into the note table for note math - whose code we should probably rewrite
        """
        # FIXME: rewrite/eliminate
        return note_table.offset(self, semitones)

    def transpose(self, steps=0, semitones=0, degrees=None, octaves=0):
        """
        Returns a note a given number of steps or octaves or (other things) higher.
        steps -- half step as 0.5, whole step as 1, or any combination.  The most basic way to do things.
        semitones - 1 semitone is simply a half step.  Provided to keep some implementations more music-literate.
        octaves - 6 whole steps, or 12 half steps.  Easy enough.
        degrees - scale degrees, to keep scale definition somewhat music literate.  "3" is a third, "b3" is a flat third, "3#" is an augmented third, etc.
        You can combine all of them at the same time if you really want (why?), in which case they are additive.
        """

        if degrees is not None:
            degrees = str(degrees)
            degree_steps = self._scale_degrees_to_steps(degrees)
        else:
            degree_steps = 0
        if steps is None:
            steps = 0
        if octaves is None:
            octaves = 0
        if semitones is None:
            semitones = 0

        steps = steps + (semitones * 0.5) + degree_steps

        result = self.copy()

        if steps:
            result = self._offset(steps)
        if octaves:
            result.octave = result.octave + octaves
        return result

    def note_number(self):
        """
        What order is this note on the keyboard?
        """
        if self.name is None:
            # FIXME: when does this happen? ties maybe? does it still happen?
            return None
        nn = NOTES.index(self.name) + (12 * self.octave)
        return nn

    def __eq__(self, other):
        """
        Are two notes the same?
        """
        return self.note_number() == other.note_number()

    def __lt__(self, other):
        """
        Compare note ordering
        """
        return self.note_number() < other.note_number()

    def __repr__(self):
        # FIXME: simplify as this is no longer used for debug
        return "Note<%s%s,LEN=%s,s=%s,e=%s,cc=%s>" % (self.name, self.octave, self.length,self.start_time, self.end_time, self.flags['cc'])

def note(st):
     """
     note('Db3') -> Note(name='Db', octave=3)
     """
     if type(st) == Note:
         return st
     match = NOTE_SHORTCUT_REGEX.match(st)
     if not match:
         raise InvalidNote("cannot form note from: %s" % st)
     name = match.group(1)
     octave = match.group(2)
     if octave == '' or octave is None:
        octave = 4
     octave = int(octave)
     return Note(name=name, octave=octave, length=None)

from . base import BaseObject
from classforge import Class, Field

from functools import total_ordering
import re

NOTE_SHORTCUT_REGEX = re.compile("([A-Za-z#]+)([0-9]*)")

# ours
from .. utils.utils import roll_left, roll_right

NOTES          = [ 'C',  'Db', 'D', 'Eb', 'E',  'F',  'Gb', 'G',  'Ab', 'A', 'Bb', 'B' ]
EQUIVALENCE    = [ 'C',  'C#', 'D', 'D#', 'E',  'F',  'F#', 'G',  'G#', 'A', 'A#', 'B' ]
UP_HALF_STEP   = roll_left(NOTES)
DOWN_HALF_STEP = roll_right(NOTES)

SCALE_DEGREES_TO_STEPS = {
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

@total_ordering
class Note(BaseObject):

    name = Field(type=str)
    octave = Field(type=int, default=4, choices=[0,1,2,3,4,5,6,7,8,9,10,None],)
    tie = Field(type=bool, default=False)
    length = Field(type=int, default=None)
    start_time = Field(type=int, default=None)
    end_time = Field(type=int, default=None)

    def on_init(self):
        self.name =  self._equivalence(self.name)
        super().on_init()

    def copy(self):
        return Note(name=self.name, octave=self.octave)

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
            degree_steps = self._scale_degrees_to_steps(degrees)
        else:
            degree_steps = 0
        if steps is None:
            steps = 0
        if octaves is None:
            octaves = 0
        if semitones is None:
            semitones = 0

        steps = steps + (octaves * 6) + (semitones * 0.5) + degree_steps

        note = self
        if steps > 0:
            while steps > 0:
                note = note.up_half_step()
                steps = steps - 0.5
        else:
            while steps < 0:
                note = note.down_half_step()
                steps = steps + 0.5
        return note

    def expand_notes(self):
        return [ self ]

    def _numeric_name(self):
        """
        Give a number for the note - used by internals only
        """
        return NOTES.index(self.name)

    def note_number(self):
        """
        What order is this note on the keyboard?
        """
        nn = NOTES.index(self.name) + (12 * self.octave)
        return nn

    def up_half_step(self):
        """
        What note is a half step up from this one?
        """
        number = self._numeric_name()
        name = UP_HALF_STEP[number]
        if self.name == 'B':
            return Note(name=name, octave=self.octave + 1, length=self.length)
        return Note(name=name, octave=self.octave, length=self.length)

    def down_half_step(self):
        """
        What note is a half step down from this one?
        """
        number = self._numeric_name()
        name = DOWN_HALF_STEP[number]
        if self.name == 'C':
            return Note(name=name, octave=self.octave - 1, length=self.length)
        return Note(name=name, octave=self.octave, length=self.length)

    def __eq__(self, other):
        """
        Are two notes the same?
        """
        return self.note_number() == other.note_number()

    def __lt__(self, other):
        """
        Are two notes the same?
        """
        return self.note_number() < other.note_number()

    def short_name(self):
         """
         Returns a string like Eb4
         """
         return "%s%s" % (self.name, self.octave)

    def __repr__(self):
         return "Note<%s%s,d=%s,s=%s,e=%s>" % (self.name, self.octave, self.length,self.start_time, self.end_time)

def note(st):
     """
     note('Db3') -> Note(name='Db', octave=3)
     """
     if type(st) == Note:
         return st
     match = NOTE_SHORTCUT_REGEX.match(st)

     print("trying to match: %s, %s" % (st, type(st)))
     if not match:
         raise Exception("cannot form note from: %s" % st)
     name = match.group(1)
     octave = match.group(2)
     if octave == '' or octave is None:
        octave = 4
     octave = int(octave)
     return Note(name=name, octave=octave, length=None)


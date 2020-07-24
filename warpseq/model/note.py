from . base import BaseObject
from classforge import Class, Field

from . import note_table

from functools import total_ordering
import re

DEFAULT_VELOCITY = 120
NOTE_SHORTCUT_REGEX = re.compile("([A-Za-z#]+)([0-9]*)")

# ours
from .. utils.utils import roll_left, roll_right

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

@total_ordering
class Note(BaseObject):

    name = Field(type=str)
    octave = Field(type=int, default=4, nullable=True)
    tie = Field(type=bool, default=False)
    length = Field(type=int, default=None)
    start_time = Field(type=int, default=None)
    end_time = Field(type=int, default=None)
    flags = Field(type=dict, default=None, required=False)
    velocity = Field(type=int, default=DEFAULT_VELOCITY, required=False)
    from_scale = Field(default=None)

    def on_init(self):
        self.name =  self._equivalence(self.name)
        if self.flags is None:
            self.flags = {}
            self.flags['deferred'] = False
            self.flags['deferred_expressions'] = []
            self.flags['cc'] = dict()
        super().on_init()

    def copy(self):
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
        from . chord import Chord
        return Chord(root=self.copy(), chord_type=chord_type)

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


    def scale_transpose(self, scale, steps):

        index = 0
        found = False
        snn = self.note_number()
        for note in scale.generate(length=145):
            nn = note.note_number()
            if nn > snn:
                found = True
                break
            index = index + 1

        if not found:
            raise Exception("unexpected scale_transpose error (1): note not in scale: (%s, %s, %s)" % (scale.name, note.name, note.octave))

        new_index = index + steps

        find_index = 0
        for note in scale.generate(length=145):
            if find_index == new_index:
                return Note(name=note.name, octave=note.octave, length=self.length, start_time=self.start_time, end_time=self.end_time, tie=self.tie, flags=self.flags)
            find_index = find_index + 1

        raise Exception("unexpected scale transpose error (2)")

    def with_velocity(self, velocity):
        n1 = self.copy()
        n1.velocity = velocity
        return n1

    def adjust_velocity(self, mod):
        n1 = self.copy()
        if n1.velocity is None:
            n1.velocity = 120 # FIXME: use a constant
        n1.velocity = n1.velocity + mod
        return n1

    def with_octave(self, octave):
        n1 = self.copy()
        n1.octave = octave
        return n1

    def with_cc(self, channel, value):
        n1 = self.copy()
        n1.flags["cc"][str(channel)] = value
        return n1

    def offset(self, semitones):
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
        # FIXME: implement without offset to not need the note_table, then delete the note_table

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

        steps = steps + (octaves * 6) + (semitones * 0.5) + degree_steps

        if steps:
            return self.offset(steps)
        else:
            return self

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
        # FIXME: when does this happen? ties maybe? does it still happen?
        if self.name is None:
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
        Are two notes the same?
        """
        return self.note_number() < other.note_number()

    def short_name(self):
         """
         Returns a string like Eb4
         """
         return "%s%s" % (self.name, self.octave)

    def __repr__(self):
         # FIXME: simplify and remove CTR
         return "Note<%s%s,LEN=%s,s=%s,e=%s,cc=%s>" % (self.name, self.octave, self.length,self.start_time, self.end_time, self.flags['cc'])

def note(st):
     """
     note('Db3') -> Note(name='Db', octave=3)
     """
     if type(st) == Note:
         return st
     match = NOTE_SHORTCUT_REGEX.match(st)
     if not match:
         raise Exception("cannot form note from: %s" % st)
     name = match.group(1)
     octave = match.group(2)
     if octave == '' or octave is None:
        octave = 4
     octave = int(octave)
     return Note(name=name, octave=octave, length=None)


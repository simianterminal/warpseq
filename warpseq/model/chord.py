# Copyright 2016-2020, Michael DeHaan <michael@michaeldehaan.net>

from .base import BaseObject
from .pattern import Pattern
from classforge import Class, Field
from .transform import Transform
from .scale import Scale
from .note import Note, note

# https://en.wikipedia.org/wiki/Chord_names_and_symbols_(popular_music)
# minor 2nd - 2 semitones
# minor 3rd - 3 semitones
# major 3rd - 4 semitones
# perfect 4th - 5 semitones
# perfect 5th - 7 semitones
# major 6th - 9 semitones
# major 7th - 11 semitones
# octave - 12 semitones
# etc

CHORD_TYPES = dict(
   minor = [ 3, 7 ],
   major = [ 4, 7 ],
   dim = [ 3, 6 ],
   aug = [ 4, 8 ],
   sus4 = [ 5, 7 ],
   sus2 = [ 2, 7 ],
   fourth = [ 5 ],
   power = [ 7 ],
   fifth = [ 7 ],
   M6 = [ 4, 7, 9 ],
   m6 = [ 3, 7, 9 ],
   dom7 = [ 4, 7, 10 ],
   M7 = [ 4, 7, 11 ],
   m7 = [ 3, 7, 10 ],
   aug7 = [ 4, 8, 10 ],
   dim7 = [ 3, 6, 10 ],
   mM7 = [ 3, 7, 11 ]
)

CHORD_TYPE_KEYS = [x for x in CHORD_TYPES.keys()]

class Chord(BaseObject):

    notes = Field(type=list, required=False, nullable=True)
    root = Field(type=Note, required=False, nullable=True)
    chord_type = Field(type=str, required=False, choices=CHORD_TYPE_KEYS, default=None, nullable=True)

    """
    Constructs a chord, in different ways:
    notes = [ note('C4'), note('E4'), note('G4') ]
    chord = Chord(notes=notes)
    OR:
    chord = Chord(root=note('C4'), chord_type='major')
    OR:
    chord = Chord(root='C4', chord_type='major')
    """

    def on_init(self):


        if self.notes and self.root:
            raise Exception("notes and root are mutually exclusive")
        if self.notes is None and self.root is None:
            raise Exception("specify either notes or root")

        if self.root and self.chord_type is None:
            raise Exception("chord_type is required when using root=")

        if isinstance(self.root, str):
            self.root = note(root)

        if self.notes is not None:
            for x in self.notes:
                assert type(x) == Note
        else:
            self.notes = self._chordify()

    def chordify(self, chord_type):
        return Chord(root=self.notes[0].copy(), chord_type=chord_type)

    def copy(self):
        notes = [ n.copy() for n in self.notes ]
        return Chord(notes=notes)

    def with_velocity(self, velocity):
        c1 = self.copy()
        for n in c1.notes:
            n.velocity = velocity
        return c1

    def adjust_velocity(self, mod):
        ch = self.copy()
        ch.notes = [ x.adjust_velocity(mod) for x in ch.notes ]
        return ch

    def with_cc(self, channel, num):
        ch = self.copy()
        ch.notes = [ x.with_cc(channel, num) for x in ch.notes ]
        return ch

    def with_octave(self, octave):
        c1 = self.copy()
        for n in c1.notes:
            n.octave = octave
        return c1

    def _chordify(self):
        """
        Internal method.
        Once self.root is set to a note, and self.typ is a chord type, like 'major', return the notes in the chord.
        """
        offsets = CHORD_TYPES[self.chord_type]
        notes = []
        notes.append(self.root)
        for offset in offsets:
            notes.append(self.root.transpose(semitones=offset))
        return notes

    def expand_notes(self):
        return [ n for n in self.notes ]

    def __eq__(self, other):
        """
        Chords are equal if they contain the same notes.
        """
        return sorted(self.notes) == sorted(other.notes)

    def transpose(self, steps=None, semitones=None, octaves=None):
        """
        Transposing a chord is returns a new chord with all of the notes transposed.
        """
        notes = [ note.transpose(steps=steps, octaves=octaves, semitones=None) for note in self.notes ]
        return Chord(notes=notes)

    def invert(self, amount=1, octaves=1):
        """
        Inverts a chord.
        ex: chord("c4 major").invert() -> chord(["E4","G4","C5"])
        """
        new_chord = self.copy()
        if amount >= 1:
            new_chord.notes[0] = new_chord.notes[0].transpose(octaves=octaves)
        if amount >= 2:
            new_chord.notes[1] = new_chord.notes[1].transpose(octaves=octaves)
        if amount >= 3:
            new_chord.notes[2] = new_chord.notes[2].transpose(octaves=octaves)
        return new_chord

def chord(input):
    """
    Shortcut: chord(['C5', 'E5', 'G5') -> Chord object
    Shortcut: chord('C5 dim') -> Chord object
    """
    if type(input) == list:
        notes = [ note(n) for n in input ]
        return Chord(notes=notes)
    else:
        tokens = input.split()
        assert len(tokens) == 2, "invalid chord expression: %s" % input
        return Chord(root=note(tokens[0]), chord_type=tokens[1])
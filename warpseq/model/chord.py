# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# basic modelling of chords as an array of notes, or a root note
# with a chord type.

from ..api.exceptions import *
from .base import BaseObject
from .note import Note
from .pattern import Pattern
from .scale import Scale
from .transform import Transform

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
   minor = ( 3, 7 ),
   major = ( 4, 7 ),
   dim = ( 3, 6 ),
   aug = ( 4, 8 ),
   sus4 = ( 5, 7 ),
   sus2 = ( 2, 7 ),
   fourth = ( 5, ),
   power = ( 7, ),
   fifth = ( 7, ),
   M6 = ( 4, 7, 9 ),
   m6 = ( 3, 7, 9 ),
   dom7 = ( 4, 7, 10 ),
   M7 = ( 4, 7, 11 ),
   m7 = ( 3, 7, 10 ),
   aug7 = ( 4, 8, 10 ),
   dim7 = ( 3, 6, 10 ),
   mM7 = ( 3, 7, 11 )
)

CHORD_TYPE_KEYS = set([x for x in CHORD_TYPES.keys()])

class Chord(object):

    """
    Constructs a chord, in different ways:
    notes = [ note('C4'), note('E4'), note('G4') ]
    chord = Chord(notes=notes)
    OR:
    chord = Chord(root=note('C4'), chord_type='major')
    OR:
    chord = Chord(root='C4', chord_type='major')
    """

    __slots__ = ( "notes", "root", "chord_type", "from_scale" )

    def __init__(self, notes=None, root=None, chord_type=None, from_scale=None):

        self.notes = notes
        self.root = root
        self.chord_type = chord_type
        self.from_scale = from_scale

        if self.notes is None:
            self.notes = self._chordify()

    def chordify(self, chord_type):
        """
        This takes an existing chord and returns a new chord of a different type with the same root note.
        """
        return Chord(root=self.notes[0].copy(), chord_type=chord_type, from_scale=self.notes[0].from_scale)

    def copy(self):
        """
        Returns a new chord with exactly the same information. We can throw away the chord type
        as we don't need it, and the chord might not have been constructed with one.
        """
        return Chord(notes=self.notes, from_scale=self.from_scale)

    def with_velocity(self, velocity):
        """
        Returns a copy of the chord with every note in the chord having a set velocity
        """
        return Chord(notes=[x.with_velocity(velocity) for x in self.notes], from_scale=self.from_scale)

    def with_cc(self, channel, num):
        """
        Returns a copy of the chord with each note having a certain MIDI CC value filled in
        """
        return Chord(notes = [ x.with_cc(channel, num) for x in self.notes ], from_scale=self.from_scale)

    def with_octave(self, octave):
        """
        Returns a copy of the chord with all notes set to a certain octave.
        This is probably musically bad (will break the sound) but is required to support the mod expression O=3 generically
        for both chords and notes. It would be much better to use the mod expression O+1 or O-1.
        """
        if not self.notes:
            return self.copy()
        delta = octave - self.notes[0].octave
        return Chord(notes=[ n.with_octave(n.octave+delta) for n in self.notes ], from_scale=self.from_scale)


    def _chordify(self):
        """
        Internal method.
        Once self.root is set to a note, and self.chord_type is a chord type, like 'major', return the notes in the chord.
        """
        offsets = CHORD_TYPES[self.chord_type]
        notes = []
        notes.append(self.root)
        for offset in offsets:
            notes.append(self.root.transpose(semitones=offset))
        return notes

    #def __eq__(self, other):
    #    """
    #    Chords are equal if they contain the same notes.
    #    """
    #    return sorted(self.notes) == sorted(other.notes)

    def transpose(self, steps=None, semitones=None, octaves=None):
        """
        Transposing a chord is returns a new chord with all of the notes transposed.
        """
        notes = [ note.transpose(steps=steps, octaves=octaves, semitones=semitones) for note in self.notes ]
        return Chord(notes=notes, from_scale=notes[0].from_scale)

    def invert(self, amount=1, octaves=1):
        """
        Inverts a chord.
        ex: chord("c4 major").invert() -> chord(["E4","G4","C5"])
        """
        # TODO: this should be surfaced in mod expressions, and if used with a note, ignored
        new_chord = self.copy()
        if amount >= 1:
            new_chord.notes[0] = new_chord.notes[0].transpose(octaves=octaves)
        if amount >= 2:
            new_chord.notes[1] = new_chord.notes[1].transpose(octaves=octaves)
        if amount >= 3:
            new_chord.notes[2] = new_chord.notes[2].transpose(octaves=octaves)
        return new_chord


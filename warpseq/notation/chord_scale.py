# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class evaluates symbols like "I", "IV", and "1" or "4" and returns
# the notes and chords in the current scale. Contrast with literal.py

from ..api.exceptions import *
from ..model.chord import Chord, chord
from ..model.scale import Scale, scale

CHORD_SYMBOLS = dict(
   I   = [ 1, 'major' ],
   II  = [ 2, 'major' ],
   III = [ 3, 'major' ],
   IV  = [ 4, 'major' ],
   V   = [ 5, 'major' ],
   VI  = [ 6, 'major' ],
   VII = [ 7, 'major' ],
   i   = [ 1, 'minor' ],
   ii  = [ 2, 'minor' ],
   iii = [ 3, 'minor' ],
   iv  = [ 4, 'minor' ],
   v   = [ 5, 'minor' ],
   vi  = [ 6, 'minor' ],
   vii = [ 7, 'minor' ],
)
CHORD_SYMBOLS['-'] = 'REST'

class ChordScale(object):

    def __init__(self, scale=None):

        """
        Constructs an interpreter for Roman numbering.
        scale1 = scale("C4 major")
	    roman = Roman(scale=scale1)
        roman.do("IV") == chord("F4 major")
        roman.do(4) == note("F4")
        """

        assert scale is not None
        self.scale = scale
        self._note_buffer = self.scale.generate(length=150)

    def chord(self, sym):
        """
        Accepts symbols like ii, II, IV:power
        (the latter being a bit of a notation hack so we might want to change it)
        """

        # normally chords will be like II or ii, but occasionally II:power
        # if so, we'll ignore our usual roman parsing and let the chord type after
        # the colon win
        override_typ = None
        if ":" in sym:
           (sym, override_typ) = sym.split(":",1)

        # inversion syntax is disabled, use a mod expression instead (TODO)
        #
        #inversion = 0
        #if sym.endswith("''''"):
        #    inversion = 3
        #    sym = sym.replace("'''","")
        #elif sym.endswith("''"):
        #    inversion = 2
        #    sym = sym.replace("''","")
        #elif sym.endswith("'"):
        #    inversion = 1
        #    sym = sym.replace("'","")

        # here's where we figure out what roman numbers are which, and if the
        # roman number implies a chord type (it does - but it might be overridden
        # above).
        chord_data = CHORD_SYMBOLS.get(sym, None)
        if chord_data is None:
           raise InvalidSymbol("do not know how to parse chord symbol: %s" % sym)

        if chord_data == 'REST':
            return None

        # here's where we override the chord type if need be
        (scale_num, typ) = chord_data
        if override_typ is not None:
            typ = override_typ

        # now return the built chord, of the right type, inverting if required
        base_note = self.note(scale_num)
        return Chord(root=base_note, chord_type=typ)


    def note(self, sym):
        position = int(sym) - 1
        rc = self._note_buffer[position].copy()
        return rc

    def do(self, sym):
        """
        Generate a note from a symbol like '2', or a chord from a symbol like
        'ii' or 'II'.
        """
        try:
            int(sym)
        except ValueError:
            return self.chord(sym)
        return self.note(sym)

    def do_notes(self, sym):
        """
        Same as do() but always get back an array of notes.
        """
        if sym is None:
            return []
        note_or_chord = self.do(sym)
        if note_or_chord is None:
            return []
        elif type(note_or_chord) == Chord:
            return [ n.copy() for n in note_or_chord.notes ]
        else:
            return [ note_or_chord ]

def chord_scale(scale_pattern):
    """
    Quickly generate a Roman numeral interpreter.
    Ex: r = roman("C4 major")
    """
    return ChordScale(scale=scale(scale_pattern))
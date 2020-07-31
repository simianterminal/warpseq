# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class allows note entry of symbols like "C4" and "Eb4"

from .. model.note import note
from .. model.chord import chord, Chord

class Literal(object):

    def __init__(self):

        """
        Constructs an interpreter for specific note names or chords.
        It doesn't need to know a scale and is pretty basic.
	    literal = Literal()
        roman.do("C4,E4,G4") == chord("C4 major")
        roman.do("C4 major") == chord("C4,E4,G4")
        roman.do("C4") == note("C4")
        """
        pass

    def do(self, sym):
        """
        Accepts symbols like C4-major or C4,E4,G4
        or note symbols like 'C4'
        """
        # The dash is a bit of a notation hack, it's there because "C4 major"
        # would look like two symbols, so we need to have no whitespace
        # between them

        if ' ' in sym:
            sym = sym.replace(' ','-')
        if sym is None or sym == '-':
            # REST:
            return chord([])
        if '-' in sym:
            return chord(sym.replace("-", " "))
        elif "," in sym:
            return chord(sym.split(","))
        else:
            return note(sym)

    def do_notes(self, sym):
        """
        Same as do() but always get back an array of notes.
        """
        # DRY: duplication with Roman.py - FIXME
        if sym == '-':
            # REST
            return []
        note_or_chord = self.do(sym)
        if note_or_chord is None:
            return []
        elif type(note_or_chord) == Chord:
            return [ n.copy() for n in note_or_chord.notes ]
        else:
            return [note_or_chord]


def literal():
    """
    The shortcut method here isn't highly useful, but it's being provided
    to line up with the REST of the API.
    """
    return Literal()
# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# uses the code in smart.py or literal.py to evaluate a symbol that
# might be supported by either of those other classes. Also processes
# any mod expressions after those symbols.  Used in clip evaluation.

from ..api.exceptions import *
from ..model.note import Note, NOTES, EQUIVALENCE
from ..model.chord import Chord, CHORD_TYPES
from .mod import ModExpression

import functools
import traceback
import re
import time

NOTE_SHORTCUT_REGEX = re.compile("([A-Za-z#]+)([0-9]*)")
#INT_REGEX = re.compile("^[0-9]+$")

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


INTEGERS = set([ str(x) for x in range(-40,40) ])

class ExpressionEvaluationError(Exception):
    pass

class NoteParser(object):

    __SLOTS__ = [ 'scale', 'song', 'clip', 'track', 'pattern', '_chord_scale', '_literal', '_mod', '_slot_duration']

    def __init__(self, scale=None, song=None, clip=None, track=None, pattern=None):
        self.scale = scale
        self.song = song
        self.clip = clip
        self.track = track
        self.pattern = pattern

    def setup(self):
        self._mod = ModExpression(defer=False)
        self._slot_duration = round(self.clip.slot_duration(self.song, self.pattern))

    def do(self, sym, octave_shift):
        """
        Converts a symbol or list of symbols into an array of chords or notes.
        This uses a combination of the 'literal' and 'smart' evaluator and therefore
        does not exactly have the same API.
        """

        items = None
        if type(sym) == list:
            items = sym
        else:
            items = [ sym ]

        all_notes = []

        for sym in items:

            if sym is None:
                sym = ""

            sym = str(sym).strip()
            tokens = sym.split(None)

            if sym:
                sym = tokens[0]
                mod_expressions = tokens[1:]
            else:
                sym = ''
                mod_expressions = ''

            strategy = self._get_strategy(sym)
            res = strategy(sym)

            if not res:
                all_notes.extend([None])
                continue

            if type(res) == Chord:
                notes = res.notes
            else:
                notes = [ res ]

            for note in notes:
                if note:
                    note.length = self._slot_duration
                    if not note.tie:
                        note.octave = note.octave + octave_shift

            notes = self._process_mod_expressions(notes, mod_expressions)

            all_notes.extend(notes)

        return all_notes


    @functools.lru_cache(maxsize=256)
    def _get_strategy(self, sym):

        # FIXME: a rest should be a real note and not NONE because we can affix other
        # mod expressions to it.  We could consider it being a note with velocity 0?

        if sym is None or sym in [ "" , "_", "."]:
            # "x", "_", "", None, etc
            return self._rest_strategy
        elif sym == "-":
            # "-"
            return self._tie_strategy
        elif sym in INTEGERS: # INT_REGEX.match(sym):
            # 1, 4, -2
            return self._scale_note_strategy
        elif sym in CHORD_SYMBOLS.keys() or ":" in sym:
            # I, IV, ivv, 3:major
            return self._scale_chord_strategy
        elif NOTE_SHORTCUT_REGEX.match(sym):
            # C4, Eb4, F#
            return self._literal_note_strategy

        raise InvalidExpression(sym)

    def _rest_strategy(self, sym):
        return None

    def _tie_strategy(self, sym):
        return Note(tie=True, name=None, octave=None, length=int(self._slot_duration))

    def _scale_note_strategy(self, sym):
        return self.scale.get_notes()[int(sym)-1].copy()

    def _scale_chord_strategy(self, sym):
        override_typ = None
        if ":" in sym:
           (sym, override_typ) = sym.split(":",1)
        chord_data = CHORD_SYMBOLS.get(sym, None)
        if chord_data is None:
            raise InvalidSymbol("do not know how to parse chord symbol: %s" % sym)
        (scale_num, typ) = chord_data
        if override_typ is not None:
            typ = override_type
        pos = int(scale_num) - 1
        buffer = self.scale.get_notes()
        return Chord(root=buffer[pos].copy(), chord_type=typ)

    def _literal_note_strategy(self, sym):

        match = NOTE_SHORTCUT_REGEX.match(sym)

        name = match.group(1)
        octave = match.group(2)
        if octave:
            octave = int(octave)
        else:
            octave = 4
        return Note(name=name, octave=octave, length=None)

    def _process_mod_expressions(self, notes, mod_expressions):
        new_notes = []
        for note in notes:
            if mod_expressions is not None:
                new_note = note.copy()
                self._mod.scale = self.scale
                self._mod.track = self.track
                new_note = self._mod.do(new_note, mod_expressions)
                new_notes.append(new_note)
            else:
                new_notes.append(note)
        return new_notes
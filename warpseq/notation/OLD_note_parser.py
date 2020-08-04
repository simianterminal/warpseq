# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# uses the code in smart.py or literal.py to evaluate a symbol that
# might be supported by either of those other classes. Also processes
# any mod expressions after those symbols.  Used in clip evaluation.

import traceback

from ..api.exceptions import *
from ..model.note import Note
from .literal import Literal
from .mod import ModExpression
from .chord_scale import ChordScale
import time

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
        self._chord_scale = ChordScale(self.scale)
        self._literal = Literal()
        self._mod = ModExpression(defer=False)
        self._slot_duration = self.clip.slot_duration(self.song, self.pattern)

    def do(self, clip, sym, octave_shift):
        """
        Converts a symbol or list of symbols into an array of chords or notes.
        This uses a combination of the 'literal' and 'smart' evaluator and therefore
        does not exactly have the same API.
        """

        # if the input isn't a list - make it one
        # FIXME: do we need this, or is it *always* a list?
        #a1 = time.time()

        items = None
        if type(sym) == list:
            items = sym
        else:
            items = [ sym ]

        all_notes = []
        for x in items:
            all_notes.extend(self._do_single(clip, x, octave_shift))

        return all_notes

    # FIXME: the clip should not need to be a parameter below since it is available as self.clip

    def _do_single(self, clip, sym, octave_shift):

        """
        Processes a single expression and returns an array of notes.
        The symbol might represent a note or chord and may contain one or more mod expressions.
        """

        # we allow note symbols like "1" to be integers in slots - for consistency though, convert them to strings now
        sym = str(sym)
        sym = sym.strip()

        # an empty clip is a REST, return nothing.
        if sym in [ None, "" ]:
            return [ None ]

        # split off any mod expressions from the base symbol
        tokens = sym.split()

        sym = tokens[0]
        mod_expressions = tokens[1:]

        # an empty string or an _ means no notes
        if sym == "" or sym == "_" or sym == ".":
            return []

        # a hyphen means to tie the previous notes
        if sym == "-":
            return [ Note(tie=True, name=None, octave=None, length=int(self._slot_duration)) ]

        # ready to figure out what notes we are going to return for this expression
        notes = None

        # TODO: FIXME: combine processing to be less exception based

        # HACK: if the note incoming is negative it will jump off our scale math, so
        # instead convert it to a transposition.

        if sym is not None and ((type(sym) == int) or sym.startswith("-")):
            x = int(sym)
            if x < 0:
                sym = 1
                if mod_expressions is None:
                    mod_expressions = ""
                mod_expressions.append("S%s" % x)

        # try to process chord notes then literal notes
        try:
            notes = self._chord_scale.do_notes(sym)
        except Exception:
            # FIXME: we should have specific exception types here
            pass

        if not notes and not is_int:
            try:
                notes = self._literal.do_notes(sym)
            except Exception:
                # FIXME: we should have specific exception types here
                pass

        # if neither of the above worked, we have to give up
        if not notes:
            raise InvalidSymbol("evaluation failed: (%s)" %  sym)

        # apply octave shifts AND ...
        # assign a length to all the notes based on the clip settings
        # this may be modified later by the arp selection (if set)
        assert self.pattern is not None
        slot_duration = clip.slot_duration(self.song, self.pattern)
        for note in notes:
            note.length = round(slot_duration)
            note.octave = note.octave + octave_shift

        # if the note was trailed by any mod expressions, apply them to all notes
        # to be returned
        new_notes = []
        for note in notes:
            new_note = note.copy()
            if mod_expressions is not None:
                self._mod.scale = self.scale
                self._mod.track = self.track
                new_note = self._mod.do(new_note, mod_expressions)
            new_notes.append(new_note)


        return new_notes

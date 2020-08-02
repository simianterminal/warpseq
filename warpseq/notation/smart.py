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
from .roman import Roman
import time

class ExpressionEvaluationError(Exception):
    pass

class SmartExpression(object):

    __SLOTS__ = [ 'scale', 'song', 'clip', 'track', 'pattern', '_roman', '_literal', '_mod', '_slot_duration']

    def __init__(self, scale=None, song=None, clip=None, track=None, pattern=None):
        self.scale = scale
        self.song = song
        self.clip = clip
        self.track = track
        self.pattern = pattern


        self._roman = Roman(self.scale)
        self._literal = Literal()
        self._mod = ModExpression(defer=False)
        self._slot_duration = self.clip.slot_duration(self.song, self.pattern)

    def do(self, clip, sym):
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
            all_notes.extend(self._do_single(clip, x))

        #a2 = time.time()=
        #print("A=%s" % (a2-a1))


        return all_notes

    # FIXME: the clip should not need to be a parameter below since it is available as self.clip

    def _do_single(self, clip, sym):


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

        # first try roman numeral notation (chords are roman, scale notes are arabic)
        try:
            notes = self._roman.do_notes(sym)
        except Exception:
            # FIXME: we should have specific exception types here
            pass

        # if roman numerals failed, try literals like C4 or C4major
        if not notes:
            try:
                notes = self._literal.do_notes(sym)
            except Exception:
                # FIXME: we should have specific exception types here
                pass

        # if neither of the above worked, we have to give up
        if not notes:
            # FIXME: raise a specific exception type
            raise InvalidSymbol("evaluation failed: (%s)" %  sym)

        # assign a length to all the notes based on the clip settings
        # this may be modified later by the arp selection (if set)
        assert self.pattern is not None
        slot_duration = clip.slot_duration(self.song, self.pattern)
        for note in notes:
            note.length = round(slot_duration)

        # if the note was trailed by any mod expressions, apply them to all notes
        # to be returned
        new_notes = []
        for note in notes:
            new_note = note.copy()
            if mod_expressions is not None:
                new_note = self._mod.do(new_note, self.scale, self.track, mod_expressions)
            new_notes.append(new_note)


        return new_notes

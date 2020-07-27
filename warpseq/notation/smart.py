from . literal import Literal
from . roman  import Roman
from . mod import ModExpression
from .. model.note import Note
from classforge import Class, Field

import traceback


class ExpressionEvaluationError(Exception):
    pass

class SmartExpression(Class):

    scale = Field(type=str, required=True, nullable=False)
    song = Field(required=True, nullable=False)
    clip = Field(required=True, nullable=False)
    track = Field(required=True, nullable=False)
    pattern = Field(required=True, nullable=False)

    _previous = Field()
    _roman = Field()
    _literal = Field()
    _mod = Field()
    _slot_duration = Field()

    def on_init(self):
        self._roman = Roman(self.scale)
        self._literal = Literal()
        self._mod = ModExpression(defer=False)
        self._slot_duration = self.clip.slot_duration(self.song, self.pattern)

    def do(self, clip, sym):

        items = None
        if type(sym) == list:
            items = sym
        else:
            items = [ sym ]

        all_notes = []

        for x in items:
            all_notes.extend(self._do_single(clip, x))

        return all_notes

    def _do_single(self, clip, sym):

        sym = str(sym)
        sym = sym.strip()

        if sym in [ None, "" ]:
            return [ None ]

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
            pass

        # if roman numerals failed, try literals like C4 or C4major
        if not notes:
            try:
                notes = self._literal.do_notes(sym)
            except Exception:
                pass

        # if neither of the above worked, we have to give up
        # FIXME: custom exception types
        if not notes:
            raise Exception("evaluation failed: (%s)" %  sym)

        # assign a length to all the notes based on the clip settings
        # this may be modified later by the arp selection (if set)
        slot_duration = clip.slot_duration(self.song)
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
        self._previous = new_notes

        return new_notes

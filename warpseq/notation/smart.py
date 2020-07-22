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

    _previous = Field()
    _roman = Field()
    _literal = Field()
    _mod = Field()
    _slot_duration = Field()

    def on_init(self):
        self._roman = Roman(self.scale)
        self._literal = Literal()
        self._mod = ModExpression(defer=False)
        self._slot_duration = self.clip.slot_duration(self.song)

    def do(self, clip, sym):

        # TODO: this needs more magic here to support intra-track expressions and so on.

        # ensure the input is a string - this is mostly only a concern in test code
        sym = str(sym)
        sym = sym.strip()

        # we can write notes like 3;O+2;# -- third scale note, up two octaves, then sharp
        mod_expressions = ""
        if ";" in sym:
            (sym, mod_expressions) = sym.split(";", 1)

        # an empty string or an _ means no notes
        if sym == "" or sym == "_":
            return []

        # a hyphen means to tie the previous notes
        if sym == "-":
            print("APPLYING TIE: %s" % int(self._slot_duration))
            return [ Note(tie=True, name=None, octave=None, length=int(self._slot_duration)) ]

        # ready to figure out what notes we are going to return for this expression
        notes = None


        # first try roman numeral notation (chords are roman, scale notes are arabic)
        try:
            notes = self._roman.do_notes(sym)
            #print("S2: %s" % notes)
        except Exception:
            #traceback.print_exc()
            pass

        # if roman numerals failed, try literals like C4 or C4major
        if not notes:
            try:
                notes = self._literal.do_notes(sym)
                #print("S1: %s" % notes)
            except Exception:
                #traceback.print_exc()
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

        # FIXME: I don't think we need this, we can have lists of arps!
        new_notes = []
        for note in notes:
            new_note = note.copy()
            expressions = mod_expressions.split(";")
            for expr in expressions:
                if expr:
                    new_note = self._mod.do(new_note, self.scale, self.track, expr)
            new_notes.append(new_note)

        self._previous = new_notes

        return new_notes

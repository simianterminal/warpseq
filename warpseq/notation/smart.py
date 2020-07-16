from . literal import Literal
from . roman  import Roman
from .. model.note import Note
from classforge import Class, Field

import traceback


class ExpressionEvaluationError(Exception):
    pass

class SmartExpression(Class):

    scale = Field(type=str, required=True, nullable=False)
    song = Field(required=True, nullable=False)
    clip = Field(required=True, nullable=False)

    _previous = Field()
    _roman = Field()
    _literal = Field()

    def on_init(self):
        self._roman = Roman(self.scale)
        self._literal = Literal()



    def do(self, clip, sym):

        # TODO: this needs more magic here to support intra-track expressions and so on.

        if sym == "-":
            return [ Note(tie=True, name=None, octave=None) ]

        sym = str(sym)

        notes = None


        slot_duration = clip.get_slot_duration(self.song)

        try:
            notes = self._roman.do_notes(sym)
            #print("S2: %s" % notes)
        except Exception:
            #traceback.print_exc()
            pass

        if not notes:
            try:
                notes = self._literal.do_notes(sym)
                #print("S1: %s" % notes)
            except Exception:
                #traceback.print_exc()
                pass

        if not notes:
            raise Exception("evaluation failed: %s" %  sym)


        for note in notes:
            note.length = slot_duration

        self._previous = notes

        return notes
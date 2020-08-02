# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# This is the class that evaluates mod expressions to return output.

from ..model.registers import get_first_playing_note
from .mod_parser import is_deferred_expr, process_expr


class ModExpression(object):

    __slots__ = [ 'defer', 'execute_next', 'scale', 'track' ]

    def __init__(self, scale=None, track=None, defer=False):
        self.defer = defer
        self.execute_next = True
        #assert scale is not None
        #assert track is not None
        self.scale = scale
        self.track = track

    def do(self, note, expressions):

        # self.scale = scale

        if type(expressions) != list:
            expressions = str(expressions)
            expressions = expressions.split()

        input_note = note.copy()

        if not self.defer:

            # decide if we need to recompute the note again at play time because it includes intra-track events
            has_deferred = False
            for expr in expressions:
                if is_deferred_expr(expr):
                    has_deferred = True
                    break

            # if we do have intra-track events, we record them on the note for replay later
            if has_deferred:
                input_note.flags['deferred'] = True
                input_note.flags['deferred_expressions'] = expressions

        # execute next is a boolean toggled by probability events
        self.execute_next = True

        expr_index = 0

        for expr in expressions:

            expr_index = expr_index + 1

            # if false, execute next ignores the NEXT event and then toggles back on.
            if self.execute_next == False:
                self.execute_next = True
                continue

            # we might need to process deferred events depending on where this class is invoked
            if self.defer:
                input_note = process_expr(self, input_note, expr, deferred=True)
                if input_note is None:
                    return input_note

            # we ALWAYS need to process non-deferred events
            input_note = process_expr(self, input_note, expr, deferred=False)
            if input_note is None:
                return input_note

        from ..model.note import Note
        #from ..model.chord import Chord


        if type(input_note) == Note:
            input_note.from_scale = self.scale
        else:
            # Chord
            for x in input_note.notes:
                x.from_scale = x

        return input_note

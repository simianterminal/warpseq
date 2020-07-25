"""
Copyright 2020, Michael DeHaan <michael@michaeldehaan.net>
"""

# from .. model.note import note
# from .. model.chord import chord, Chord
from .. model.registers import get_first_playing_note
from . mod_parser import process_expr, is_deferred_expr

class ModExpression(object):

    def __init__(self, defer=False):
        self.defer = defer
        self.execute_next = True
        self.scale = None

    def do(self, note, scale, track, expressions):

        self.scale = scale

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

        input_note.from_scale = self.scale

        return input_note
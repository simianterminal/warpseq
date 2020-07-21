"""
Copyright 2020, Michael DeHaan <michael@michaeldehaan.net>
"""

# from .. model.note import note
# from .. model.chord import chord, Chord
from .. model.registers import get_first_playing_note

# A mod expression can follow a note, like "C4;O+2" or is used in an arpeggiator "O+2

class ModExpression(object):

    def __init__(self, defer=False):
        self.defer = defer

    # FIXME: this needs a lot more error handling and evolution

    def do(self, note, scale, track, expressions):


        if type(expressions) != list:
            expressions = str(expressions)
            expressions = expressions.split(";")

        input_note = note.copy()

        if not self.defer:

            # decide if we need to recompute the note again at play time because it includes intra-track events

            has_deferred = False
            for expr in expressions:
                # if has a deferred expression
                # FIXME: this should include a full list of intra-track event prefixes here, and not be hard coded
                if expr.startswith("T="):
                    has_deferred = True
                    break

            if has_deferred:
                input_note.flags['deferred'] = True
                input_note.flags['deferred_expressions'] = expressions

        for expr in expressions:

            if self.defer:

                if expr.startswith("T="):

                    (_, how) = expr.split("T=")
                    playing = get_first_playing_note(how)
                    if playing is None:
                        pass
                    else:
                        input_note.octave = playing.octave
                        input_note.name = playing.name

            # all remaining events here

            if expr.startswith("O+"):
                # octave up: O+2
                (_, how) = expr.split("O+")
                how = int(how)
                input_note = input_note.transpose(octaves=how)

            elif expr.startswith("O-"):
                # octave down: O-2
                (_, how) = expr.split("O-")
                how = int(how)
                input_note = input_note.transpose(octaves=-how)

            elif expr.startswith("+"):
                # steps up: +1
                (_, how) = expr.split("+")
                how = int(how)
                input_note = input_note.scale_transpose(scale, how)

            elif expr.startswith("-"):
                # steps down: -1
                (_, how) = expr.split("-")
                how = int(how)
                input_note = input_note.scale_transpose(scale, how)

            elif expr.startswith("S+"):
                # steps up: +1
                (_, how) = expr.split("S+")
                how = int(how)
                input_note = input_note.transpose(steps=how)

            elif expr.startswith("S-"):
                # steps down: -1
                (_, how) = expr.split("S-")
                how = int(how)
                input_note = input_note.transpose(steps=-how)

            elif expr == "#":
                input_note = input_note.transpose(semitones=1)

            elif expr == "b":
                input_note = input_note.tranpose(semitones=-1)


            elif expr == 'x':
                return None

        return input_note
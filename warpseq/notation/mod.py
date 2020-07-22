"""
Copyright 2020, Michael DeHaan <michael@michaeldehaan.net>
"""

# from .. model.note import note
# from .. model.chord import chord, Chord
from .. model.registers import get_first_playing_note
import random

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

        execute_next = True

        random.seed()

        for expr in expressions:

            if not execute_next:
                execute_next = True
                continue

            if self.defer:

                # ------------------------------------------------------------------------------------------------------
                # ALL INTRA-TRACK EXPRESSIONS HERE

                if expr.startswith("T="):
                    # note grab: T=euro1

                    (_, how) = expr.split("T=")
                    playing = get_first_playing_note(how)
                    if playing is None:
                        pass
                    else:
                        input_note.octave = playing.octave
                        input_note.name = playing.name
                    continue


            # ---------------------------------------------------------------------------------------------------------
            # ALL STANDARD EXPRESSIONS HERE

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

            # FIXME: consider S+/- for scale transpose and +1/-1 be octaves, but also any number of + and - be octaves

            elif expr.startswith("+"):
                # steps up: +1
                (_, how) = expr.split("+", 1)
                how = int(how)
                input_note = input_note.scale_transpose(scale, how)

            elif expr.startswith("-"):
                # steps down: -1
                (_, how) = expr.split("-", 1)
                how = int(how)
                input_note = input_note.scale_transpose(scale, how)

            elif expr.startswith("S+"):
                # steps up: +1
                (_, how) = expr.split("S+", 1)
                how = int(how)
                input_note = input_note.transpose(steps=how)

            elif expr.startswith("S-"):
                # steps down: -1
                (_, how) = expr.split("S-", 1)
                how = int(how)
                input_note = input_note.transpose(steps=-how)

            elif expr == "#":
                # sharp
                input_note = input_note.transpose(semitones=1)

            elif expr == "b":
                # flat
                input_note = input_note.transpose(semitones=-1)

            elif expr.startswith("p="):
                (_, how) = expr.split("p=", 1)
                how = float(how)
                rn = random.random()
                if rn > how:
                    execute_next = False

            elif expr.startswith("v="):
                (_, how) = expr.split("v=", 1)
                # FIXME: add more helper methods / DRY
                if "," in how:
                    tokens = how.split(",", 1)
                    how = int(random.randrange(int(tokens[0]),int(tokens[1])))
                else:
                    how = int(how)
                input_note = input_note.with_velocity(how)

            elif expr.startswith("ch="):
                (_, how) = expr.split("ch=", 1)
                input_note = input_note.chordify(how)


            elif expr.startswith("cc") and "=" in expr:
                (_, rest) = expr.split("cc", 1)
                (number, how) = rest.split("=", 1)
                #print("num=%s" % number)
                if "," in how:
                    tokens = how.split(",", 1)
                    how = int(random.randrange(int(tokens[0]),int(tokens[1])))
                    #print("apply: %s" % how)
                else:
                    how = int(how)
                    #print("apply2: %s" % how)

                input_note = input_note.with_cc(number, how)


            elif expr in [ '_', 'x', '0' ]:
                input_note = None

            elif expr in [ ".", "1" ]:
                pass

            elif expr.startswith("T="):
                # pass ... deferred for now!
                pass

            else:
                raise Exception("don't know how to process expr: %s" % expr)

        return input_note
"""
Copyright 2020, Michael DeHaan <michael@michaeldehaan.net>
"""

# from .. model.note import note
# from .. model.chord import chord, Chord

# A mod expression can follow a note, like "C4;O+2" or is used in an arpeggiator "O+2

class ModExpression(object):

    def __init__(self):
        pass

    # FIXME: this needs a lot more error handling and evolution

    def do(self, note, scale, expression):

        expression = str(expression)
        expressions = expression.split(";")

        input_note = note.copy()

        for expr in expressions:

            # FIXME: might want a way to +1/-1 scale notes eventually after we do track grabs.  Right now
            # mod expressions can only do absolutes

            # FIXME: yes we need this!

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
# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the parser decides what mod expressions are used and returns
# the appropriate functions to evaluate them.

import random
from . mod_expressions import *
from . mod_util import *

# ----------------------------------------------------------------------------------------------------------------------
# EXPRESSION TABLE
# does not include sharp, flat, tie, and silence operations.

INCREMENTS = {
    "o"  : expr_octave_up,
    "s"  : expr_scale_note_up,
    "d"  : expr_degree_up,
    "$"  : expr_variable_up,
}

DECREMENTS = {
    "o"  : expr_octave_down,
    "s"  : expr_scale_note_down,
    "d"  : expr_degree_down,
    "$"  : expr_variable_up
}

ASSIGNMENTS = {
    "o"  : expr_octave_set,
    "s"  : expr_scale_note_down,
    "v"  : expr_velocity_set,
    "cc" : expr_cc_set,
    "ch" : expr_chord_set,
    "$"  : expr_variable_set,
    "p"  : expr_probability_set,
    "t"  : expr_ignore
}

DEFERRED_ASSIGNMENTS = {
    "o": expr_octave_set,
    "s": expr_scale_note_down,
    "v": expr_velocity_set,
    "cc": expr_cc_set,
    "ch": expr_chord_set,
    "$": expr_variable_set,
    "p": expr_probability_set,
    "t"  : expr_track_grab
}



OPERATIONS = dict(
    normal = dict(
        increments = INCREMENTS,
        decrements = DECREMENTS,
        assignments = ASSIGNMENTS
    ),
    deferred = dict(
        increments = INCREMENTS,
        decrements = DECREMENTS,
        assignments = DEFERRED_ASSIGNMENTS
    )
)



# ----------------------------------------------------------------------------------------------------------------------
# helper functions for process_expr

def perform(parser, note, operations, what, how):

    what = what.lower()

    extra_info = None
    if what.startswith('cc'):
        extra_info = what[2:]
        what = 'cc'

    if what.startswith('$'):
        extra_info = what[1:]
        what = '$'

    if not what in operations:
        raise Exception("unknown mod expression: (%s)" % what)

    routine = operations[what]
    result = routine(parser, note, how, extra_info)
    return result


# ----------------------------------------------------------------------------------------------------------------------
# interface used by mod.py (ModExpression class)

def process_expr(parser, input, expr, deferred=False):

    if expr in [ "_", 'x', "0" ]:
        return silence(input)
    elif expr in ["." , "1", ]:
        return input
    elif expr == "#":
        return sharp(input)
    elif expr == "b":
        return flat(input)

    global OPERATIONS

    table = OPERATIONS['normal']
    if deferred:
        table = OPERATIONS['deferred']

    if "+=" in expr:
        operations = table['increments']
        tokens = expr.split("+=",1)
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "+" in expr:
        # DUPLICATE CODE
        operations = table['increments']
        tokens = expr.split("+",1)
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "-=" in expr:
        operations = table['decrements']
        tokens = expr.split('-=',1)
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "-" in expr:
        # FIXME: duplicate code
        operations = table['decrements']
        tokens = expr.split('-',1)
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "=" in expr:
        operations = table['assignments']
        tokens = expr.split("=",1)
        return perform(parser, input, operations, tokens[0], tokens[1])

    else:
        raise Exception("unknown expr! (%s)" % expr)

def is_deferred_expr(expr):
    expr = expr.lower()
    for (k,v) in DEFERRED_ASSIGNMENTS.items():
        chk = "%s=" % k
        if expr.startswith(chk):
            return True
    return False
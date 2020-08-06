# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the parser decides what mod expressions are used and returns
# the appropriate functions to evaluate them.

import random

from ..api.exceptions import *
from .mod_expressions import *
from .mod_util import *

# ----------------------------------------------------------------------------------------------------------------------
# EXPRESSION TABLE
# does not include sharp, flat, tie, and silence operations.

INCREMENTS = {
    "o"  : expr_octave_up,
    "s"  : expr_scale_note_up,
    "d"  : expr_degree_up
}

DECREMENTS = {
    "o"  : expr_octave_down,
    "s"  : expr_scale_note_down,
    "d"  : expr_degree_down
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
        raise InvalidExpression("unknown mod expression: (%s)" % what)

    routine = operations[what]
    result = routine(parser, note, how, extra_info)
    return result




# ----------------------------------------------------------------------------------------------------------------------
# interface used by mod.py (ModExpression class)

FAST_MAP = {
    "_": silence,
    "x": silence,
    "0": silence,
    "#": sharp,
    "b": flat,
    "1": same,
    ".": same,
}

def process_expr(parser, input, expr, deferred=False):


    fn = FAST_MAP.get(expr, None)
    if fn is not None:
        return fn(input)

    global OPERATIONS

    table = OPERATIONS['normal']
    if deferred:
        table = OPERATIONS['deferred']

    if "+" in expr:
        tokens = expr.replace("+=","+").split("+",1)
        return perform(parser, input, table['increments'], tokens[0], tokens[1])
    elif "-" in expr:
        tokens = expr.replace("-=","-").split('-',1)
        return perform(parser, input,  table['decrements'], tokens[0], tokens[1])
    elif "=" in expr:
        tokens = expr.split("=",1)
        return perform(parser, input, table['assignments'], tokens[0], tokens[1])
    else:
        raise InvalidExpression("unknown expr! (%s)" % expr)

def is_deferred_expr(expr):

    # hard coded to be a bit more efficient

    return expr.startswith("T=") or '$' in expr

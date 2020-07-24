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
    "v"  : expr_velocity_up,
    "cc" : expr_cc_up,
    "$"  : expr_variable_up,
}

DECREMENTS = {
    "o"  : expr_octave_down,
    "s"  : expr_scale_note_down,
    "d"  : expr_degree_down,
    "v"  : expr_velocity_down,
    "cc" : expr_cc_down,
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
    "t"  : expr_track_grab
}


OPERATIONS = dict(
    normal = dict(
        increments = INCREMENTS,
        decrements = DECREMENTS,
        assignments = ASSIGNMENTS
    ),
    deferred = dict(
        increments = dict(),
        decrements = dict(),
        assignments = DEFERRED_ASSIGNMENTS
    )
)

# ----------------------------------------------------------------------------------------------------------------------
# helper functions for process_expr

def perform(parser, note, operations, what, how):

    #print("PERFORM: (%s,%s,%s,%s)" % (parser, note, what, how))

    what = what.lower()

    extra_info = None
    if what.startswith('cc'):
        extra_info = what[2:]
        what = 'cc'

    if what.startswith('$'):
        extra_info = what[1:]
        what = '$'

    if not what in operations:
        raise Exception("unknown mod expression: %s" % what)

    routine = operations[what]
    #print("routine: %s", routine.__name__)
    result = routine(parser, note, how, extra_info)
    #print("RESULT=%s" % result)
    return result


# ----------------------------------------------------------------------------------------------------------------------
# interface used by mod.py (ModExpression class)

def process_expr(parser, input, expr, deferred=False):
    tokens = []

    #print("process_expr: %s" % expr)


    if expr in [ "_", 'x']:
        #print("> silence")
        return silence(input)
    elif expr in ["." , "0", ]:
        #print("> pass")
        return input
    elif expr == "#":
        #print("> sharp")
        return sharp(input)
    elif expr == "b":
        #print("> flat")
        return flat(input)

    global OPERATIONS

    table = OPERATIONS['normal']
    if deferred:
        table = OPERATIONS['deferred']

    if "+=" in expr:
        operations = table['increments']
        tokens = expr.split("+=",1)
        #print("+> %s" % tokens[0])
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "+" in expr:
        # DUPLICATE CODE
        operations = table['increments']
        tokens = expr.split("+",1)
        #print("+> %s" % tokens[0])
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "-=" in expr:
        operations = table['decrements']
        tokens = expr.split('-=',1)
        #print("-> %s" % tokens[0])
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "-" in expr:
        # FIXME: duplicate code
        operations = table['decrements']
        tokens = expr.split('-',1)
        #print("-> %s" % tokens[0])
        return perform(parser, input, operations, tokens[0], tokens[1])
    elif "=" in expr:
        operations = table['assignments']
        tokens = expr.split("=",1)
        return perform(parser, input, operations, tokens[0], tokens[1])

    else:
        raise Exception("unknown expr! (%s)" % expr)
        pass

def is_deferred_expr(expr):
    expr = expr.lower()
    for (k,v) in DEFERRED_ASSIGNMENTS.items():
        chk = "%s=" % k
        if expr.startswith(chk):
            return True
    return False
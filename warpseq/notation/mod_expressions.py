# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this file contains the implementation of all Mod Expression symbols.

from ..model.registers import get_first_playing_note
from .mod_util import *

# ----------------------------------------------------------------------------------------------------------------------
# SPECIAL (these do not take parameters)

def silence(input):
    return None

def sharp(input):
    return input.transpose(semitones=1)

def flat(input):
    return input.transpose(semitones=-1)

def same(input):
    return input.copy()

# ----------------------------------------------------------------------------------------------------------------------
# IGNORE EXPRESSIONS (used for defer events in non-deferral mode)

def expr_ignore(parser, input, how, extra_info):
    return input.copy()

# ----------------------------------------------------------------------------------------------------------------------
# OCTAVES

def expr_octave_up(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    res = input.transpose(octaves=how)
    return res

def expr_octave_down(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    res = input.transpose(octaves=-how)
    return res

def expr_octave_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    res = input.with_octave(how)
    return res

# ----------------------------------------------------------------------------------------------------------------------
# SCALE NOTES

def expr_scale_note_up(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.scale_transpose(parser.scale, how)


def expr_scale_note_down(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.scale_transpose(parser.scale, -how)

# ----------------------------------------------------------------------------------------------------------------------
# SCALE DEGREES

def expr_degree_up(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.transpose(degrees=how)

def expr_degree_down(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.transpose(degrees=-how)

# ----------------------------------------------------------------------------------------------------------------------
# VELOCITY

def expr_velocity_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.with_velocity(how)

# ----------------------------------------------------------------------------------------------------------------------
# CCs

def expr_cc_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.with_cc(extra_info, how)

# ----------------------------------------------------------------------------------------------------------------------
# VARIABLES

def expr_variable_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_string=True)
    set_variable(extra_info, how)
    return input

# ----------------------------------------------------------------------------------------------------------------------
# CHORDS

def expr_chord_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_string=True)
    return input.chordify(how)

# ----------------------------------------------------------------------------------------------------------------------
# INTRA-TRACK EVENTS

def expr_track_grab(parser, input, how, extra_info):

    how = evaluate_params(how, want_string=True)
    playing = get_first_playing_note(how)
    if playing is not None:
        input = input.copy()
        input.octave = playing.octave
        input.name = playing.name
        #assert input.start_time is not None
        #assert input.end_time is not None
    return input

# ----------------------------------------------------------------------------------------------------------------------    
# PROBABILITY    

def expr_probability_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_string=True)
    how = float(how)
    rn = random.random()

    # example: p=0.1
    #
    # event should only happen in 1 in 10 times
    # random number chosen is 0.9
    # rn is higher than the threshold
    # the event should NOT happen
    #
    # random number chosen is 0.02
    # rn is LOWER than the threshold
    # the event should happen

    if rn > how:
        parser.execute_next = False
    return input

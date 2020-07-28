from . mod_util import *
from .. model.registers import get_first_playing_note

# ----------------------------------------------------------------------------------------------------------------------
# SPECIAL (these do not take parameters)

def silence(input):
    return None

def sharp(input):
    return input.transpose(semitones=1)

def flat(input):
    return input.transpose(semitones=-1)

# ----------------------------------------------------------------------------------------------------------------------
# IGNORE EXPRESSIONS (used for defer events in non-deferral mode)

def expr_ignore(parser, input, how, extra_info):
    return input

# ----------------------------------------------------------------------------------------------------------------------
# OCTAVES

def expr_octave_up(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.transpose(octaves=how)

def expr_octave_down(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    #print("-how=%s" % -how)
    #print(type(how))
    #print(type(input))
    return input.transpose(octaves=-how)

def expr_octave_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.with_octave(how)

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

def expr_velocity_up(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.adjust_velocity(how)

def expr_velocity_down(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.adjust_velocity(-how)

def expr_velocity_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.with_velocity(how)

# ----------------------------------------------------------------------------------------------------------------------
# CCs

# FIXME: do we want to support this?
def expr_cc_up(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.adjust_cc(extra_info, how)

# FIXME: do we want to support this?
def expr_cc_down(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.adjust_cc(extra_info, -how)

def expr_cc_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    return input.with_cc(extra_info, how)

# ----------------------------------------------------------------------------------------------------------------------
# VARIABLES

# FIXME: do we want to support this?
def expr_variable_up(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    set_variable(extra_info, get_variable(extra_info) + how)
    return input

# FIXME: do we want to support this?
def expr_variable_down(parser, input, how, extra_info):
    how = evaluate_params(how, want_int=True)
    set_variable(extra_info, get_variable(extra_info) - how)
    return input

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

    # note grab: T=euro1
    how = evaluate_params(how, want_string=True)
    playing = get_first_playing_note(how)
    if playing is None:
        pass
    else:
        input = input.copy()
        input.octave = playing.octave
        input.name = playing.name
    return input

# ----------------------------------------------------------------------------------------------------------------------    
# PROBABILITY    

def expr_probability_set(parser, input, how, extra_info):
    how = evaluate_params(how, want_string=True)
    how = float(how)
    rn = random.random()
    if rn < how:
        parser.execute_next = False
    else:
        pass
    return input
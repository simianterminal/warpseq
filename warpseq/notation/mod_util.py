import random

VARIABLES = dict()

def is_choice(how):
    return "," in how

def is_range(how):
    return ":" in how

def pick_choice(how):
    tokens = how.split(",")
    choices = []
    for t in tokens:
        if is_variable(t):
            choices.append(_get_variable(t))
        else:
            choices.append(t)
    return random.choice(choices)

def pick_range(how):
    bounds = how.split(":",1)
    left = bounds[0]
    right = bounds[1]
    if is_variable(left):
        left = get_variable(left)
    if is_variable(right):
        right = get_variable(right)
    left = int(left)
    right = int(right)
    rc = random.randrange(left, right)
    return rc

def evaluate_params(how, want_int=False, want_string=False):

    if is_choice(how):
        #print("C1")
        result = pick_choice(how)
    elif is_range(how):
        #print("R1")
        result = pick_range(how)
    else:
        #print("--")
        result = how


    if want_int:
        result = int(result)
    if want_string:
        result = str(result)
    return result

def is_variable(what):
    return what.startswith("$")

def get_variable(what, value):
    return what.replace("$","")

def set_variable(what, value):
    global VARIABLES
    VARIABLES[what] = value

def increment_variable(what, value):
    global VARIABLES
    VARIABLES[what] = VARIABLES[what] + value

def decrement_variable(what, value):
    global VARIABLES
    VARIABLES[what] = VARIABLES[what] - value
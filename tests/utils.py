# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from warpseq.utils.utils import roll_left, roll_right, roller

def test_roll_left():
    assert roll_left([1,2,3,4,5]) == [2,3,4,5,1]

def test_roll_right():
    assert roll_right([1,2,3,4,5]) == [5,1,2,3,4]

def test_roller():

    alist = [ 1, 2, 3 ]

    generator = roller(alist)

    assert next(generator) == 1
    assert next(generator) == 2
    assert next(generator) == 3
    assert next(generator) == 1

    generator = roller(alist)

    assert next(generator) == 1
    assert next(generator) == 2


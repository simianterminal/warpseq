# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a Pattern is a list of symbols/expressions that will eventually
# evaluate into Chords/Notes.

from classforge import Class, Field

from .base import NewReferenceObject
from .scale import Scale
from .transform import Transform

FORWARD='forward'
REVERSE='reverse'

DIRECTIONS = [
    FORWARD,
    REVERSE
]

class Pattern(NewReferenceObject):

    __slots__ = [ 'name', 'slots', 'octave_shift', 'rate', 'scale', 'obj_id' ]

    def __init__(self, name=None, slots=None, octave_shift=0, rate=1, scale=None, obj_id=None):

        self.name = name
        self.slots = slots
        self.octave_shift = octave_shift
        self.rate = rate
        self.scale = scale
        self.obj_id = obj_id

        super(Pattern, self).__init__()

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            slots = self.slots,
            octave_shift = self.octave_shift,
            rate = self.rate
        )
        if self.scale:
            result['scale'] = self.obj_id
        else:
            result['scale'] = None
        return result

    @classmethod
    def from_dict(cls, song, data):
        return Pattern(
            obj_id = data['obj_id'],
            name = data['name'],
            slots = data['slots'],
            octave_shift = data['octave_shift'],
            rate = data['rate'],
            scale = song.find_scale(data['scale'])
        )

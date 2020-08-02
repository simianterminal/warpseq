# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# logic behind scale math, allowing for computing of intervals within
# a scale.

from .base import NewReferenceObject
from .note import Note, note
import functools

SCALE_TYPES = dict(
   major              = [ 1, 2, 3, 4, 5, 6, 7 ],
   pentatonic         = [ 1, 2, 3, 5, 6 ],
   natural_minor      = [ 1, 2, 'b3', 4, 5, 'b6', 'b7' ],
   blues              = [ 1, 'b3', 4, 'b5', 5, 'b7' ],
   dorian             = [ 1, 2, 'b3', 4, 5, 6, 'b7' ],
   chromatic          = [ 1, 'b2', 2, 'b3', 3, 4, 'b5', 5, 'b6', 6, 'b7', 7 ],
   harmonic_major     = [ 1, 2, 3, 4, 5, 'b6', 7 ],
   harmonic_minor     = [ 1, 2, 3, 4, 5, 'b6', 7 ],
   locrian            = [ 1, 'b2', 'b3', 4, 'b5', 'b6', 'b7' ],
   lydian             = [ 1, 2, 3, 'b5', 5, 6, 7 ],
   major_pentatonic   = [ 1, 2, 3, 5, 6 ],
   melodic_minor_asc  = [ 1, 2, 'b3', 4, 5, 'b7', 'b8', 8 ],
   melodic_minor_desc = [ 1, 2, 'b3', 4, 5, 'b6', 'b7', 8 ],
   minor_pentatonic   = [ 1, 'b3', 4, 5, 'b7' ],
   mixolydian         = [ 1, 2, 3, 4, 5, 6, 'b7' ],
   phyrigian          = [ 1, 'b2', 'b3', 4, 5, 'b6', 'b7' ],
   akebono            = [ 1, 2, 'b3', 5, 6 ]
)

SCALE_TYPE_NAMES = [ k for k in SCALE_TYPES.keys() ]
SCALE_TYPE_NAMES.append(None)

SCALE_ALIASES = dict(
   aeolian = 'natural_minor',
   ionian = 'major',
   minor = 'natural_minor'
)

def scale_types():
    values = [ x for x in SCALE_TYPES.keys() ]
    return values

class Scale(NewReferenceObject):

    from . note import Note

    __SLOTS__ = ['name', 'root', 'scale_type', 'slots', '_cached', 'obj_id']

    #name = Field(type=str, required=False, nullable=False)
    #root = Field(type=Note, required=False, nullable=True)
    #scale_type = Field(type=str, required=False, nullable=True, default=None, choices=SCALE_TYPE_NAMES)
    #slots = Field(type=list, required=False, nullable=True, default=None)
    #_cached = Field(type=list, required=False)

    def __init__(self, name=None, root=None, scale_type=None, slots=None, obj_id=None):
        self.name = name
        self.root = root
        self.scale_type = scale_type
        self.slots = slots
        self.obj_id = obj_id
        self._cached = None
        super(Scale, self).__init__()
        self.generate(length=140)

    def to_dict(self):
        data = dict(
            obj_id = self.obj_id,
            name = self.name,
            scale_type = self.scale_type,
            slots = self.slots
        )
        if self.root:
            data["root"] = [ self.root.name, self.root.octave ]
        else:
            data["root"] = None
        return data

    @classmethod
    def from_dict(cls, song, data):
        s = Scale(
            obj_id = data['obj_id'],
            name = data['name'],
            scale_type = data['scale_type'],
            slots = data['slots']
        )
        if data['root']:
            s.root = Note(name=data['root'][0], octave=data['root'][1])
        return s

    # FIXME: remove the length param
    @functools.lru_cache(maxsize=5)
    def generate(self, length=None):

        if self._cached is None:
            self._generate(length=145)
        else:
            #return [ r.copy() for r in self._cached ]
            return self._cached

        index = 0

        result = []
        while (index < length):
            try:
                result.append(self._cached[index])
            except IndexError:
                return result
            index = index + 1

        return result

    def _generate(self, length=None):
        """
        Allows traversal of a scale in a forward direction.
        Example:
        for note in scale.generate(length=7):
           print(note)
        """


        assert length is not None

        scale_data = self.slots

        if not scale_data:
            scale_type = SCALE_ALIASES.get(self.scale_type, self.scale_type)
            scale_data = SCALE_TYPES[scale_type][:]

        octave_shift = 0
        index = 0

        self._cached = []

        while (length is None or length > 0):

            if index == len(scale_data):
               index = 0
               octave_shift = octave_shift + 1

            try:
                result = self.root.transpose(degrees=scale_data[index], octaves=octave_shift)
            except IndexError:
                return

            self._cached.append(result)

            index = index + 1
            if length is not None:
                length = length - 1

def scale(input):
    """
    Shortcut: scale(['C major') -> Scale object
    """
    (root, scale_type) = input.split()
    return Scale(root=note(root), scale_type=scale_type)

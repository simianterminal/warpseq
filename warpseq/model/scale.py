from . base import ReferenceObject
from classforge import Class, Field
from . note import Note, note

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
   lydian             = [ 1, 2, 3, 'b4', 5, 6, 7 ],
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

class Scale(ReferenceObject):

    from . note import Note

    name = Field(type=str, required=False, nullable=False)
    root = Field(type=Note, required=True, nullable=False)
    scale_type = Field(type=str, required=False, nullable=True, default=None, choices=SCALE_TYPE_NAMES)
    slots = Field(type=list, required=False, nullable=True, default=None)

    # slots = Field(type=list, required=True, nullable=False)

    def to_dict(self):
        return dict(
            obj_id = self.obj_id,
            name = self.name,
            root = [ self.root.name, self.root.octave ],
            scale_type = self.scale_type,
            slots = self.slots
        )

    @classmethod
    def from_dict(cls, song, data):
        return Scale(
            obj_id = data['obj_id'],
            name = data['name'],
            root = Note(name=data['root'][0], octave=data['root'][1]),
            scale_type = data['scale_type'],
            slots = data['slots']
        )


    def generate(self, length=None):
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
        while (length is None or length > 0):

            if index == len(scale_data):
               index = 0
               octave_shift = octave_shift + 1
            result = self.root.transpose(degrees=scale_data[index], octaves=octave_shift)
            yield(result)
            index = index + 1
            if length is not None:
                length = length - 1

    #def __eq__(self, other):
    #    """
    #    Scales are equal if they are the ... same scale
    #    """
    #    if other is None:
    #        return False
    #    return self.root == other.root and self.scale_type == other.scale_type

    #def short_name(self):
    #    return "%s %s" % (self.root.short_name(), self.scale_type)

    #def __repr__(self):
    #    return "Scale<%s>" % self.short_name()

def scale(input):
    """
    Shortcut: scale(['C major') -> Scale object
    """
    (root, scale_type) = input.split()
    return Scale(root=note(root), scale_type=scale_type)
from .base import BaseObject
from classforge import Class, Field
from .scale import Scale
from .arp import Arp

FORWARD='forward'
REVERSE='reverse'

DIRECTIONS = [
    FORWARD,
    REVERSE
]

class Pattern(BaseObject):

    track = Field(required=True, nullable=False)
    events = Field(type=list, default=[], required=True)


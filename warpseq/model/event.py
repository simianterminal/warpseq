import copy
from classforge import Field
from .base import BaseObject

NOTE_ON = 1
NOTE_OFF = 0

class Event(BaseObject):

    from . note import Note

    type = Field(type=int, required=True, choices=[NOTE_ON, NOTE_OFF])
    note = Field(type=Note, required=True, nullable=False)
    time = Field(type=float, required=True, nullable=False)

    # TODO: add velocity to note
    # TODO: CC flags as dict?
    # TODO: grab channel from *TRACK*

    def __repr__(self):
        return "Event<Note=%s, type=%s, time=%s>" % (self.note, self.type, self.time)
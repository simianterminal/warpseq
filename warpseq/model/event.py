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
    on_event = Field(required=False, default=None, nullable=True)

    def __repr__(self):
        return "Event<Note=%s, type=%s, time=%s>" % (self.note, self.type, self.time)

    def copy(self):
        return Event(
            type = self.type,
            note = self.note.copy(), # could be a Chord!  Be careful.
            time = self.time,
            on_event = self.on_event,
        )
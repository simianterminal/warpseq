# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# an event represents starting or stopping a note, and some associated
# data so the program can handle the note and other processing in context.
# for instance the scale is needed for processing deferred events.

import copy

from classforge import Field

from .base import BaseObject

NOTE_ON = 1
NOTE_OFF = 0

class Event(object):


    __slots__ = [ 'type', 'note', 'time', 'on_event', 'scale' ]

    from . note import Note

    #type = Field(type=int, required=True, choices=[NOTE_ON, NOTE_OFF])
    #note = Field(type=Note, required=True, nullable=False)
    #time = Field(type=float, required=True, nullable=False)
    #on_event = Field(required=False, default=None, nullable=True)
    #scale = Field(required=False, default=None)

    def __init__(self, type=None, note=None, time=None, on_event=None, scale=None):
        self.type = type
        self.note = note
        self.time = time
        self.on_event = on_event
        self.scale = scale

    def __repr__(self):
        return "Event<Note=%s, type=%s, time=%s>" % (self.note, self.type, self.time)

    def copy(self):
        return Event(
            type = self.type,
            note = self.note.copy(), # could be a Chord!  Be careful.
            time = self.time,
            on_event = self.on_event,
        )

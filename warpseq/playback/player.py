from .. model.base import BaseObject
from classforge import Field
from .. model.event import Event, NOTE_ON, NOTE_OFF

TIME_INTERVAL = 10


# FIXME: this whole player logic might be rather off and will need some debugging

class Player(BaseObject):

    # input
    events = Field(type=list, required=True, nullable=False)
    clip_length_in_ms = Field(type=int, required=True, nullable=False)
    engine = Field(required=True, nullable=False)

    # state
    left_to_play = Field(type=list, nullable=False)
    time_index = Field(type=int, default=0, nullable=False)

    def on_init(self):

        self.start()

    def queue_size(self):
        return len(self.left_to_play)

    def advance(self, milliseconds=TIME_INTERVAL):

        #print("TIME INDEX=%s, REMAINING_QUEUE_SIZE=%s" % (self.time_index, len(self.left_to_play)))



        self.time_index += milliseconds

        self.engine.note_time_index(self.time_index)
        self.engine.note_advance(milliseconds)

        while True:

            if len(self.left_to_play):
                first = self.left_to_play[-1]

                #print("FT=%s" % first.time)

                if first.time < self.time_index:
                    #print("t1=%s < t2=%s" % (first.time, self.time_index))

                    self.engine.play(first)
                    discard = self.left_to_play.pop()
                    #print("DISCARDED 1: %s" % discard)
                else:
                    break
            else:
                break

        if self.time_index >= self.clip_length_in_ms:
            self.start()


    def stop(self):

        # make sure we play all the stop events
        for event in self.left_to_play:
            if event.type == NOTE_OFF:
                self.engine.play(event)
        self.left_to_play = []


    def start(self):

        if self.left_to_play is not None:
            self.stop()

        self.time_index = 0

        self.left_to_play = [ n for n in self.events ]
        self.left_to_play.reverse()



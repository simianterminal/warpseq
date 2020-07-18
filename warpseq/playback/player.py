from .. model.base import BaseObject
from classforge import Field

TIME_INTERVAL = 10

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

    def advance(self, milliseconds=TIME_INTERVAL):

        self.time_index += milliseconds

        while True:

            if len(self.left_to_play):
                first = self.left_to_play[-1]
                if first.time < self.time_index:
                    self.engine.play(first)
                    self.left_to_play.pop()
                else:
                    break
            else:
                break


    def stop(self):

        # make sure we play all the stop events
        for event in self.left_to_play:
            if event.type == Event.NOTE_OFF:
                self.engine.play(x)


    def start(self):

        if self.left_to_play is not None:
            self.stop()

        self.time_index = 0

        self.left_to_play = [ n for n in self.events ]
        self.left_to_play.reverse()



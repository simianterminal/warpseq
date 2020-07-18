from classforge import Field

from warpseq.model.base import BaseObject

TIME_INTERVAL = 10

class LogEngine(BaseObject):

    from ... model.song import Song
    from ... model.track import Track

    # input
    song = Field(type=Song,  required=True, nullable=False)
    track = Field(type=Track, required=True, nullable=False)

    # informational/state
    time_index = Field(type=int)

    def on_init(self):
        self.time_index = 0
        pass

    def play(self, event):
        print("player plays event (%s) on track (%s) at time index (%s)" % (event, self.track.name, self.time_index))

    def note_advance(self, milliseconds):
        #print("player notes advance of (%s) for track (%s)" % (milliseconds, self.track.name))
        pass

    def note_time_index(self, time_index):
        self.time_index = time_index
        #print("player notes time index of (%s) for track (%s)" % (time_index, self.track.name))

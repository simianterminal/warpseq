from classforge import Field

from warpseq.model.base import BaseObject

TIME_INTERVAL = 10

class LogEngine(BaseObject):

    from ... model.song import Song
    from ... model.track import Track

    song = Field(type=Song,  required=True, nullable=False)
    track = Field(type=Track, required=True, nullable=False)

    def on_init(self):
        pass

    def play(self, event):
        print(event)
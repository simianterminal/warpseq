# TODO?

from .. model.base import BaseObject
from classforge import Field
from . player import TIME_INTERVAL
import time
import ctypes

#libc = ctypes.CDLL('libc.so.6')


# FIXME: any higher level code that allows renaming of a clip will have to call remove_clip and then add_clip
# or this implementation will get confused when trying to stop that clip.

class MultiPlayer(BaseObject):

    # input
    song = Field()
    engine_class = Field()

    # state
    clips = Field(type=list)
    players = Field(type=dict)

    def on_init(self):
        self.clips = []
        self.players = {}


    #def start(self, milliseconds=TIME_INTERVAL):
    #    for (n, p) in self.players.items():
    #        p.start()
    #        p.advance(milliseconds=milliseconds)

    def stop(self):
        for (n, p) in self.players.items():
            p.stop()

            assert p.queue_size() == 0
        self.clips = []
        self.players = {}

    def advance(self, milliseconds=TIME_INTERVAL):

        my_players = [ p for p in self.players.values() ]

        if len(my_players) == 0:
            return

        for p in my_players:
            p.advance(milliseconds=milliseconds)

        x = time.perf_counter() + (milliseconds/1000.0)
        while time.perf_counter() < x:
            pass

    def play_scene(self, scene):

        self.stop()

        clips = scene.clips(self.song)
        for c in clips:
            self.add_clip(c)


    def add_clip(self, clip):

        #print("playing clip: %s" % clip.name)

        # starts a clip playing, including stopping any already on the same track

        assert clip.track is not None

        need_to_stop = [ c for c in self.clips if clip.track.obj_id == c.track.obj_id ]
        for c in need_to_stop:
            self.remove_clip(c)

        matched = [ c for c in self.clips if c.name == clip.name ]
        if not len(matched):
            self.clips.append(clip)

            player = clip.get_player(self.song, self.engine_class)
            self.players[clip.name] = player

            player._multiplayer = self
            player.start()

    def remove_clip(self, clip):

        # stops a playing clip

        if clip.name not in self.players:
            return

        player = self.players[clip.name]
        player.stop()

        # it's possible this was already removed?
        del self.players[clip.name]

        self.clips = [ c for c in self.clips if c.name != clip.name ]


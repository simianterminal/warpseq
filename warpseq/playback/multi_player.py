# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

from .. model.base import BaseObject
from classforge import Field
from . player import TIME_INTERVAL
import time
import ctypes

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

        # starts a clip playing, including stopping any already on the same track
        # FIXME: move this into the callbacks system (among other events)
        print("playing clip: %s" % clip.name)
        clip.reset()
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
        if clip.name not in self.players:
            # clip was already removed/stopped ?
            return
        player = self.players[clip.name]
        player.stop()
        del self.players[clip.name]
        self.clips = [ c for c in self.clips if c.name != clip.name ]


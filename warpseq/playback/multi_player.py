# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# the multi-player class contains high level methods for playing
# clips and scenes, as such the individual (track-specific) interface,
# player.py, is a less public API than this one.

import ctypes
import time

from ..api.callbacks import Callbacks
from ..api.exceptions import AllClipsDone
from ..model.base import BaseObject
from .player import TIME_INTERVAL
import time


class MultiPlayer(object):

    __slots__ = [ 'song', 'engine_class', 'clips', 'players', 'callbacks', 'stop_if_empty' ]

    def __init__(self, song=None, engine_class=None):
        self.song = song
        self.engine_class = engine_class

        self.clips = []
        self.players = {}
        self.callbacks = Callbacks()

    def stop(self):
        """
        Stops all clips.
        """

        # stop all players that are attached
        for (n, p) in self.players.items():
            p.stop()
            #assert p.queue_size() == 0

        # clear the list of things that are playing, in case we start more
        self.clips = []
        self.players = {}

    def advance(self, milliseconds=TIME_INTERVAL):

        """
        return all events from now to TIME_INTERVAL and then move the time index up by that amount.
        the multiplayer doesn't keep track of the time indexes themselves, the clips do, and they may
        all run at different speeds.
        """

        my_players = [ p for p in self.players.values() ]

        for p in my_players:
            p.advance(milliseconds=milliseconds)

        # time.sleep is unreliable - so we burn clock instead, giving us much nicer timing.
        x = time.perf_counter() + (milliseconds/1000.0)
        while time.perf_counter() < x:
            time.sleep(0.00005)
            pass

    def play_scene(self, scene):
        """
        Plays all clips in a scene, first stopping all clips that might be playing elsewhere.
        """
        self.stop()
        self.callbacks.on_scene_start(scene)
        clips = scene.clips(self.song)
        self.add_clips(clips)

    def add_clips(self, clips):
        """
        Adds a clip to be playing by creating a Player for it.
        """

        for clip in clips:

            # starts a clip playing, including stopping any already on the same track
            self.callbacks.on_clip_start(clip)

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

        for (k,v) in self.players.items():
            v.start()

    def remove_clip(self, clip, add_pending=False):
        """
        Stops a clip and removes the player for it.
        """

        self.callbacks.on_clip_stop(clip)
        if clip.name not in self.players:
            # clip was already removed/stopped ?
            return
        player = self.players[clip.name]
        player.stop()
        del self.players[clip.name]
        self.clips = [ c for c in self.clips if c.name != clip.name ]

        if not add_pending and len(self.clips) == 0 and self.stop_if_empty:
            # TODO: add callback?
            #print("-- all clips done --")
            time.sleep(0.5)
            raise AllClipsDone()

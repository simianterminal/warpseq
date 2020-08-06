# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# this class contains play-head logic to support processing events
# into MIDI notes. This class isn't meant to be used directly,
# use Multiplayer as shown in api/public.py instead.

# FAIR WARNING: this code has some larger functions because it is trying to be more efficient

from ..api.callbacks import Callbacks
from ..api.exceptions import *
from ..model.event import NOTE_OFF, NOTE_ON, Event
import time
from .. notation.time_stream import NOTE_GAP

def event_sorter(evt):
    return evt.time

class Player(object):

    __slots__ = [ 'clip', 'song', 'engine', 'left_to_play', 'time_index', 'repeat_count', 'clip_length_in_ms', 'events', '_multiplayer', 'callbacks' ]


    def __init__(self, clip=None, song=None, engine=None):
        """
        When we start a player we ask clips for all the events between a start
        time and a hypothethical start time. The player class can then walk through
        them in steps.
        """

        self.clip = clip
        self.song = song
        self.engine = engine
        self.time_index = 0
        self.left_to_play = None
        self.clip_length_in_ms = self.clip.get_clip_duration(self.song)
        self.events = self.clip.get_events(self.song)
        self.repeat_count = self.clip.repeat
        self.callbacks = Callbacks()
        self.start()

    def inject_off_event(self, event):
        self.left_to_play.append(Event(
            type = NOTE_OFF,
            off_event = None,
            on_event = event,
            time = event.time + event.note.length - NOTE_GAP,
            note = event.note.copy()
        ))
        print("OFF=>%s" % (event.time + event.note.length - NOTE_GAP))

    def _still_on_this_clip(self):
        """
        We are due to still be playing this clip if the clip has infinite repeats
        or the repeats are expired.
        """
        if self.clip.repeat is None:
            return True
        self.repeat_count = self.repeat_count - 1
        if self.repeat_count <= 0:
            return False
        return True

    def advance(self, milliseconds):
        """
        Advances the playhead a number of milliseconds and plays all the notes
        between those two points.
        """

        self.time_index += milliseconds
        ti = self.time_index
        ltp = self.left_to_play

        # consume any events we need to off the time queue
        if len(self.left_to_play):

            due = [ x for x in ltp if x.time < ti ]

            if len(due):
                due = sorted(due, key=event_sorter)
                #print("DUE: %s" % due)
                for x in due:
                    self.engine.play(x)
                self.left_to_play = [ x for x in ltp if x not in due ]


        if self.time_index >= self.clip_length_in_ms:


            # the play-head has advanced beyond the end of the clip

            if self._still_on_this_clip():
                # the clip is due to repeat again...
                self.callbacks.on_clip_restart(self.clip)
                # recompute events so randomness can change
                self.events = self.clip.get_events(self.song)
                self.start()
            else:
                # the clip isn't due to repeat again, make sure we have played any note off events
                # before removing it

                self.stop()

                if self.clip.auto_scene_advance:

                    # see if the clip says to go play a new scene
                    new_scene = self.song.next_scene(self.clip.scene)
                    if new_scene:
                        self._multiplayer.remove_clip(self.clip, add_pending=True)

                        new_clips = new_scene.clips(self.song)
                        if (len(new_clips) == 0) and self._multiplayer.stop_if_empty:
                            raise AllClipsDone()

                        self._multiplayer.play_scene(new_scene)
                        return

                if self.clip.next_clip is not None:

                    new_clip = self.song.find_clip_by_name(self.clip.next_clip)
                    self._multiplayer.remove_clip(self.clip, add_pending=True)
                    self._multiplayer.add_clips([new_clip])
                    return

                self._multiplayer.remove_clip(self.clip)

    def stop(self):
        """
        Stop this clip/player making sure to send any midi off events
        """

        for event in self.left_to_play:
            if event.type == NOTE_OFF:
                self.engine.play(event)
        self.left_to_play = []

    def start(self):
        """
        Stop the clip if already playing, then configure the play head to read from the start of the clip.
        This isn't a directly usable API, use MultiPlayer instead.
        """

        if self.left_to_play is not None:
            self.stop()
        self.time_index = 0
        self.left_to_play = [ n for n in self.events ]
        self.left_to_play.reverse()

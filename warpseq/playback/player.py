from .. model.base import BaseObject
from classforge import Field
from .. model.event import Event, NOTE_ON, NOTE_OFF

TIME_INTERVAL = 10


# FIXME: this whole player logic might be rather off and will need some debugging

class Player(BaseObject):

    # input
    clip   = Field(required=True, nullable=False)
    song   = Field(required=True, nullable=False)
    engine = Field(required=False, nullable=False)

    # state
    left_to_play = Field(type=list, nullable=False)
    time_index = Field(type=int, default=0, nullable=False)
    repeat_count = Field(type=int, default=0, nullable=True)

    # calculated
    clip_length_in_ms = Field(type=int, required=False, nullable=False)
    events = Field(type=list, required=False, nullable=False)
    _multiplayer = Field()

    def on_init(self):

        self.clip_length_in_ms = self.clip.get_clip_duration(self.song)
        self.events = self.clip.get_events(self.song)
        self.repeat_count = self.clip.repeat
        self.start()

    def queue_size(self):
        return len(self.left_to_play)

    def _still_on_this_clip(self):

        if self.clip.repeat is None:
            print("this clip (%s) is set to infinite repeat" % (self.clip.name))
            return True
        self.repeat_count = self.repeat_count - 1
        if self.repeat_count <= 0:
            return False
        print("this clip still has repeats left (%s=%s)" % (self.clip.name, self.repeat_count))
        return True


    def advance(self, milliseconds=TIME_INTERVAL):

        #print("TIME INDEX=%s, REMAINING_QUEUE_SIZE=%s" % (self.time_index, len(self.left_to_play)))



        self.time_index += milliseconds

        self.engine.note_time_index(self.time_index)
        self.engine.note_advance(milliseconds)

        while True:

            # consume any events we need to off the time queue

            if len(self.left_to_play):
                first = self.left_to_play[-1]

                #print("FT=%s" % first.time)

                if first.time < self.time_index:
                    #print("t1=%s < t2=%s" % (first.time, self.time_index))

                    self.engine.play(first)
                    discard = self.left_to_play.pop()
                    #print("DISCARDED 1: %s" % discard)
                else:
                    # we aren't ready to play this yet
                    break
            else:
                break

        if self.time_index >= self.clip_length_in_ms:
            #print("time=%s >= %s" % (self.time_index, self.clip_length_in_ms))
            if self._still_on_this_clip():
                #print("it is decided to stay on this clip (%s)" % (self.clip.name))
                # recompute events so randomness can change
                self.events = self.clip.get_events(self.song)
                self.start()

            else:
                #print("it is decided to stop this clip (%s)" % (self.clip.name))
                self.stop()
                print("ended clip: %s" % self.clip.name)
                self._multiplayer.remove_clip(self.clip)

                if self.clip.auto_scene_advance:
                    new_scene = self.song.next_scene(self.clip.scene)
                    print("scene advance to: %s" % new_scene)
                    self._multiplayer.play_scene(new_scene)

                elif self.clip.next_clip is not None:
                    print("clip advance: %s" % self.clip.next_clip)
                    #print("Adding a new clip (%s) after (%s)" % (self.clip.next_clip, self.clip.name))
                    new_clip = self.song.find_clip_by_name(self.clip.next_clip)
                    self._multiplayer.add_clip(new_clip)


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



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
            return True
        self.repeat_count = self.repeat_count - 1
        if self.repeat_count <= 0:
            return False
        return True


    # TODO: we might want to consider a callback type API to send events when clips start and stop playing

    def advance(self, milliseconds=TIME_INTERVAL):

        self.time_index += milliseconds
        self.engine.note_time_index(self.time_index)

        while True:

            # consume any events we need to off the time queue
            if len(self.left_to_play):
                first = self.left_to_play[-1]
                if first.time < self.time_index:
                    self.engine.play(first)
                    discard = self.left_to_play.pop()
                else:
                    # we aren't ready to play this yet
                    break
            else:
                break

        if self.time_index >= self.clip_length_in_ms:
            if self._still_on_this_clip():
                # recompute events so randomness can change
                self.events = self.clip.get_events(self.song)
                self.start()

            else:
                self.stop()
                self._multiplayer.remove_clip(self.clip)

                if self.clip.auto_scene_advance:
                    new_scene = self.song.next_scene(self.clip.scene)
                    if new_scene:
                        print("auto advancing scene to: %s" % new_scene.name)
                        self._multiplayer.play_scene(new_scene)
                    else:
                        print("no scene to advance to")

                elif self.clip.next_clip is not None:
                    new_clip = self.song.find_clip_by_name(self.clip.next_clip)
                    print("auto advancing clip to: %s" % new_clip.name)
                    self._multiplayer.add_clip(new_clip)


    def stop(self):
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



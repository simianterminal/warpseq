# get all the playing clips
# have a method .add_playing_clip() that also resets the clip
# have a method .stop_playing_clip()

# on each clip, get the processed notes stream which looks like
#   [ note w/ length, note w/ length, note w/length ]
#   [ note w/ length ]

# base start time is time_index + 0
# if the note is in slot 1, 2, 3, 4 this adds in 0 * note_width
# use SmartExpression

def get_slot_duration(self):
    tempo = self.clip.get_effective_tempo(self.song)
    quarter_notes_per_second = tempo / 60
    sixteenth_note_speed = quarter_notes_per_second * (1 / 4)
    slot_length = clip.slot_length
    slot_duration = (slot_length / 16) * sixteenth_note_speed
    return slot_duration


# the stop time for each note, which we CAN record on the note is this start time
# plus the stop time

# each clip has this width, if the width but the ".conduct()" beat is shorter than this

# if we call .stop_playing_clip() we stop all playing notes that have been started
# we have a list of notes that have been started and not stopped
# this is done by checking for any notes with the same track + note + device

class Event(BaseObject):

    notes = Field(type=list)
    off = Field(type=bool)

class RealtimeEngine(BaseObject):

    time_index = Field(type=float)
    event_queue = Field(type=list)

    def enqueue_events(self, events):
        # enqueue events_to_stop at time_index + note_length
        pass

    def panic(self):
        # stop all the notes in events_to_stop
        pass

    def play_due_events(self, time_index):

        # this not only plays the events that are before the time index but it also
        # adds their stop versions as enqueued also

        # FIXME: the first version just prints


class Pipeline(BaseObject):

    song = Field()
    active_clips = Field(type=list)
    realtime_player = Field(type=list)

    def change_song(self, song):
        self.realtime_player.panic()
        self.active_clips = []
        self.song = song

    # we need some way to change objects by dicts??

    def get_generators_for_active_clips(self):
        pass

    def set_clip_active(self, clip):
        # also unsets any clips on the current track
        pass

    def unset_clip_active(self, clip):
        pass

    def panic_clips(self):
        # clear active clip events
        pass


    def run(self):

        generators_for_active_clips = []

        try:

            while True:

                time_index = 0

                for g in generators():

                    events = g.tick(SMALL_INCREMENT)
                    self.realtime_player.time_index = time_index
                    self.realtime_player.enqueue_events(events)
                    self.sleep(SMALL_INCREMENT)

                time_index = time_index + SMALL_INCREMENT

        except SystemInterruptExceptionWhatever:

            self.realtime_player.panic()


# usage:

pipeline = Pipeline(song=song, active_clips=[], realtime_player=RealtimePlayer())
pipeline.run()

# pipeline needs a method to change the song?
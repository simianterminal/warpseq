from .base import ReferenceObject
from .pattern import Pattern
from classforge import Class, Field
from .arp import Arp
from .scale import Scale
from ..notation.smart import SmartExpression
from ..notation.time_stream import evaluate_ties, notes_to_events
from ..playback.player import Player

class Clip(ReferenceObject):

    from . track import Track
    from . scene import Scene

    name = Field(type=str, required=True, nullable=False)

    scale = Field(type=Scale, required=False, nullable=True, default=None)

    pattern = Field(type=Pattern, required=False, default=None, nullable=True)

    # number of notes before repeat/loop
    length = Field(type=int, default=16, required=False, nullable=False)

    slot_length = Field(type=float, default=0.0625, required=False, nullable=False)

    arp = Field(type=Arp, default=None, nullable=True)
    tempo = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=-1, nullable=True)

    track = Field(type=Track, default=None, required=False, nullable=True)
    scene = Field(type=Scene, default=None, required=False, nullable=True)

    def scenes(self, song):
        return [ song.find_scene(x) for x in self.scene_ids ]

    def tracks(self, song):
        return [ song.find_track(x) for x in self.track_ids ]

    def to_dict(self):
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            length = self.length,
            tempo = self.tempo,
            repeat = self.repeat,
            slot_length = self.slot_length,
        )
        if self.pattern:
            result['pattern'] = self.pattern.obj_id
        else:
            result['pattern'] = None
        if self.arp:
            result['arp'] = self.arp.obj_id
        else:
            result['arp'] = None
        if self.scale:
            result['scale'] = self.scale.obj_id
        else:
            result['scale'] = None
        if self.track:
            result['track'] = self.track.obj_id
        else:
            result['track'] = None
        if self.scene:
            result['scene'] = self.scene.obj_id
        else:
            result['scene'] = None
        return result

    def copy(self):

        new_id = self.new_object_id()

        return Clip(
            obj_id = new_id,
            name = self.name,
            pattern = self.pattern,
            length = self.length,
            arp = self.arp,
            tempo = self.tempo,
            repeat = self.repeat,
            track_ids = [],
            scene_ids = [],
            slot_length = self.slot_length,

        )

    @classmethod
    def from_dict(cls, song, data):
        return Clip(
            obj_id = data['obj_id'],
            name = data['name'],
            scale = song.find_scale(data['scale']),
            pattern = song.find_pattern(data['pattern']),
            length = data['length'],
            arp = song.find_arp(data['arp']),
            tempo = data['tempo'],
            repeat = data['repeat'],
            track = song.find_track(data['track']),
            scene = song.find_scene(data['scene']),
            slot_length = data['slot_length']
        )

    def actual_scale(self, song):
        assert song is not None

        assert self.scene is not None, "clip scene must be defined"

        if self.scale:
            return self.scale
        if self.pattern and self.pattern.scale:
            return self.pattern.scale
        if self.scene.scale:
            return self.scene.scale
        if song.scale:
            return song.scale

        return Scale(root=Note(name="C", octave=0), scale_type='chromatic')

    def actual_arp(self, song):

        assert self.track is not None

        if self.arp is not None:
            return self.arp
        if self.pattern and self.pattern.arp:
            return arp
        return None

    def actual_tempo(self, song):

        if self.tempo is not None:
            return self.tempo
        if self.scene.tempo is not None:
            return self.scene.tempo
        if song.tempo is not None:
            return song.tempo

        raise Exception("?")

    def sixteenth_note_duration(self, song):

        tempo = float(self.actual_tempo(song))
        tempo_ratio = (120 / self.actual_tempo(song))
        snd = tempo_ratio * 125
        # print("SND=%s" % snd)
        return snd

    def slot_duration(self, song):

        # 1/16 note at 120 bpm is 125 ms

        # self.slot_length is the note size of each slot
        # self.length is the number of slots
        # the product is the number of whole notes in each clip

        #whole_notes = self.slot_length * self.length
        #print("WHOLE NOTES=%s" % whole_notes)

        snd = self.sixteenth_note_duration(song)
        slot_ratio = self.slot_length / (1/16.0)

        # print("SLOT RATIO = %s" % slot_ratio)

        slot_duration = snd * slot_ratio

        return slot_duration

    def get_clip_duration(self, song):
        return self.slot_duration(song) * self.length

    def get_notes(self, song):

        # how long is each slot in MS?
        sixteenth = self.sixteenth_note_duration(song)
        slot_duration = self.slot_duration(song)

        # print("SD milliseconds=%s" % slot_duration)


        scale = self.actual_scale(song)
        arp = self.actual_arp(song)

        assert scale is not None
        if self.pattern is None:
            return []

        slots = self.pattern.slots

        if not self.pattern:
            return []

        # convert expressions into arrays of notes
        notation = SmartExpression(scale=scale, song=song, clip=self, track=self.track)

        # expression evaluator will need to grow smarter for intra-track and humanizer fun
        # create a list of list of notes per step... ex: [ [ c4, e4, g4 ], [ c4 ] ]
        notes = [ notation.do(self, expression) for expression in slots ]

        # "-" means extend the previous note length
        notes = evaluate_ties(notes)


        # set the start and end times for each note


        # FIXME: it appears the notes aren't copies ... somewhere

        t_start = 0.0
        for slot in notes:
            for note in slot:
                note.start_time = round(t_start)
                note.end_time = round(t_start + note.length)
            t_start = t_start + slot_duration
            # print("t_start=%s" % t_start)


        if arp:
            notes = arp.process(song, scale, self.track, notes)

            #print("ARP RESULTS: %s" % notes)
        else:
            # print("NO ARP")
            pass

        # print("THE QUEUE=%s" % notes)

        return notes

    def get_events(self, song):
        notes = self.get_notes(song)
        events = notes_to_events(notes)
        return events

    def get_player(self, song, engine_class):

        events = self.get_events(song)
        t_len = self.get_clip_duration(song)
        scale = self.actual_scale(song)

        player = Player(
            events=events,
            engine=engine_class(song=song, track=self.track, scale=scale, clip=self),
            clip_length_in_ms=t_len,
        )

        return player



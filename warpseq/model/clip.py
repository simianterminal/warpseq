from .base import ReferenceObject
from .pattern import Pattern
from classforge import Class, Field
from .arp import Arp
from .scale import Scale
from ..notation.smart import SmartExpression
from ..notation.time_stream import evaluate_ties, evaluate_shifts, chord_list_to_notes, notes_to_events
from ..playback.player import Player
from .. utils import utils
import time

class Clip(ReferenceObject):

    from . track import Track
    from . scene import Scene

    name = Field(type=str, required=True, nullable=False)

    scales = Field(type=list, required=False, nullable=True, default=None)

    patterns = Field(type=list, required=True, nullable=False)

    # number of notes before repeat/loop
    length = Field(type=int, default=None, required=False, nullable=True)

    slot_length = Field(type=float, default=0.0625, required=False, nullable=False)
    octave_shifts = Field(type=list, default=None, required=False, nullable=True)
    degree_shifts = Field(type=list, default=None, required=False, nullable=True)

    next_clip = Field(required=False, nullable=True)

    arps = Field(type=list, default=None, nullable=False)
    tempo = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=-1, nullable=True)

    auto_scene_advance = Field(type=bool, default=False, nullable=False)

    track = Field(type=Track, default=None, required=False, nullable=True)
    scene = Field(type=Scene, default=None, required=False, nullable=True)

    def scenes(self, song):
        return [ song.find_scene(x) for x in self.scene_ids ]

    def tracks(self, song):
        return [ song.find_track(x) for x in self.track_ids ]

    def to_dict(self):

        print(self.name)
        #print("SCALES=%s" % self.scales)
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            length = self.length,
            tempo = self.tempo,
            repeat = self.repeat,
            slot_length = self.slot_length,
            next_clip = self.next_clip,
            auto_scene_advance = self.auto_scene_advance
        )
        if self.patterns:
            result['patterns'] = [ x.obj_id for x in self.patterns ]
        else:
            result['patterns'] = []
        if self.arps:
            #print("arps: %s" % self.arps)
            result['arps'] = [ x.obj_id for x in self.arps ]
        else:
            result['arps'] = []
        if self.scales:
            result['scales'] = [x.obj_id for x in self.scales ]
        else:
            result['scales'] = []
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
        # this might not be  used

        new_id = self.new_object_id()

        return Clip(
            obj_id = new_id,
            name = self.name,
            patterns = [ x for x in self.patterns ],
            length = self.length,
            arps = [ x for x in self.arps ],
            tempo = self.tempo,
            repeat = self.repeat,
            track_ids = [],
            scene_ids = [],
            slot_length = self.slot_length,
            next_clip = self.next_clip,
            auto_scene_advance = self.auto_scene_advance,
            scales = [ x for x in self.scales ]

        )

    @classmethod
    def from_dict(cls, song, data):
        return Clip(
            obj_id = data['obj_id'],
            name = data['name'],
            scales = [ song.find_scale(x) for x in data['scales'] ],
            patterns = [ song.find_pattern(x) for x in data['patterns'] ],
            length = data['length'],
            arps = [ song.find_arp(x) for x in data['arps'] ],
            tempo = data['tempo'],
            repeat = data['repeat'],
            track = song.find_track(data['track']),
            scene = song.find_scene(data['scene']),
            slot_length = data['slot_length'],
            next_clip = data['next_clip'],
            auto_scene_advance = data['auto_scene_advance']
        )

    def get_actual_scale(self, song, pattern, roller):

        if roller:
            return next(roller)

        if pattern and pattern.scale:
            return pattern.scale

        if self.scene.scale:
            return self.scene.scale

        if song.scale:
            return song.scale

        return Scale(root=Note(name="C", octave=0), scale_type='chromatic')

    def actual_tempo(self, song, pattern):

        if self.tempo is not None:
            return self.tempo
        if pattern.tempo is not None:
            return pattern.tempo
        if self.scene.tempo is not None:
            return self.scene.tempo
        if song.tempo is not None:
            return song.tempo

        raise Exception("?")

    def sixteenth_note_duration(self, song, pattern):

        tempo = float(self.actual_tempo(song, pattern))
        tempo_ratio = (120 / self.actual_tempo(song, pattern))
        snd = tempo_ratio * 125
        # print("SND=%s" % snd)
        return snd

    def slot_duration(self, song, pattern=None):

        patterns = self.patterns
        if pattern is not None:
            patterns = [ pattern ]


        total_duration = 0

        for pat in patterns:

            snd = self.sixteenth_note_duration(song, pat)
            slot_ratio = self.slot_length / (1/16.0)
            slot_duration = snd * slot_ratio

            total_duration = total_duration + slot_duration

        return total_duration

    def get_clip_duration(self, song):

        total = 0



        for pattern in self.patterns:
            total = total + self.slot_duration(song, pattern) * self.actual_length(pattern)

        return total


    def actual_length(self, pattern=None):

        if self.length:
            return self.length

        patterns = self.patterns
        if pattern is not None:
            patterns = [ pattern ]

        new_len = 0
        for pattern in patterns:
            pl = pattern.length
            if not pl:
               pl = len(pattern.slots)
            new_len = new_len + pl

        return new_len

    def get_notes(self, song):

        #print("E1: %s" % time.time())
        c1 = time.time()

        # how long is each slot in MS?


        all_notes = []

        t_start = 0.0

        arp_roller = None

        scales = self.scales
        if scales is None:
            scales = [ None ]

        degree_shifts = self.degree_shifts
        if degree_shifts is None:
            degree_shifts = [ 0 ]

        octave_shifts = self.octave_shifts
        if octave_shifts is None:
            octave_shifts = [ 0 ]

        degree_shifts = utils.roller(degree_shifts)
        octave_shifts = utils.roller(octave_shifts)
        scale_roller = utils.roller(self.scales)


        arp = None

        if self.arps:
            arp_roller = utils.roller(self.arps)

        for pattern in self.patterns:

            octave_shift = next(octave_shifts) + pattern.octave_shift
            degree_shift = next(degree_shifts)

            #print("degree shift: %s" % degree_shift)
            #print("octave shift: %s" % octave_shift)

            sixteenth = self.sixteenth_note_duration(song, pattern)
            slot_duration = self.slot_duration(song, pattern)

            # print("SD milliseconds=%s" % slot_duration)

            scale = self.get_actual_scale(song, pattern, scale_roller)
            #print("using scale: %s" % scale.name)

            if arp_roller:
                arp = next(arp_roller)

            assert scale is not None

            slots = pattern.slots

            if not pattern:
                continue

            # convert expressions into arrays of notes
            notation = SmartExpression(scale=scale, song=song, clip=self, track=self.track, pattern=pattern)

            use_length = self.actual_length()

            if use_length < len(slots):
                slots = slots[0:use_length]

            # expression evaluator will need to grow smarter for intra-track and humanizer fun
            # create a list of list of notes per step... ex: [ [ c4, e4, g4 ], [ c4 ] ]
            notes = [ notation.do(self, expression) for expression in slots ]

            notes = chord_list_to_notes(notes)


            notes = evaluate_ties(notes)
            notes = evaluate_shifts(notes, octave_shift, degree_shift)

            for slot in notes:
                for note in slot:
                    note.start_time = round(t_start)
                    note.end_time = round(t_start + note.length)
                t_start = t_start + slot_duration
                # print("t_start=%s" % t_start)

            # if the length of the pattern (or the clip) is shorter than the symbols provided, trim the pattern
            # to just contain the first part
            if self.length and self.length < len(notes):
                notes = notes[0:self.length]

            if arp:
                notes = arp.process(song, scale, self.track, notes)

            all_notes.extend(notes)

        c2 = time.time()

        return all_notes


    def get_events(self, song):
        notes = self.get_notes(song)
        events = notes_to_events(notes)

        return events

    def get_player(self, song, engine_class):


        # the player needs the scale so it can process mod events in track grabs
        # we need to fix this so instead the note knows the scale.

        player = Player(
            clip=self,
            song=song,
            engine=engine_class(song=song, track=self.track, clip=self),
        )

        return player



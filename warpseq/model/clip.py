from .base import ReferenceObject
from .pattern import Pattern
from classforge import Class, Field
from .transform import Transform
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
    tempo_shifts = Field(type=list, default=None, required=False, nullable=True)
    scale_note_shifts = Field(type=list, default=None, required=False, nullable=True)
    next_clip = Field(required=False, nullable=True)
    transforms = Field(type=list, default=None, nullable=True)
    tempo = Field(type=int, default=None, nullable=True)
    repeat = Field(type=int, default=-1, nullable=True)
    auto_scene_advance = Field(type=bool, default=False, nullable=False)

    # internal state
    track = Field(type=Track, default=None, required=False, nullable=True)
    scene = Field(type=Scene, default=None, required=False, nullable=True)

    _current_tempo_shift = Field(type=int, default=0, nullable=False)
    _tempo_roller = Field()
    _scale_roller = Field()
    _degree_roller = Field()
    _octave_roller = Field()
    _scale_note_roller = Field()
    _transform_roller = Field()

    def on_init(self):
        super().on_init()
        self.reset()

    def reset(self):

        if self.tempo_shifts:
            self._tempo_roller = utils.roller(self.tempo_shifts)
        else:
            self._tempo_roller = utils.roller([0])

        degree_shifts = self.degree_shifts
        if degree_shifts is None:
            degree_shifts = [ 0 ]

        octave_shifts = self.octave_shifts
        if octave_shifts is None:
            octave_shifts = [ 0 ]

        scale_note_shifts = self.scale_note_shifts
        if scale_note_shifts is None:
            scale_note_shifts = [ 0 ]

        self._degree_roller = utils.roller(degree_shifts)
        self._octave_roller = utils.roller(octave_shifts)

        if self.scales:
            self._scale_roller = utils.roller(self.scales)
        else:
            self._scale_roller = None

        self._scale_note_roller = utils.roller(scale_note_shifts)

        if self.transforms is not None:
            self._transform_roller = utils.roller(self.transforms)
        else:
            self._transform_roller = None

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
            next_clip = self.next_clip,
            auto_scene_advance = self.auto_scene_advance,
            degree_shifts = self.degree_shifts,
            scale_note_shifts = self.scale_note_shifts,
            tempo_shifts = self.tempo_shifts,
            octave_shifts = self.octave_shifts
        )
        if self.patterns:
            result['patterns'] = [ x.obj_id for x in self.patterns ]
        else:
            result['patterns'] = []

        if self.transforms:
            result['transforms'] = [ x.obj_id for x in self.transforms ]
        else:
            result['transforms'] = []

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
        raise Exception("DO NOT RECYCLE CLIPS!")

        new_id = self.new_object_id()
        c2 = Clip(
            obj_id = new_id,
            name = self.name,
            patterns = [ x for x in self.patterns ],
            length = self.length,
            tempo = self.tempo,
            repeat = self.repeat,
            slot_length = self.slot_length,
            next_clip = self.next_clip,
            auto_scene_advance = self.auto_scene_advance,
            degree_shifts = self.degree_shifts,
            octave_shifts = self.octave_shifts,
            scale_note_shifts = self.scale_note_shifts,
            tempo_shifts = self.tempo_shifts,

        )
        if self.arps:
            c2.arps = [ x for x in self.arps ]
        if self.scales:
            c2.scales = [ x for x in self.scales ]
        return c2

    @classmethod
    def from_dict(cls, song, data):
        return Clip(
            obj_id = data['obj_id'],
            name = data['name'],
            scales = [ song.find_scale(x) for x in data['scales'] ],
            patterns = [ song.find_pattern(x) for x in data['patterns'] ],
            length = data['length'],
            transforms = [ song.find_transform(x) for x in data['transforms'] ],
            tempo = data['tempo'],
            repeat = data['repeat'],
            track = song.find_track(data['track']),
            scene = song.find_scene(data['scene']),
            slot_length = data['slot_length'],
            next_clip = data['next_clip'],
            auto_scene_advance = data['auto_scene_advance'],
            degree_shifts = data['degree_shifts'],
            scale_note_shifts = data['scale_note_shifts'],
            octave_shifts = data['octave_shifts'],
            tempo_shifts = data['tempo_shifts']
        )

    def get_actual_scale(self, song, pattern, roller):

        from . scale import Scale
        from . note import Note

        if roller:
            return next(roller)
        if pattern and pattern.scale:
            return pattern.scale
        if self.scene.scale:
            return self.scene.scale
        if song.scale:
            return song.scale
        print("-- WARNING -- DEFAULT TO CHROMATIC SCALE -- EXPECTED?")
        return Scale(root=Note(name="C", octave=5), scale_type='chromatic')

    def actual_tempo(self, song, pattern):

        if self.tempo is not None:
            return self.tempo + self._current_tempo_shift
        if pattern.tempo is not None:
            return pattern.tempo  + self._current_tempo_shift
        if self.scene.tempo is not None:
            return self.scene.tempo  + self._current_tempo_shift
        if song.tempo is not None:
            return song.tempo  + self._current_tempo_shift

        raise Exception("?")

    def sixteenth_note_duration(self, song, pattern):
        tempo_ratio = (120 / self.actual_tempo(song, pattern))
        return tempo_ratio * 125

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

        # FIXME: this is long, clean it up.

        c1 = time.time()


        all_notes = []

        t_start = 0.0





        # arp = None

        if self.transforms:
            transform_roller = utils.roller(self.transforms)
        else:
            transform_roller = None

        pat_index = 0

        for pattern in self.patterns:

            self._current_tempo_shift = next(self._tempo_roller)

            pat_index = pat_index + 1
            no = next(self._octave_roller)
            octave_shift = no + pattern.octave_shift + self.track.instrument.base_octave
            degree_shift = next(self._degree_roller)
            scale_shift = next(self._scale_note_roller)
            slot_duration = self.slot_duration(song, pattern)
            scale = self.get_actual_scale(song, pattern, self._scale_roller)

            if self._transform_roller:
                transform = next(self._transform_roller)
            else:
                transform = None

            slots = pattern.slots

            # convert expressions into arrays of notes
            #print("SCALE=%s" % scale)
            notation = SmartExpression(scale=scale, song=song, clip=self, track=self.track, pattern=pattern)

            use_length = self.actual_length()

            if use_length < len(slots):
                slots = slots[0:use_length]

            # expression evaluator will need to grow smarter for intra-track and humanizer fun
            # create a list of list of notes per step... ex: [ [ c4, e4, g4 ], [ c4 ] ]

            notes = [ notation.do(self, expression) for expression in slots ]
            #print("N1>>>%s" % notes)
            notes = chord_list_to_notes(notes)
            notes = evaluate_ties(notes)
            #print("N2>>>%s" % notes)

            notes = evaluate_shifts(notes, octave_shift, degree_shift, scale, scale_shift)
            #print("N3>>>%s" % notes)


            for slot in notes:
                for note in slot:
                    note.start_time = round(t_start)
                    note.end_time = round(t_start + note.length)
                t_start = t_start + slot_duration

            # if the length of the pattern (or the clip) is shorter than the symbols provided, trim the pattern
            # to just contain the first part
            if self.length and self.length < len(notes):
                notes = notes[0:self.length]
            if transform:
                notes = transform.process(song, scale, self.track, notes)
            all_notes.extend(notes)

        c2 = time.time()
        # temporary debug to make sure pattern computation is efficient and doesn't cause audible gaps
        print(c2 - c1)

        return all_notes


    def get_events(self, song):
        notes = self.get_notes(song)
        events = notes_to_events(self, notes)
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



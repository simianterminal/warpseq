# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# a clip is a set of patterns and other details at the intersection
# of a scene and track

import time

from ..notation.note_parser2 import NoteParser
from ..notation.time_stream import (chord_list_to_notes, evaluate_ties, notes_to_events)
from ..playback.player import Player
from ..utils import utils
from .base import NewReferenceObject
from .pattern import Pattern
from .scale import Scale
from .transform import Transform


class Clip(NewReferenceObject):

    from . track import Track
    from . scene import Scene

    # -----

    # THIS SECTION: USER EDITABLE

    # PRIMARY FEATURES
    #name = Field(type=str, required=True, nullable=False)
    #scales = Field(type=list, required=False, nullable=True, default=None)
    #patterns = Field(type=list, required=True, nullable=False)
    #transforms = Field(type=list, default=None, nullable=True)

    # COLUMN TWO
    #rate = Field(type=float, default=1, nullable=False)
    #repeat = Field(type=int, default=-1, nullable=True)
    # these next two are mutually exclusive, if ASA is true, next_clip is ignored
    #auto_scene_advance = Field(type=bool, default=False, nullable=False)
    #next_clip = Field(required=False, nullable=True)

    #tempo_shifts = Field(type=list, default=None, required=False, nullable=True)

    # -------

    # FIXME: do we need this anymore? Not an input parameter.
    # length = Field(type=int, default=None, required=False, nullable=True)

    # basically internal, not exposed in the public API, use 'rate' instead
    # might be used later to implement some note length mods
    #slot_length = Field(type=float, default=0.0625, required=False, nullable=False)

    # internal state - not exposed
    #track = Field(type=Track, default=None, required=False, nullable=True)
    #scene = Field(type=Scene, default=None, required=False, nullable=True)
    #_current_tempo_shift = Field(type=int, default=0, nullable=False)
    #_tempo_roller = Field()
    #_scale_roller = Field()
    #_degree_roller = Field()
    #_octave_roller = Field()
    #_scale_note_roller = Field()
    #_transform_roller = Field()

    __slots__ = [
        'name', 'scales', 'patterns', 'transforms', 'rate', 'repeat', 'auto_scene_advance', 'next_clip', 'tempo_shifts'
        'obj_id',
        'slot_length',
        'track','scene','_current_tempo_shift','_tempo_roller','_transform_roller','_notation'
    ]

    def __init__(self, name=None, scales=None, patterns=None, transforms=None,  rate=1, repeat=-1, auto_scene_advance=False, next_clip=None, tempo_shifts=None, track=None, scene=None, slot_length=0.0625, obj_id=None):
        self.name = name
        self.scales = scales
        self.patterns = patterns
        self.transforms = transforms
        self.rate = rate
        self.repeat = repeat
        self.auto_scene_advance = auto_scene_advance
        self.next_clip = next_clip
        self.tempo_shifts = tempo_shifts
        self.obj_id = obj_id
        self.track = track
        self.scene = scene
        self.slot_length = slot_length
        self._current_tempo_shift = 0
        self._notation = NoteParser(clip=self)

        super(Clip, self).__init__()
        self.reset()

    def reset(self):
        """
        Resetting a clip (restarting it) moves all rolling positions in
        scales and so on to the first position in those lists.
        """

        # FIXME: why does this not reset the pattern?

        if self.tempo_shifts:
            self._tempo_roller = utils.roller(self.tempo_shifts)
        else:
            self._tempo_roller = utils.roller([0])

        if self.scales:
            self._scale_roller = utils.roller(self.scales)
        else:
            self._scale_roller = None

        if self.transforms is not None:
            self._transform_roller = utils.roller(self.transforms)
        else:
            self._transform_roller = utils.roller([ None ])

    def scenes(self, song):
        """
        Returns all scenes this clip is in.  While the code technically allows more than one
        the PublicApi does not - so this should return 0 or 1 scenes. We are leaving the implementation
        this way in case we want to implement symlinked clips (and not just patterns) later - which
        will keep from breaking song files between versions of the program.
        """
        return [ song.find_scene(x) for x in self.scene_ids ]

    def tracks(self, song):
        """
        Returns all tracks this clip is in. Like scenes() this should really just return 0 or 1
        tracks.
        """
        return [ song.find_track(x) for x in self.track_ids ]

    def to_dict(self):
        """
        Return a dictionary representation of the clip.
        """
        result = dict(
            obj_id = self.obj_id,
            name = self.name,
            repeat = self.repeat,
            slot_length = self.slot_length,
            next_clip = self.next_clip,
            auto_scene_advance = self.auto_scene_advance,
            tempo_shifts = self.tempo_shifts,
            rate = self.rate,
        )
        if self.patterns:
            result['patterns'] = [ x.obj_id for x in self.patterns ]
        else:
            result['patterns'] = []

        result["transforms"] = self._save_transforms()

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

    def _save_transforms(self):
        """
        support function to save transforms, which can be a flat list or can contain lists of transforms:
        ex: [t1, [t2,t3], t4, [t5,t6]].  Stacked transforms indicate multiple MIDI effects to be applied
        to a pattern at once.
        """
        if not self.transforms:
            return []
        results = []
        for x in self.transforms:
            if type(x) == list:
                results.append([ i.obj_id for i in x ])
            else:
                results.append(x.obj_id)
        return results

    def _load_transforms(self, data):
        """
        inverse of _save_transforms
        """
        results = []
        for x in data:
            if type(x) == list:
                results.append([ song.find_transform(i) for i in x ])
            else:
                results.append(song.find_transform(x))
        return results

    @classmethod
    def from_dict(cls, song, data):
        """
        Used to load a clip from a datastructure.
        """
        clip = Clip(
            obj_id = data['obj_id'],
            name = data['name'],
            scales = [ song.find_scale(x) for x in data['scales'] ],
            patterns = [ song.find_pattern(x) for x in data['patterns'] ],
            transforms = [],
            repeat = data['repeat'],
            track = song.find_track(data['track']),
            scene = song.find_scene(data['scene']),
            slot_length = data['slot_length'],
            next_clip = data['next_clip'],
            auto_scene_advance = data['auto_scene_advance'],
            tempo_shifts = data['tempo_shifts'],
            rate = data['rate']
        )
        clip.transforms = clip._load_transforms(data['transforms'])
        return clip

    def get_actual_scale(self, song, pattern, roller):
        """
        The scale can be set on the clip, as a list of scales to be used in series, and if not set
        there will be taken from the scene, then the pattern, the song.
        """

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

        # FIXME: we should make the song object create this scale if not set on the constructor
        # and remove this logic below:

        print("-- WARNING -- DEFAULT TO CHROMATIC SCALE -- EXPECTED?")
        return Scale(root=Note(name="C", octave=5), scale_type='chromatic')

    def actual_tempo(self, song, pattern):
        """
        The current tempo is the song's tempo after all multipliers and the current tempo shift is applied.
        """
        return int(song.tempo * self.rate * pattern.rate * self.scene.rate + self._current_tempo_shift)

    def sixteenth_note_duration(self, song, pattern):
        """
        A sixteenth note at 120 bpm is 125 ms. From this, we calculate all slot lengths.
        Unless "ratio" is set, all slots without ties are considered 1/16th notes.
        """
        tempo_ratio = (120 / self.actual_tempo(song, pattern))
        return tempo_ratio * 125

    def slot_duration(self, song, pattern):
        """
        Returns the slot duration in milliseconds - how long is each slot in a pattern before
        any transforms might be applied?
        """
        assert pattern is not None
        snd = self.sixteenth_note_duration(song, pattern)
        slot_ratio = self.slot_length / (1/16.0)
        slot_duration = snd * slot_ratio
        return slot_duration

    def get_clip_duration(self, song):
        """
        Returns the total length of the clip in milliseconds, which includes all patterns.
        """
        total = 0
        for pattern in self.patterns:
            total = total + self.slot_duration(song, pattern) * len(pattern.slots)
        return total

    def get_notes(self, song):
        """
        Evaluates the clip to return a list of notes
        """

        # FIXME: this is long, split into smaller functions

        # store the result here
        all_notes = []

        t_start = 0.0



        # loop over each pattern in the list, all must play for one "repeat" of the clip
        for pattern in self.patterns:

            # see if we need to nudge the tempo (default is no)
            self._current_tempo_shift = next(self._tempo_roller)

            # any scale notes will be shifted by the amount set on the pattern and instrument
            octave_shift = pattern.octave_shift + self.track.instrument.base_octave

            slot_duration = self.slot_duration(song, pattern)

            scale = self.get_actual_scale(song, pattern, self._scale_roller)

            # the list of transforms loops each time we move between patterns in the clip
            # each "item" may be a list of one or more stacked transforms
            if self._transform_roller:
                transform = next(self._transform_roller)
            else:
                transform = None

            slots = pattern.slots

            notation = self._notation

            notation.scale = scale
            notation.song = song
            notation.track = self.track
            notation.pattern = pattern
            notation.setup()

            notes = [ notation.do(expression, octave_shift) for expression in slots ]

            # the smart expressions may output chords, so map them back into notes
            # "notes" now looks like: [[n1, n2, n3], [n4], [], [n5], [n6]]
            notes = chord_list_to_notes(notes)
            # use ties to lengthen note events
            notes = evaluate_ties(notes)
            # now apply any octave shifts.

            # FIXME: Support for scale shifts is obsolete and this function can take less parameters
            # FIXME: this function is now obsolete.
            #notes = evaluate_shifts(notes, octave_shift, 0, scale, 0)


            # compute the start and end
            # times of each note
            # FIXME: move this into another function
            for slot in notes:
                for note in slot:
                    note.start_time = round(t_start)
                    note.end_time = round(t_start + note.length)
                    note.from_scale = scale
                t_start = t_start + slot_duration

            # if the length of the pattern (or the clip) is shorter than the symbols provided, trim the pattern
            # to just contain the first part

            #d1 = time.time()

            # apply any transforms to this pattern - there may be more than one

            if transform:
                # transforms can be in lists like: [t0, [t1, t2], t3, [ t4, t5, t6]]
                if type(transform) != list:
                    transform = [ transform ]
                for tform in transform:
                    notes = tform.process(scale, self.track, notes)

            #d2 = time.time()

            all_notes.extend(notes)

        return all_notes


    def get_events(self, song):
        """
        Return the list of events for use by the player class.  Events are basically note objects
        but are split by ON and OFF events.
        """
        c1 = time.time()
        rc = notes_to_events(self, self.get_notes(song))
        c2 = time.time()
        print("TIME=%s" % (c2-c1))
        return rc


    def get_player(self, song, engine_class):
        """
        Return an instance of Player that can play this clip.
        """

        player = Player(
            clip=self,
            song=song,
            engine=engine_class(song=song, track=self.track, clip=self),
        )
        return player

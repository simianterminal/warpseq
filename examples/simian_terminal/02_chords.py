# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how to express basic chords using roman
# numerals and other chord types with mod expressions. Chords
# will pick up the assigned scale.
#
# it also shows how to use ties ("-") and how to mix chords
# and scale notes.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=100)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=5, max_octave=10)

# setup tracks
api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# setup scales
api.scales.add(name='C-major', note='C', octave=0, scale_type='major')
api.scales.add(name='C-minor', note='C', octave=0, scale_type='natural_minor')

# setup patterns
api.patterns.add(name='quiet', slots=['','',])
api.patterns.add(name='major_hold', slots=['I', '-', '-', '-', '-', '-'])
api.patterns.add(name='major_gap', slots=['I', '_', '_', '_', '_', '_'])


api.patterns.add(name='major_chords', slots=['I', 'IV', 'V', ])
api.patterns.add(name='minor_chords', slots=['i', 'iv', 'v', ])
api.patterns.add(name='chords_with_silence_and_then_notes', slots = [ 'I', ' ', 1, 2, 3, 4, 5, 6 ])
api.patterns.add(name='chords_with_ties_and_notes', slots = [ 'I', '-', 1, 2, 3, 4, 5, 6,])
api.patterns.add(name='all_chord_types', slots = [
    '1 ch=major','2 ch=minor','3 ch=dim','4 ch=aug','1 ch=sus4','2 ch=sus2','3 ch=fourth',
    '4 ch=fifth','1 ch=M6','2 ch=m6','3 ch=dom7','4 ch=aug7','1 ch=dim7','1 ch=mM7'
])

# setup scenes
api.scenes.add(name='scene_0', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_4', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_5', rate=0.5, auto_advance=True)

# setup clips
api.clips.add(name='s0c', scene='scene_0', track='lead', scales=['C-major'], patterns=['major_hold', 'quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s1c', scene='scene_1', track='lead', scales=['C-major'], patterns=['major_chords','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s2c', scene='scene_2', track='lead', scales=['C-major'], patterns=['minor_chords','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3c', scene='scene_3', track='lead', scales=['C-major'], patterns=['chords_with_silence_and_then_notes','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s4c', scene='scene_4', track='lead', scales=['C-major'], patterns=['chords_with_ties_and_notes','quiet'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s5c', scene='scene_5', track='lead', scales=['C-major'], patterns=['all_chord_types','quiet'], repeat=1, auto_scene_advance=True)

# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_0')

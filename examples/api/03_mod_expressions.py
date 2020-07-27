# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
# What this demos shows:
# * learn about different types of mod expressions
# * how to jump up octaves
# * how to use sharps and flats
# * how to assign events randomly based on % probability
# * how to assign a value randomly from a range
# * how to assign a value randomly from a list
# * how to set MIDI CC
# * how to set velocity
# --------------------------------------------------------------
# Learning objectives:
# * fully understand basic mod expressions
# * be able to use mod expressions in transforms in the next lesson
# -------------------------------------------------------------
# Things to try:
# * anything goes!
# -------------------------------------------------------------

from warpseq.api.public import Api as WarpApi
from warpseq.api import demo

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
api.patterns.add(name='octave jumps', slots=['1','2','3','1 O+1','2 O+1','3 O+1','1 O+2','2 O+2', '3 O+2', '1 O-1', '1 O-2'])
api.patterns.add(name='sharps and flats', slots=[ '1','2','3','1 b','2 b','3 b','1 #','2 #', '3 #'] )
api.patterns.add(name='random octave jumps on certain steps', slots=['1','2 p=0.5 O-1','3','4 p=0.5 O+1'])
api.patterns.add(name='random flats on certain steps', slots=['1','2','3 p=0.5 x','4' ])
api.patterns.add(name='random octave jumps using a range', slots=['1','2','3','4 O=0:3'])
api.patterns.add(name='random octave jumps from a list', slots=[ '1', '2', '3', '4 O=0,1,2,3'])
api.patterns.add(name='fixed MIDI velocity', slots=['1','2 v=80','3 v=128','4 v=60'])
api.patterns.add(name='fixed MIDI CC', slots=[ '1 cc0=40 cc1=60', '2', '3 cc1=90, cc2=120', '4 cc2=90' ])
api.patterns.add(name='humanized MIDI velocity', slots=['1','2 v=80:100','3 v=80:100','4 v=80:100'])
api.patterns.add(name='humanized MIDI CC',slots=['1 cc0=40:100','2','3','4']) # kind of like sample and hold!
api.patterns.add(name='randomized gaps', slots=['1','2','3 p=0.65 x','4'])
api.patterns.add(name='many things also with chords',slots=['I cc0=50 v=90 O=0:3', 'IV cc0=75 v=90:100', '3 ch=power v=100 p=0.5 x cc0=60', '4 ch=sus4'])

# setup scenes
api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_4', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_5', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_6', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_7', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_8', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_9', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_10', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_11', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_12', rate=0.5, auto_advance=True)

# setup clips
api.clips.add(name='s1c', scene='scene_1', track='lead', scales=['C-major'], patterns=['octave jumps'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s2c', scene='scene_2', track='lead', scales=['C-major'], patterns=['sharps and flats'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3c', scene='scene_3', track='lead', scales=['C-major'], patterns=['random octave jumps on certain steps'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s4c', scene='scene_4', track='lead', scales=['C-major'], patterns=['random flats on certain steps'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s5c', scene='scene_5', track='lead', scales=['C-major'], patterns=['random octave jumps using a range'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s6c', scene='scene_6', track='lead', scales=['C-major'], patterns=['random octave jumps from a list'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s7c', scene='scene_7', track='lead', scales=['C-major'], patterns=['fixed MIDI velocity'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s8c', scene='scene_8', track='lead', scales=['C-major'], patterns=['fixed MIDI CC'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s9c', scene='scene_9', track='lead', scales=['C-major'], patterns=['humanized MIDI velocity'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s10c', scene='scene_10', track='lead', scales=['C-major'], patterns=['humanized MIDI CC'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s11c', scene='scene_11', track='lead', scales=['C-major'], patterns=['randomized gaps'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s12c', scene='scene_12', track='lead', scales=['C-major'], patterns=['many things also with chords'], repeat=4, auto_scene_advance=True)

# play
api.player.play_scene('scene_1')
for x in range(0,128000):
    api.player.advance(5)

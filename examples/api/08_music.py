# -------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# -------------------------------------------------------------
#
# this demo shows a basic 4/4 kick/snare pattern using absolute
# notes. It will not be adjusted by a scale change, which is
# important when talking to drum hardware and soft synths.
#
# after the basic pattern plays, the pattern changes up,
# showing how to advance a clip.
#
# try changing the patterns and adding a third scene.

from warpseq.api import demo
from warpseq.api.callbacks import Callbacks, DefaultCallback
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=120)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('kick_inst', device=DEVICE, channel=1, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('snare_inst', device=DEVICE, channel=2, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('lead_inst', device=DEVICE, channel=3, min_octave=0, base_octave=3, max_octave=10, muted=False)

# setup tracks
api.tracks.add(name='kick', instrument='kick_inst', muted=False)
api.tracks.add(name='snare', instrument='snare_inst', muted=False)
api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# setup scales
api.scales.add(name='main', note='C', octave=3, slots=[1, 'b3', 4, 'b5', 5, 'b7'])

# setup patterns
api.patterns.add(name='kick_4_4',  slots="C1 . . . C1 . . . C1 . . . C1 . . .".split())
api.patterns.add(name='snare_4_4', slots=". . D1 . . . D1 . . . D1 . . . D1 .".split())
api.patterns.add(name='L1', slots=[1,2,6,1,2,7,1,2,5,1,2,4])
api.patterns.add(name='L2', slots=[1,2,5,1,2,5,1,6,'4 O+1',5,2,1])
api.patterns.add(name='L3', slots=[1,2,'6 O+1',1,2,'7 O+1',1,2,5,1,2,4])


api.patterns.add(name='C1', slots=['I','IV','V','VI','I'])

# setup transforms
api.transforms.add(name='A1', slots=['1','O+1','O-1'], divide=3)

# setup scenes
api.scenes.add(name='scene_1', scale='main', auto_advance=True)
api.scenes.add(name='scene_2', scale='main', auto_advance=True)
api.scenes.add(name='scene_3', scale='main', auto_advance=True)
api.scenes.add(name='scene_4', scale='main', auto_advance=True)


#api.scenes.add(name='scene_2', scale='C-major', auto_advance=True)

# setup clips
api.clips.add(name='s1k1', scene='scene_1', track='kick', patterns=['kick_4_4'], repeat=None)
api.clips.add(name='s1s1', scene='scene_1', track='snare', patterns=['snare_4_4'], repeat=None)
api.clips.add(name='s1L1', scene='scene_1', track='lead', patterns=['L1','L2','L1','L3'], transforms=[], repeat=2, auto_scene_advance=True)

api.clips.add(name='s1k2', scene='scene_2', track='kick', patterns=['kick_4_4'], repeat=None, auto_scene_advance=True)
api.clips.add(name='s1s2', scene='scene_2', track='snare', patterns=['snare_4_4'], repeat=None)
api.clips.add(name='s1L2', scene='scene_2', track='lead', patterns=['L1','L2','L1','L3'], transforms=['A1'], repeat=2, auto_scene_advance=True)

# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_1')

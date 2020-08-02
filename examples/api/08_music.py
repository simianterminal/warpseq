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
api.song.edit(tempo=140)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('kick_inst', device=DEVICE, channel=1, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('snare_inst', device=DEVICE, channel=2, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('lead_inst', device=DEVICE, channel=3, min_octave=0, base_octave=5, max_octave=10, muted=False)
api.instruments.add('fx_inst', device=DEVICE, channel=4, min_octave=0, base_octave=4, max_octave=10, muted=False)
api.instruments.add('bass_inst', device=DEVICE, channel=5, min_octave=0, base_octave=4, max_octave=10, muted=False)

# setup tracks
api.tracks.add(name='kick', instrument='kick_inst', muted=False)
api.tracks.add(name='snare', instrument='snare_inst', muted=False)
api.tracks.add(name='lead', instrument='lead_inst', muted=False)
api.tracks.add(name='fx', instrument='fx_inst', muted=False)
api.tracks.add(name='bass', instrument='bass_inst', muted=False)

# setup scales
api.scales.add(name='main', note='C', octave=0, slots=[1, 'b3', 4, 'b5', 5, 'b7']) # minor blues
api.scales.add(name='alt', note='C', octave=0, slots=[1, 2, 'b3', 3, 5, 6 ]) # major blues
api.scales.add(name='alt2', note='E', octave=0, scale_type='akebono')

# setup patterns
api.patterns.add(name='kick_4_4',  slots="C1 . . . C1 . . . C1 . . . C1 . . .".split())
api.patterns.add(name='kick_alt',  slots="C1 . . . C1 . C1 . C1 . . . C1 . . .".split())
api.patterns.add(name='kick_alt1',  slots="C1 C1 . . C1 . C1 . C1 . . . C1 . . .".split())
api.patterns.add(name='kick_alt2',  slots="C1 . . . C1 . C1 . C1 . . . C1 C1 . .".split())
api.patterns.add(name='kick_alt3',  slots="C1 . C1 C1 C1 . C1 . C1 . . . C1 . C1 .".split())
api.patterns.add(name='kick_alt4',  slots="C1 . . . C1 . C1 . C1 . C1 . C1 C1 . .".split())

api.patterns.add(name='snare_4_4', slots=". . D1 . . . D1 . . . D1 . . . D1 .".split())
api.patterns.add(name='snare_alt', slots=". . D1 D1 . . D1 . . . D1 D1 . . D1 .".split())
api.patterns.add(name='snare_alt1', slots=". . D1 D1 . . D1 . D1 . D1 D1 . . D1 .".split())
api.patterns.add(name='snare_alt2', slots=". . D1 D1 . D1 D1 . D1 . D1 D1 . D1 D1 .".split())
api.patterns.add(name='snare_alt3', slots=". D1 D1 D1 . . D1 D1 D1 . D1 D1 . D1 D1 .".split())
api.patterns.add(name='snare_alt4', slots="D1 D1 D1 D1 D1 . D1 . . . D1 D1 . . D1 .".split())

api.patterns.add(name='L0', slots=[1,'-', 2, '-', 6, '-', 1, 2, '-', 7, 1, '-', '-'])
api.patterns.add(name='L1', slots=[1,2,6,1,2,7,1,2,5,1,2,4])
api.patterns.add(name='L2', slots=[1,2,5,1,2,5,1,6,'4 O+1',5,2,1])
api.patterns.add(name='L3', slots=[1,2,'6 O+1',1,2,'7 O+1',1,2,5,1,2,4])

api.patterns.add(name='X1', slots=[8,6,7,5,3,'.',9])
api.patterns.add(name='X2', slots=[9,1,9,5,1,5,2,4,0,1])

api.patterns.add(name='B1', slots=[1,4,5,1,4,5,1,4,6,1,2,5])
api.patterns.add(name='slide', slots=[8,7,6,5,4,3,2,1])
api.patterns.add(name='slide2', slots=[8,7,6,5,4,3,2,1,8,7,6,5,4,3,2,1,1,2,3,4,5,6,7,8])
api.patterns.add(name='slide3', slots=[8,8,7,7,6,6,5,5,4,4,3,3,2,2,1,1,1,1,1,1,1,1,1,1])
api.patterns.add(name='slide4', slots=[1,1,1,1,1,1,1,1,2,3,4,5,6,7,8,9,10])
#api.patterns.add(name='C1', slots=['I','IV','V','VI','I'])

# setup transforms
api.transforms.add(name='A1', slots=['1','O+1','O-1'], divide=3)
api.transforms.add(name='A2', slots=['1','S+4','S+5'], divide=6)
api.transforms.add(name='A3', slots=['1','O-1','O-2'], divide=6)
api.transforms.add(name='A4', slots=['1 ch=power', 'x', 'x', 'x' ], divide=1)
api.transforms.add(name='A5', slots=['1 O+1'], divide=2)
api.transforms.add(name='A6a', slots=['ch=power','x'], divide=1)
api.transforms.add(name='A6b', slots=['x','ch=power'], divide=1)

# setup scenes
api.scenes.add(name='scene_0', scale='main', auto_advance=True)
api.scenes.add(name='scene_1', scale='main', auto_advance=True)
api.scenes.add(name='scene_2', scale='alt', auto_advance=True)
api.scenes.add(name='scene_3', scale='alt', auto_advance=True)
api.scenes.add(name='scene_4', scale='main', auto_advance=True)
api.scenes.add(name='scene_5', scale='alt2', auto_advance=True)
api.scenes.add(name='scene_6', scale='alt2', auto_advance=True)
api.scenes.add(name='scene_7', scale='main', auto_advance=True)
api.scenes.add(name='scene_8', scale='main', auto_advance=True)
api.scenes.add(name='scene_9', scale='main', auto_advance=True)
api.scenes.add(name='scene_10', scale='main', auto_advance=True)
api.scenes.add(name='scene_11', scale='main', auto_advance=True)
api.scenes.add(name='scene_12', scale='main', auto_advance=True, rate=0.5)
api.scenes.add(name='scene_END', scale='main', auto_advance=True)

#api.scenes.add(name='scene_2', scale='C-major', auto_advance=True)

# setup clips

api.clips.add(name='s0a', scene='scene_0', track='lead', patterns=['slide4'], transforms=['A3'], repeat=1, auto_scene_advance=True)


api.clips.add(name='s1a', scene='scene_1', track='kick', patterns=['kick_4_4'], repeat=None)
api.clips.add(name='s1b', scene='scene_1', track='snare', patterns=['snare_4_4'], repeat=None)
api.clips.add(name='s1c', scene='scene_1', track='lead', patterns=['L1','L2','L1','L3'], transforms=[], repeat=1, auto_scene_advance=True)

api.clips.add(name='s1a', scene='scene_2', track='bass', patterns=['slide'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s1b', scene='scene_2', track='fx', patterns=['kick_4_4'], repeat=None)

api.clips.add(name='s3a', scene='scene_3', track='kick', patterns=['kick_4_4'], repeat=None, auto_scene_advance=True)
api.clips.add(name='s3b', scene='scene_3', track='snare', patterns=['snare_4_4'], repeat=None)
api.clips.add(name='s3c', scene='scene_3', track='lead', patterns=['X1','X2','X1','X2'], transforms=['A1'], repeat=1, auto_scene_advance=True)

api.clips.add(name='s4a', scene='scene_4', track='bass', patterns=['slide2'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s4b', scene='scene_4', track='fx', patterns=['kick_4_4'], repeat=None)

api.clips.add(name='s5a', scene='scene_5', track='kick', patterns=['kick_alt'], repeat=None, auto_scene_advance=True)
api.clips.add(name='s5b', scene='scene_5', track='snare', patterns=['snare_alt'], repeat=None)
api.clips.add(name='s5c', scene='scene_5', track='lead', patterns=['L0','L1','L2','L1','L3','L1'], transforms=['A3'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s5d', scene='scene_5', track='bass', patterns=['B1'], repeat=None)

api.clips.add(name='s6a', scene='scene_6', track='kick', patterns=['kick_alt1','kick_alt2','kick_alt3','kick_alt4'], tempo_shifts=[5,10,15,20,25,30,35], repeat=1, auto_scene_advance=True)
api.clips.add(name='s6b', scene='scene_6', track='snare', patterns=['snare_alt','snare_alt2','snare_alt3','snare_alt4'], tempo_shifts=[5,10,15,20,25,30,35], repeat=1)

api.clips.add(name='s7a', scene='scene_7', track='kick', patterns=['kick_alt'], repeat=None, auto_scene_advance=True)
api.clips.add(name='s7b', scene='scene_7', track='snare', patterns=['snare_alt'], repeat=None)
api.clips.add(name='s7c', scene='scene_7', track='lead', patterns=['X1','X2','X1','X2'], transforms=['A4'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s7d', scene='scene_7', track='bass', patterns=['X1','X1','X2','X1'], repeat=1)

api.clips.add(name='s8a', scene='scene_8', track='fx', patterns=['slide3'], repeat=1, auto_scene_advance=True)

api.clips.add(name='s9a', scene='scene_9', track='kick', patterns=['kick_4_4'], repeat=None, auto_scene_advance=True)
api.clips.add(name='s9b', scene='scene_9', track='snare', patterns=['snare_4_4'], repeat=None)
api.clips.add(name='s9c', scene='scene_9', track='lead', patterns=['L0','L1','L2','L1','L3','L1'], transforms=['A5'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s9d', scene='scene_9', track='bass', patterns=['L0','L1','L2','L3','L2','L1'], transforms=['A5'], repeat=1)

api.clips.add(name='s8a', scene='scene_10', track='fx', patterns=['slide3'], transforms=['A3'], repeat=1, auto_scene_advance=True)

api.clips.add(name='s10a', scene='scene_11', track='kick', patterns=['kick_4_4'], repeat=None, auto_scene_advance=True)
api.clips.add(name='s10b', scene='scene_11', track='snare', patterns=['snare_4_4'], repeat=None)
api.clips.add(name='s10c', scene='scene_11', track='lead', patterns=['X1','X2','X1','X2'], transforms=['A6a'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s10d', scene='scene_11', track='bass', patterns=['X1','X1','X1','X2'], transforms=['A6b'], repeat=1)

api.clips.add(name='s12a', scene='scene_12', track='lead', patterns=['slide3'], transforms=['A3'], repeat=1, auto_scene_advance=True)

# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_0')

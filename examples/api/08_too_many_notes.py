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
api.song.edit(tempo=95)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('kick_inst', device=DEVICE, channel=1, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('snare_inst', device=DEVICE, channel=2, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('lead_inst', device=DEVICE, channel=3, min_octave=0, base_octave=5, max_octave=10, muted=False)
api.instruments.add('bass_inst', device=DEVICE, channel=5, min_octave=0, base_octave=4, max_octave=10, muted=False)

# setup tracks
api.tracks.add(name='kick', instrument='kick_inst', muted=False)
api.tracks.add(name='snare', instrument='snare_inst', muted=False)
api.tracks.add(name='lead', instrument='lead_inst', muted=False)
api.tracks.add(name='bass', instrument='bass_inst', muted=False)

# setup scales
api.scales.add(name='main', note='C', octave=0, slots=[1, 'b3', 4, 'b5', 5, 'b7']) # minor blues
api.scales.add(name='alt', note='C', octave=0, slots=[1, 2, 'b3', 3, 5, 6 ]) # major blues
api.scales.add(name='alt2', note='C', octave=0, scale_type='minor')

# patterns can of course be generated programmatically
f1 = [1,4,6,5,4,3,2,1,4,3,2,5,3,2]
f2 = f1.copy()
f2.reverse()
f3 = ['1 O+1,2','4 S+0,2',6,'5 S+0,2']
f4 = f3.copy()
f4.reverse()

api.patterns.add(name='L0', slots=f1)
api.patterns.add(name='L1', slots=f2)
api.patterns.add(name='L2', slots=f3)
api.patterns.add(name='L3', slots=f4)
api.patterns.add(name='B1', slots=[1,1,2,3,1,1,1,3,1,1,5,1,1,1,4,2])
api.patterns.add(name='B2', slots=[1,1,'2 S+1',3,1,1,1,'3 O+1,2',1,1,5,1,'1 S+1,2,3',1,4,2])
api.patterns.add(name='kick4x4', slots=[1,''], rate=0.5)
api.patterns.add(name='snare4x4', slots=['',1], rate=0.5)
api.patterns.add(name='slide4', slots=[1,1,1,2,3,4,5,6,7,8,9,10])
api.patterns.add(name='slide3', slots=[8,8,7,7,6,6,5,5,4,4,3,3,2,2,1,1])

# setup transforms
api.transforms.add(name='A2', slots=['1','S+4','S+5'], divide=6)
api.transforms.add(name='A3', slots=['1','O-1','O-2'], divide=3)
api.transforms.add(name='A4', slots=['1','S-1','S-2','S-3' ], divide=4)

# setup scenes
# scene names don't have to be chronological, you can leave gaps like old BASIC programs if you want
# or give them descriptive names
api.scenes.add(name='scene_0', scale='main', auto_advance=True)
api.scenes.add(name='scene_1', scale='main', auto_advance=True)
api.scenes.add(name='scene_3', scale='main', auto_advance=True)
api.scenes.add(name='scene_5', scale='alt', auto_advance=True)
api.scenes.add(name='scene_11', scale='alt2', auto_advance=True)

# clips will play a set of  patterns each
pat1 = [ 'L3','L2','L1']
pat2 = [ 'L1','L2','L3']
pat3 = [ 'B1','B2']

# setup clips
api.clips.add(name='s0a', scene='scene_0', track='lead', patterns=['slide4'], transforms=['A3'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s1c', scene='scene_1', track='lead', patterns=pat1, transforms=[], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3c', scene='scene_3', track='lead', patterns=pat2, transforms=['A4'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3b', scene='scene_3', track='bass', patterns=pat3, transforms=[], repeat=None)
api.clips.add(name='s5c', scene='scene_5', track='lead', patterns=pat1, transforms=['A2'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s5b', scene='scene_5', track='bass', patterns=pat3, transforms=[], repeat=None)
api.clips.add(name='s5k', scene='scene_5', track='kick', patterns=['kick4x4'], repeat=None)
api.clips.add(name='s12a', scene='scene_11', track='lead', patterns=['slide3'], transforms=['A3'], repeat=1, auto_scene_advance=True)

api.player.loop('scene_0')

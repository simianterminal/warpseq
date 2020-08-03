# -------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# -------------------------------------------------------------
#
# https://soundcloud.com/mpdehaan

# *** THIS IS NOT DONE AND IS MORE OF A TEST TRACK AT THE MOMENT ***

from warpseq.api import demo
from warpseq.api.callbacks import Callbacks, DefaultCallback
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=96)

# setup instruments
DEVICE = demo.suggest_device(api, 'USB MIDI Interface')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('setup_inst', device=DEVICE, channel=16, min_octave=0, base_octave=5, max_octave=10, muted=False)
api.instruments.add('drum1_inst', device=DEVICE, channel=8, min_octave=0, base_octave=0, max_octave=10, muted=False)

# setup tracks
api.tracks.add(name='setup', instrument='setup_inst', muted=True)
api.tracks.add(name='lead', instrument='lead_inst', muted=False)
api.tracks.add(name='drum1', instrument='drum1_inst', muted=False)

# setup scales
api.scales.add(name='main', note='F', octave=0, scale_type='major')

api.patterns.add(name='vars', slots=[
    '1 $w=0 $x=0 $y=0 $z=1',
    '1 $w=1 $x=1 $z=1',
    '1 $w=0 $x=2 $y=1 $z=2',
    '1 $x=3 $z=1'
])
api.patterns.add(name='vars2', slots=[
    '1 $w=1 $x=1 $y=1 $z=2',
    '1 $w=1 $x=0 $z=0',
    '1 $w=3 $x=2 $y=1 $z=1',
    '1 $x=0 $z=1'
])
api.patterns.add(name='L0', slots=[
    1,
    "-"
    "2",
    "-",
    
    "3 O+1",
    "1 S+$y O+$y",
    "4",
    "-",

    "1 S+$x",
    "4",
    "2 O+$w",
    "3 O+$y",

    "-4",
    "2 S+$x",
    "-",
    "-"
])
api.patterns.add(name='D0', slots=[1,'','','',1,'','','',1,'','','',1,'','',''], rate=1)

#api.patterns.add(name='L0', slots=[1,"",2,"","3","",'4',"",5])


# setup transforms
#api.transforms.add(name='A2', slots=['1','S+4','S+5'], divide=6)

# setup scenes
# scene names don't have to be chronological, you can leave gaps like old BASIC programs if you want
# or give them descriptive names
api.scenes.add(name='scene_0', scale='main', auto_advance=True)
api.scenes.add(name='scene_1', scale='main', auto_advance=True)
api.scenes.add(name='scene_END', scale='main', auto_advance=True)

# clips will play a set of  patterns each
pat1 = [ 'L3','L2','L1']
pat2 = [ 'L1','L2','L3']
pat3 = [ 'B1','B2']

# setup clips
api.clips.add(name='s0_setup', scene='scene_0', track='setup', patterns=['vars'], repeat=None, rate=0.0625)
api.clips.add(name='s0a', scene='scene_0', track='lead', patterns=['L0'], transforms=[], repeat=4, auto_scene_advance=True)

api.clips.add(name='s1_setup', scene='scene_1', track='setup', patterns=['vars2'], repeat=None, rate=0.0625)
api.clips.add(name='s1a', scene='scene_1', track='lead', patterns=['L0'], transforms=[], repeat=4, auto_scene_advance=True)
api.clips.add(name='s1dX', scene='scene_1', track='drum1', patterns=['D0'] , transforms=[], repeat=None)

api.player.loop('scene_1')

# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# MIDI CV Interface Connected To Eurorack As Follows:
#
# Basic Connections:
# Track 1: Noise Engineering Cursus Iteritas Percido
# Track 2: Noise Engineering Manis Iteritas
# Track 5: Bassimilus Iteritas Alter
# Track 6: Bassimilus Iteritas Alter
# Track 7: Bassimilus Iteritas Alter
# Track 8: Gate Output - When On, Toggles Algorithm on Cursus Iteritas Percido
# LFO => Bassimilus Iteritas Alter Pitch (Track 7)
#
# Synth Bus Tracks 1-2, All UAD Plugins: Century Channel => Culture Vulture => Galaxy Tape Echo
# Drum Bus Tracks 5-7, All UAD Plugins: Century Channel => Culture Vulture
# Mix Bus, UHE Satin, Service Panel Tweaked for slight old tape effects

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=116)

# setup instruments
DEVICE = demo.suggest_device(api, 'USB MIDI Interface')
api.instruments.add('CIP', device=DEVICE, channel=1, min_octave=0, base_octave=2, max_octave=10)
api.instruments.add('MI', device=DEVICE, channel=2, min_octave=0, base_octave=1, max_octave=10)
api.instruments.add('AT1', device=DEVICE, channel=3, min_octave=0, base_octave=0, max_octave=10)
api.instruments.add('AT2', device=DEVICE, channel=4, min_octave=0, base_octave=0, max_octave=10)
api.instruments.add('BIA1', device=DEVICE, channel=5, min_octave=0, base_octave=2, max_octave=10)
api.instruments.add('BIA2', device=DEVICE, channel=6, min_octave=0, base_octave=2, max_octave=10)
api.instruments.add('BIA3', device=DEVICE, channel=7, min_octave=0, base_octave=2, max_octave=10)
api.instruments.add('CHAOS', device=DEVICE, channel=8, min_octave=0, base_octave=1, max_octave=10)
api.instruments.add('VARS', device=DEVICE, channel=9, min_octave=0, base_octave=1, max_octave=10, muted=True)

# setup tracks
api.tracks.add(name='CIP', instrument='CIP')
api.tracks.add(name='MI', instrument='MI')
api.tracks.add(name='AT1', instrument='AT1')
api.tracks.add(name='AT2', instrument='AT2')
api.tracks.add(name='BIA1', instrument='BIA1')
api.tracks.add(name='BIA2', instrument='BIA2')
api.tracks.add(name='BIA3', instrument='BIA3')
api.tracks.add(name='CHAOS', instrument='CHAOS')
api.tracks.add(name='VARS', instrument='VARS')

# setup scales
api.scales.add(name='s0', note='C', octave=0, scale_type='minor')
api.scales.add(name='s1', note='C', octave=0, scale_type='minor_pentatonic')
api.scales.add(name='s2', note='C', octave=0, scale_type='major')
api.scales.add(name='s3', note='C', octave=0, scale_type='pentatonic')

# NON-DRUM PATTERNS

api.patterns.add(name='p1', slots=[
    '1 v=127 O+1','4 v=20','5', '7 v=60',
    '2 v=127','5 v=20 O+1','6', '2 v=60',
    '3 v=127 O+1','7 v=20','5', '4 v=60',
    '6 v=127','2 v=20 O+1','5', '3 v=60',
])
api.patterns.add(name='p2', slots=[
    '1 v=127 O+1','4 v=20','5', '7 v=60',
    '2 v=127','6 v=20 O+1','6', '2 v=60',
    '3 v=127 O+1','7 v=20','5', '4 v=60',
    '6 v=127','2 v=20 O+1','6', '3 v=60',
])
api.patterns.add(name='p3', slots=[
    '1 v=127 O+1','4 v=20','5', '7 v=60',
    '2 v=127','7 v=20 O+1','6', '2 v=60',
    '3 v=127 O+1','7 v=20','5', '4 v=60',
    '6 v=127','2 v=20 O+1','7', '3 v=60',
])
api.patterns.add(name='p4', slots=[
    '1 v=127 O+2','4 v=70','5', '7 v=80',
    '2 v=127 O+1','8 v=75 O+1','6', '2 v=90',
    '3 v=127 O+2','7 v=70 O+1','5', '4 v=80',
    '6 v=127 O+1','2 v=75 O+1','8 O+1', '3 v=90',
])
api.patterns.add(name='x1', slots=[1,6,4,2,1,6,4,3,1,6,4,1,1,6,4,3])
api.patterns.add(name='x2', slots=[1,5,4,2,1,5,4,3,1,5,4,1,1,5,4,3])
api.patterns.add(name='x3', slots=[1,4,4,2,1,4,4,3,1,4,4,1,1,4,4,3])
api.patterns.add(name='x4', slots=[1,3,4,2,1,3,3,3,1,3,4,1,1,3,3,3])
api.patterns.add(name='y1', slots=['1 ch=major',6,4,2,1,6,4,3,1,6,4,1,1,6,4,3])
api.patterns.add(name='y2', slots=['1 ch=major',5,4,2,'1 ch=minor',5,4,3,'1 ch=major',5,4,1,'1 ch=major',5,4,3])
api.patterns.add(name='y3', slots=['1 ch=major',4,4,2,'1 ch=minor',4,4,3,'1 ch=major',4,4,1,'1 ch=major',4,4,3])
api.patterns.add(name='y4', slots=['1 ch=major',1,3,4,'2 ch=minor',1,3,3,1,3,4,1,1,3,3,3])
api.patterns.add(name='slide1', slots=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,13,12,11,10,9,8,7,6,5,4,3,2,1],rate=4)

# GATE MOD PATTERNS

api.patterns.add(name='gate_mod2', slots=['C0','','','','C0','','','','C0','','','','C0','','',''])
api.patterns.add(name='gate_mod3', slots=['C0','','','','C0','','C0','','C0','','','','C0','','C0',''])
api.patterns.add(name='gate_mod4', slots=['C0','','C0','','C0','','C0','','C0','','C0','C0','','C0',''])
api.patterns.add(name='gate_mod5', slots=['C0','','C0','','C0','C0','C0','','C0','','C0','','C0','C0','C0',''])
api.patterns.add(name='gate_mod6', slots=['C0','C0','C0','','C0','','','C0','C0','','C0','','C0','','C0','C0'])

# DRUM PATTERNS

api.patterns.add(name='d1', slots=['1', '', '', '','1', '', '', '','1', '', '', '','1', '', '', ''])
api.patterns.add(name='d2', slots=['', 'C0', '', '','', 'C0', '', '','', 'C0', '', '','', 'C0', '', ''])
api.patterns.add(name='d3', slots=['C0', '', '', '','', '', '', '','C0', '', '', '','', '', '', ''])

api.patterns.add(name='d1a', slots=['1', '', '', '','1', '1', '', '','1', '1', '', '','1', '1', '', ''])
api.patterns.add(name='d2a', slots=['', 'C0', '', '','', 'C0', '', '','C0', 'C0', 'C0', 'C0','', 'C0', '', ''])
api.patterns.add(name='d3a', slots=['C0', '', '', 'C0','C0', 'C0', 'C0', '','C0', '', '', '','', '', '', ''])

api.patterns.add(name='d1b', slots=['C0', 'C0', '', '','1', '', '', '','1', '', '', '','1', '', '', ''])
api.patterns.add(name='d2b', slots=['', 'C0', '', '','', 'C0', '', 'C0','', 'C0', '', 'C0','', 'C0', '', ''])
api.patterns.add(name='d3b', slots=['C0', '', '', 'C0','', '', '', '','C0', 'C0', '', '','', '', 'C0', 'C0'])

# TRANSFORMS

api.transforms.add(name='t1', slots=['1','1','O+1'], divide=1)
api.transforms.add(name='octave_up', slots=['O+1'], divide=1)
api.transforms.add(name='octave_down', slots=['O-1'], divide=1)
api.transforms.add(name='slice', slots=[1,1,1], divide=3)
api.transforms.add(name='odds', slots=['x',1], divide=3)
api.transforms.add(name='evens', slots=[1,'x'], divide=3)

# SCENES

api.scenes.add(name='1', rate=1, auto_advance=True, scale='s0')
api.scenes.add(name='2', rate=1, auto_advance=True, scale='s0')
api.scenes.add(name='3', rate=1, auto_advance=True, scale='s0')
api.scenes.add(name='5', rate=1, auto_advance=True, scale='s2')
api.scenes.add(name='6', rate=1, auto_advance=True, scale='s2')
api.scenes.add(name='7', rate=1, auto_advance=True, scale='s2')
api.scenes.add(name='8', rate=1, auto_advance=True, scale='s3')
api.scenes.add(name='9', rate=1, auto_advance=True, scale='s3')
api.scenes.add(name='10', auto_advance=True, scale='s3', rate=0.5)
api.scenes.add(name='END', auto_advance=True, scale='s3')

# CLIPS

api.clips.add(name='s1A', scene='1', track='BIA1', patterns=['d1'], repeat=None)
api.clips.add(name='s1B', scene='1', track='BIA2', patterns=['d2'], repeat=None)
api.clips.add(name='s1C', scene='1', track='CIP', patterns=['p1','p2','p3','p4','slide1'],
              transforms=[['t1','octave_up']], auto_scene_advance=True, repeat=1)
api.clips.add(name='s1D', scene='1', track='CHAOS', patterns=['gate_mod2'], repeat=None)

# ---

api.clips.add(name='s2C', scene='2', track='CIP', patterns=['slide1'],
              transforms=['t1'], auto_scene_advance=True, repeat=1)

# ---

api.clips.add(name='s3A', scene='3', track='BIA1', patterns=['d1'], repeat=None)
api.clips.add(name='s3B', scene='3', track='BIA2', patterns=['d2'], repeat=None)
api.clips.add(name='s3C', scene='3', track='MI', patterns=['p1','p2','p3','p4','slide1'],
              transforms=['t1'], auto_scene_advance=True, repeat=1)
 # ---

api.clips.add(name='s5A', scene='5', track='BIA1', patterns=['d1'], repeat=None)
api.clips.add(name='s5B', scene='5', track='BIA2', patterns=['d2'], repeat=None)
api.clips.add(name='s5C', scene='5', track='CIP', patterns=['y1','y2','y3','y4'],
              transforms=['slice'], auto_scene_advance=True, repeat=1)
api.clips.add(name='s5D', scene='5', track='CHAOS', patterns=['gate_mod3'], repeat=None)

# ---

api.clips.add(name='s6A', scene='6', track='BIA1', patterns=['d1'], repeat=None)
api.clips.add(name='s6B', scene='6', track='BIA2', patterns=['d2'], repeat=None)
api.clips.add(name='s6C', scene='6', track='CIP', patterns=['slide1','y1','y2','y3','y4'], scales=['s0','s1','s2','s0'],
              transforms=[['octave_up','evens']], rate=2, auto_scene_advance=True, repeat=1)
api.clips.add(name='s6D', scene='6', track='CHAOS', patterns=['gate_mod4'], repeat=None)

# ---

api.clips.add(name='s7A', scene='7', track='BIA1', patterns=['d1a'], repeat=None)
api.clips.add(name='s7B', scene='7', track='BIA2', patterns=['d2a'], repeat=None)
api.clips.add(name='s7C', scene='7', track='CIP', patterns=['y1','y2','y3','y4','slide1'], scales=['s0','s1','s2','s0'],
              transforms=[['octave_up','odds']], rate=2, auto_scene_advance=True, repeat=1)
api.clips.add(name='s7D', scene='7', track='CHAOS', patterns=['gate_mod5'], repeat=None)
api.clips.add(name='s7B', scene='7', track='BIA3', patterns=['d3a'], repeat=None)

# ---

api.clips.add(name='s8A', scene='8', track='BIA1', patterns=['d1a'], repeat=None)
api.clips.add(name='s8B', scene='8', track='BIA2', patterns=['d2a'], repeat=None)
api.clips.add(name='s8C', scene='8', track='CIP', patterns=['x1','y1','x2','y2','x3','y3','x4','y4'], scales=['s0','s1','s2','s0'],
              transforms=[['octave_up','odds']], rate=2, auto_scene_advance=True, repeat=1)
api.clips.add(name='s8D', scene='8', track='CHAOS', patterns=['gate_mod6'], repeat=None)
api.clips.add(name='s8B', scene='8', track='BIA3', patterns=['d3a'], repeat=None)

# ---

api.clips.add(name='s9A', scene='9', track='BIA1', patterns=['d1b'], repeat=None)
api.clips.add(name='s9B', scene='9', track='BIA2', patterns=['d2b'], repeat=None)
api.clips.add(name='s9C', scene='9', track='MI', patterns=['p1','p2','p3','p4','slide1','p1','p2','p3','p4','slide1'], transforms=['t1','octave_up'],
              auto_scene_advance=True, repeat=1)

# ---

api.clips.add(name='s10C', scene='10', track='CIP', patterns=['slide1', 'slide1', 'slide1'], transforms=[['t1','octave_down']], auto_scene_advance=True, repeat=1)

# ---

api.player.loop('1')

# -------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# -------------------------------------------------------------
#
# https://soundcloud.com/mpdehaan

# as recorded, all eurorack:
# Track1: Verbos Complex Oscillator => Verbos Amp&Tone (no modulation) => Worng Parallax Filter (2nd envelope) => Worng Vertex (limited LFOs)
# Track2: Livewire AFG => Verbos Amp&Tone (no modulation) => Worng Vertex
# Tracks 6-8: Noise Engineering Bassimilus Iteritas Alter (x3).
# Synth processing: UAD Struder
# Drum processing: UAD Distressor
# no MIDI CC or velocity usage from Warp, though that might have been interesting
#
# variable handling is a little different now than when recorded (on a development version),
# so it won't quite sound the same

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
api.instruments.add('lead2_inst', device=DEVICE, channel=2, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('drum2_inst', device=DEVICE, channel=7, min_octave=0, base_octave=0, max_octave=10, muted=False)
api.instruments.add('drum3_inst', device=DEVICE, channel=6, min_octave=0, base_octave=0, max_octave=10, muted=False)

# setup tracks
api.tracks.add(name='setup', instrument='setup_inst', muted=True)
api.tracks.add(name='lead', instrument='lead_inst', muted=False)
api.tracks.add(name='drum1', instrument='drum1_inst', muted=False)
api.tracks.add(name='lead2', instrument='lead2_inst', muted=False)
api.tracks.add(name='drum2', instrument='drum2_inst', muted=False)
api.tracks.add(name='drum3', instrument='drum3_inst', muted=False)

# setup scales
api.scales.add(name='intro', note='F', octave=0, scale_type='minor')
api.scales.add(name='main', note='F', octave=0, scale_type='major')
api.scales.add(name='main2', note='A', octave=1, scale_type='major')

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

lead_slots = [
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
]

lead_slots4 = [
    4,
    "-"
    "2",
    "-",

    "5 O+1",
    "1 S+$y O+$y",
    "4",
    "-",

    "4 S+$x",
    "4",
    "5 O+$w",
    "3 O+$y",

    "-4",
    "3 S+$x",
    "-",
    "-"
]

lead_slots5 = [
    4,
    "4",
    "2 S+$x",
    "2",

    "5 O+1",
    "1 S+$y O+$y",
    "4",
    "4",

    "4 S+$x",
    "4",
    "5 O+$w",
    "3 S+$x",

    "-4",
    "3 S+$x",
    "1",
    "1"
]

lead_slots2 = lead_slots.copy()
lead_slots2.reverse()
lead_slots3 = lead_slots.copy()
lead_slots3.extend(["-","-","-","-"])

api.patterns.add(name='L0', slots=lead_slots)
api.patterns.add(name='L1', slots=lead_slots2)
api.patterns.add(name='FILL0', slots=lead_slots3, rate=1)
api.patterns.add(name='L3', slots=lead_slots4)
api.patterns.add(name='L4', slots=lead_slots5)

api.patterns.add(name='D0', slots=[1,'','','',1,'','','',1,'','','',1,'','',''], rate=1)
api.patterns.add(name='D0a', slots=[1,'',1,'',1,'','','',1,'',1,'',1,'','',''], rate=1)

api.patterns.add(name='D1', slots=['',1,], rate=0.25)
api.patterns.add(name='D1a', slots=['',1,1,1], rate=0.5)

api.patterns.add(name='D2', slots=[1,'',1,''], rate=0.5)
api.patterns.add(name='D2a', slots=[1,'',1,1,1,1,1,''], rate=1)
api.patterns.add(name='slide', slots=[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1])

# setup transforms
api.transforms.add(name='octave_up', slots=['O+1'], divide=1)
api.transforms.add(name='arp1', slots=['O-1','O+1'], divide=1)

# setup scenes
# scene names don't have to be chronological, you can leave gaps like old BASIC programs if you want
# or give them descriptive names
api.scenes.add(name='scene_0', scale='intro', auto_advance=True)
api.scenes.add(name='scene_1', scale='intro', auto_advance=True)
api.scenes.add(name='scene_2', scale='intro', auto_advance=True)
api.scenes.add(name='scene_3', scale='main', auto_advance=True)
api.scenes.add(name='scene_4', scale='main', auto_advance=True)
api.scenes.add(name='scene_5', scale='main2', auto_advance=True)
api.scenes.add(name='scene_7', scale='main2', auto_advance=True)
api.scenes.add(name='scene_7a', scale='main2', auto_advance=True)
api.scenes.add(name='scene_8', scale='main', auto_advance=True)
api.scenes.add(name='scene_9', scale='main', auto_advance=True)
api.scenes.add(name='scene_10', scale='main', auto_advance=True, rate=0.5)

api.scenes.add(name='scene_END', scale='main', auto_advance=True)

# setup clips
# lead plays in
api.clips.add(name='s0_setup', scene='scene_0', track='setup', patterns=['vars'], repeat=None, rate=0.0625)
api.clips.add(name='s0a', scene='scene_0', track='lead', patterns=['L0'], transforms=[], repeat=4, auto_scene_advance=True)

# lead plays, different variables, add drums
api.clips.add(name='s1_setup', scene='scene_1', track='setup', patterns=['vars2'], repeat=None, rate=0.0625)
api.clips.add(name='s1a', scene='scene_1', track='lead', patterns=['L0'], transforms=[], repeat=4, auto_scene_advance=True)
api.clips.add(name='s1dX', scene='scene_1', track='drum1', patterns=['D0'] , transforms=[], repeat=None)

# we need something fun here - just a placeholder for now
api.clips.add(name='s1dX', scene='scene_2', track='lead', patterns=['slide'] , transforms=[], repeat=1, auto_scene_advance=True)

# lead reverses, keep drums
api.clips.add(name='s1_setup', scene='scene_3', track='setup', patterns=['vars2'], repeat=None, rate=0.0625)
api.clips.add(name='s1a', scene='scene_3', track='lead', patterns=['L1'], transforms=[], repeat=4, auto_scene_advance=True)
api.clips.add(name='s1dX', scene='scene_3', track='drum1', patterns=['D0'] , transforms=[], repeat=None)

# fill sequence, new instrument
api.clips.add(name='1', scene='scene_4', track='setup', patterns=['vars'], repeat=None, rate=0.0625)
api.clips.add(name='2', scene='scene_4', track='drum1', patterns=['D0'] , transforms=[], repeat=None)
api.clips.add(name='3', scene='scene_4', track='lead2', patterns=['FILL0'], transforms=[], repeat=4, auto_scene_advance=True)
api.clips.add(name='4', scene='scene_4', track='drum2', patterns=['D1'] , transforms=[], repeat=None)

# add third drum part, back to original instrument, transform up
api.clips.add(name='5', scene='scene_5', track='drum2', patterns=['D1'] , transforms=[], repeat=None)
api.clips.add(name='6', scene='scene_5', track='drum1', patterns=['D0'] , transforms=[], repeat=None)
api.clips.add(name='7', scene='scene_5', track='drum3', patterns=['D2'] , transforms=[], repeat=None)
api.clips.add(name='8', scene='scene_5', track='lead', patterns=['L3'], transforms=[], repeat=4, auto_scene_advance=True)

# back to octave up, alt pattern, switchup drums
api.clips.add(name='11', scene='scene_7', track='drum2', patterns=['D0'] , transforms=[], repeat=None)
api.clips.add(name='12', scene='scene_7', track='drum1', patterns=['D1'] , transforms=[], repeat=None)
api.clips.add(name='13', scene='scene_7', track='drum3', patterns=['D2'] , transforms=[], repeat=None)
api.clips.add(name='14', scene='scene_7', track='lead2', patterns=['L4'], transforms=[], repeat=4, auto_scene_advance=True)

api.clips.add(name='14a', scene='scene_7a', track='lead', patterns=['slide'] , transforms=[], repeat=1, auto_scene_advance=True)

# reprise - heavy drums
api.clips.add(name='15', scene='scene_8', track='drum2', patterns=['D1a'] , transforms=[], repeat=None)
api.clips.add(name='16', scene='scene_8', track='drum1', patterns=['D0a'] , transforms=[], repeat=None)
api.clips.add(name='17', scene='scene_8', track='drum3', patterns=['D2a'] , transforms=[], repeat=None)
api.clips.add(name='18', scene='scene_8', track='lead', patterns=['L0'], transforms=[], repeat=4, auto_scene_advance=True)

# same as before but arp time
api.clips.add(name='19', scene='scene_9', track='drum2', patterns=['D1a'] , transforms=[], repeat=None)
api.clips.add(name='20', scene='scene_9', track='drum1', patterns=['D0a'] , transforms=[], repeat=None)
api.clips.add(name='21', scene='scene_9', track='drum3', patterns=['D2a'] , transforms=[], repeat=None)
api.clips.add(name='22', scene='scene_9', track='lead', patterns=['L0'], transforms=['arp1'], repeat=4, auto_scene_advance=True)

# back to lead2, no drums
api.clips.add(name='23', scene='scene_10', track='setup', patterns=['vars'], repeat=None, rate=0.0625)
api.clips.add(name='24', scene='scene_10', track='lead', patterns=['L0'], transforms=[], repeat=2, auto_scene_advance=True)

api.player.loop('scene_0')

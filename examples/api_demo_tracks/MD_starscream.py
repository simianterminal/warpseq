# -------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# -------------------------------------------------------------
#
# https://soundcloud.com/mpdehaan

# as recorded, all eurorack:

# ** THREE TRACKS CONTROLLING THE FIRST INSTRUMENT **
#
# Track1 - Livewire AFG.
#   subwoofer and alien saws output go to a Random Source Serge Wave Multiplier
#   the output is amplified by an unmodulated Verbos Amp & Tone
#   the output feeds into a Make Noise QPAS (low pass outputs)
#   a gate triggered envelope feeds a Worng Vertex VCA
#   a second envelope slightly offsets the filter of the QPAS
# Track 8 - Gate Mod
#   when the gates fire a gate signal is send the "radiate" inputs of the QPAS, moving both filters in opposite directions
# Track 2 - Pitch Mod
#   the pitch signal is  used in place of a MIDI CC or Velocity input that controls the rate of the mod oscillator of a Verbos Amp & Tone
#   the mod oscillator is attenuated and is sent to the FM of the QPAS.

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
api.song.edit(tempo=65)

# setup instruments
DEVICE = demo.suggest_device(api, 'USB MIDI Interface')
DEVICE2 = 'IAC Driver Bus 1'

api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('gate_mod1', device=DEVICE, channel=8, min_octave=0, base_octave=1, max_octave=10, muted=False)
api.instruments.add('pitch_mod1', device=DEVICE, channel=2, min_octave=0, base_octave=1, max_octave=10, muted=False)

api.instruments.add('setup_inst', device=DEVICE, channel=16, min_octave=0, base_octave=5, max_octave=10, muted=True)
api.instruments.add('drum1_inst', device=DEVICE2, channel=8, min_octave=0, base_octave=0, max_octave=10, muted=False)
#api.instruments.add('lead2_inst', device=DEVICE, channel=2, min_octave=0, base_octave=0, max_octave=10, muted=False)
#api.instruments.add('drum2_inst', device=DEVICE, channel=7, min_octave=0, base_octave=0, max_octave=10, muted=False)
#api.instruments.add('drum3_inst', device=DEVICE, channel=6, min_octave=0, base_octave=0, max_octave=10, muted=False)

# setup tracks
api.tracks.add(name='setup', instrument='setup_inst', muted=True)
api.tracks.add(name='lead', instrument='lead_inst', muted=False)
api.tracks.add(name='gate_mod1', instrument='gate_mod1', muted=False)
api.tracks.add(name='pitch_mod1', instrument='pitch_mod1', muted=False)
#api.tracks.add(name='drum1', instrument='drum1_inst', muted=False)
#api.tracks.add(name='lead2', instrument='lead2_inst', muted=False)
##api.tracks.add(name='drum2', instrument='drum2_inst', muted=False)
#api.tracks.add(name='drum3', instrument='drum3_inst', muted=False)

# setup scales
api.scales.add(name='intro', note='C', octave=0, scale_type='minor')
#api.scales.add(name='main', note='F', octave=0, scale_type='major')
#api.scales.add(name='main2', note='A', octave=1, scale_type='major')

api.patterns.add(name='vars', slots=[
    '1 $w=250 $x=0 $y=0 $z=1',
    '1 $w=100 $x=1 $y=0 $z=1',
])

api.patterns.add(name='L0', slots=[1,6,5,4,2,3,4,'-',5,6,5,4,3,2,3,1,'-','-'], rate=1)
#api.patterns.add(name='GM1a', slots=[ 'C4', '', '', '', '',   '', '', '', '',  '',  '', '', '',  '',  '', '' ], rate=1)
#api.patterns.add(name='GM1b', slots=[ 'C4', '', '', '', 'C4', '', '', '', 'C4', '', '', '', 'C4', '', '', '' ], rate=1)

api.patterns.add(name='pitch_mod_off', slots=['C0'], rate=1)
api.patterns.add(name='pitch_mod_on', slots=['C4'], rate=1)
api.patterns.add(name='pitch_mod_hi', slots=['F8'], rate=1)

# setup transforms
api.transforms.add(name='hop', slots=['O-1','O+1'], divide=1)

# setup scenes
api.scenes.add(name='scene_0', scale='intro', auto_advance=True)
api.scenes.add(name='scene_1', scale='intro', auto_advance=True)
api.scenes.add(name='scene_END', scale='intro', auto_advance=True)

# setup clips
# lead plays in
#api.clips.add(name='1', scene='scene_0', track='setup', patterns=['vars'], repeat=None, rate=0.0625)
api.clips.add(name='2', scene='scene_0', track='lead', patterns=['L0'], transforms=[], repeat=None, auto_scene_advance=True)
#api.clips.add(name='3', scene='scene_0', track='gate_mod1', patterns=['GM1b'], transforms=[], repeat=None)
#api.clips.add(name='4', scene='scene_0', track='pitch_mod1', patterns=['pitch_mod_off'], transforms=[], repeat=None)

api.player.loop('scene_0')

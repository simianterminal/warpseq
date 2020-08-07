# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------

# https://soundcloud.com/mpdehaan/probability-of-monster
# as recorded: 3x Arturia ObXA synth instances + Lexicon UAD Reverb

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=112)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver Bus 1')

api.instruments.add('guide', device=DEVICE, channel=4, min_octave=0, base_octave=4, max_octave=10, muted=True)
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10, muted=False)
api.instruments.add('bass_inst', device=DEVICE, channel=2, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('lead2_inst', device=DEVICE, channel=3, min_octave=0, base_octave=4, max_octave=10)

# setup tracks
api.tracks.add(name='guide', instrument='guide')
api.tracks.add(name='lead', instrument='lead_inst')
api.tracks.add(name='bass', instrument='bass_inst')
api.tracks.add(name='lead2', instrument='lead2_inst')

# setup scales
api.scales.add(name='intro', note='Eb', octave=0, scale_type='natural_minor')
api.scales.add(name='mid', note='Eb', octave=0, scale_type='melodic_minor_desc')

# setup patterns
api.patterns.add(name='a', slots=[1,4,5,1,6,5,2,3,4,5,1])
api.patterns.add(name='b', slots=['7', '6', '5', '4', '3', '2', '1' ])
api.patterns.add(name='a2', slots=[9,5,4,2,8,5,4,2,4,5,1])
api.patterns.add(name='b2', slots=[8,6,5,2,5,4,3,2,5,4,3,2,1])
api.patterns.add(name='a3', slots=[4,4,5,6,1,5,2,4,3,5,1])
api.patterns.add(name='b3', slots=[ '7', '6', '4', '5', '2', '3', '1' ])

api.patterns.add(name='copy', slots = ['1 T=guide'])
api.patterns.add(name='copy_to_power_chords', slots = ['1 T=guide ch=power'])
api.patterns.add(name='even', slots = ['1 T=guide','','1 T=guide', '', '5', ''])

# setup transforms
api.transforms.add(name='riff', slots=['1', 'S+1', 'S+4', 'S+5'], divide=4)
api.transforms.add(name='octave up', slots=['O+1'], divide=1)

# setup scenes
api.scenes.add(name='scene_1', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_3', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_5', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_7', rate=1, auto_advance=True, scale='mid')
api.scenes.add(name='scene_9', rate=1, auto_advance=True, scale='mid')
api.scenes.add(name='scene_11', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_12', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_13', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_15', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_END', rate=1, auto_advance=True, scale='intro')

# setup clips
api.clips.add(name='s1_guide', scene='scene_1', track='guide', patterns=['a','b','a','b'], repeat=1, rate=0.33, auto_scene_advance=True)
api.clips.add(name='s1_lead', scene='scene_1', track='lead', patterns=['copy_to_power_chords'], rate=0.33, repeat=None)

api.clips.add(name='s3_guide', scene='scene_3', track='guide', patterns=['a','b','a','b'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3_bass', scene='scene_3', track='lead', patterns=['even'], repeat=None)

api.clips.add(name='s5_guide', scene='scene_5', track='guide', patterns=['a','b','a','b'], repeat=1, rate=0.5, auto_scene_advance=True)
api.clips.add(name='s5_lead', scene='scene_5', track='lead', patterns=['copy'], transforms=['octave up'], rate=0.5, repeat=None)
api.clips.add(name='s5_bass', scene='scene_5', track='bass', patterns=['copy'], rate=1, repeat=None)
api.clips.add(name='s5_lead2', scene='scene_5', track='lead2', patterns=['copy'], transforms=['riff','octave up'], rate=1, repeat=None)

api.clips.add(name='s7_guide', scene='scene_7', track='guide', patterns=['a','b','a','b'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s7_bass', scene='scene_7', track='lead', patterns=['even'], repeat=None)

api.clips.add(name='s9_guide', scene='scene_9', track='guide', patterns=['a2','b2','a2','b2'], repeat=1, rate=0.5, auto_scene_advance=True)
api.clips.add(name='s9_lead', scene='scene_9', track='lead', patterns=['copy'], transforms=['octave up'], rate=0.5, repeat=None)
api.clips.add(name='s9_bass', scene='scene_9', track='bass', patterns=['copy'], rate=1, repeat=None)
api.clips.add(name='s9_lead2', scene='scene_9', track='lead2', patterns=['copy'], transforms=['riff','octave up'], rate=1, repeat=None)

api.clips.add(name='s11_lead', scene='scene_11', track='lead', patterns=['a3','b3'], transforms=['octave_up'], rate=0.5, repeat=1)

api.clips.add(name='s13_guide', scene='scene_13', track='guide', patterns=['a','b','a','b'], rate=0.33, repeat=1, auto_scene_advance=True)
api.clips.add(name='s13_bass', scene='scene_13', track='lead', patterns=['even'], rate=0.33, repeat=None)

api.clips.add(name='s15_guide', scene='scene_15', track='guide', patterns=['a','b','a','b'], repeat=1, rate=0.33, auto_scene_advance=True)
api.clips.add(name='s15_lead', scene='scene_15', track='lead', patterns=['copy_to_power_chords'], rate=0.33, repeat=None)

api.player.loop('scene_1')

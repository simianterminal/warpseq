# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how to enter scale notes that change automatically
# as the scales change.
#
# scales can be defined on the song and overridden per scene
# (for easy mid-song key changes) or even per clip - where they
# can be expressed in a list, and will rotate as each pattern
# in the clip advances.
#
# try changing the patterns and scales

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=120)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10)

# setup tracks
api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# setup scales
print("available scale types:")
print(api.scales.scale_types())
api.scales.add(name='C-major', note='C', octave=0, scale_type='major')
api.scales.add(name='C-minor', note='C', octave=0, scale_type='natural_minor')
api.scales.add(name='G-major', note='G', octave=0, scale_type='major')
api.scales.add(name='G-minor', note='G', octave=0, scale_type='natural_minor')
api.scales.add(name='Bb-mixolydian', note='Bb', octave=0, scale_type='mixolydian')
api.scales.add(name='A-akebono', note='A', octave=0, scale_type='akebono')
api.scales.add(name='F-user1', note='F', octave=0, slots = [1, 'b2', 'b3', '5', 6 ])
api.scales.add(name='F-user2', note='F', octave=1, slots = [1, 'b2', 'b3', '5', 6 ])

# setup patterns
api.patterns.add(name='up', slots=['1','2','3','4','5','6','7','8'])
api.patterns.add(name='down', slots=['8','7','6','5','4','3','2','1'])

# setup scenes
api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_4', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_5', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_6', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_7', rate=1, auto_advance=True)
api.scenes.add(name='scene_8', rate=1, auto_advance=True)

# setup clips
api.clips.add(name='s1c', scene='scene_1', track='lead', scales=['C-major'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s2c', scene='scene_2', track='lead', scales=['C-minor'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3c', scene='scene_3', track='lead', scales=['G-major'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s4c', scene='scene_4', track='lead', scales=['G-minor'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s5c', scene='scene_5', track='lead', scales=['Bb-mixolydian'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s6c', scene='scene_6', track='lead', scales=['A-akebono'], patterns=['up'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s7c', scene='scene_7', track='lead', scales=['C-major','G-minor','A-akebono'], patterns=['down'], repeat=3, auto_scene_advance=True)
api.clips.add(name='s8c', scene='scene_8', track='lead', scales=['F-user1', 'F-user2'], patterns=['down'], repeat=2, auto_scene_advance=True)

# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_1')
# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------

# this demo shows some other clip parameters, including
# scale changes and puts together some concepts mentioned
# in earlier demos

from warpseq.api.public import Api as WarpApi
from warpseq.api import demo

# setup API and song
api = WarpApi()
api.song.edit(tempo=160)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10)

# setup tracks
api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# setup scales
api.scales.add(name='G-phyrigian', note='G', octave=0, scale_type='phyrigian')
api.scales.add(name='F-mixolydian', note='F', octave=0, scale_type='mixolydian')
api.scales.add(name='magic', note='C', octave=0, slots=[1,4,5])

# setup patterns
api.patterns.add(name='up', slots=['1', '2', '3', '4', '5', '6', '7', '8' ])
api.patterns.add(name='down', slots = [ '8', '7', '6', '5', '4', '3', '2', '1'])

# setup scenes
api.scenes.add(name='scene_1', rate=1, auto_advance=False)
api.scenes.add(name='scene_2', rate=1, auto_advance=False)

# setup transforms
api.transforms.add(name='stutter', slots=['1', 'x', '1', '1', '1', 'x'], divide=3)
api.transforms.add(name='chance octave jump', slots=['1','1','1','O=0,0,0,1,2'], divide=3)
api.transforms.add(name='octave up', slots=['O+1'], divide=1)
api.transforms.add(name='octave hop', slots=['1', 'O+1'], divide=1)
api.transforms.add(name='every third note up 5th', slots=['1','1','S+5'], divide=1)


# setup clips
api.clips.add(name='kitchen sink',
              scene='scene_1',
              track='lead',
              scales=['G-phyrigian', 'F-mixolydian', 'magic'],
              patterns=['up', 'down'],
              transforms=[['chance octave jump'],['octave up', 'stutter'],['octave hop', 'every third note up 5th']],
              tempo_shifts = [0, 5, 10, 15, 20, 25, 30 ],
              repeat=20,
              next_clip='ending')

api.clips.add(name='ending',
              scene='scene_2',
              track='lead',
              scales=['magic'],
              patterns=['down'],
              repeat=2,
              rate=0.25)

# play
api.player.play_scene('scene_1')
for x in range(0,128000):
    api.player.advance(5)
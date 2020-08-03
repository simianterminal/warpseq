# --------------------------------------------------------------
# fields - a warpseq experiment
# (C) John Mitchell aka midcentury modular <midcenturymodular@gmail.com>, 2020
# find my music at midcenturymodular.bandcamp.com
# --------------------------------------------------------------
#
# based on examples/api/04_transforms.py, experiments with slight differences in layers
#
# you can listen to the track at https://soundcloud.com/midcentury/fields
#
# the sounds are sample-based instruments (wasp for the higher notes, 2600 for the two
# bass-y lines, and the vp330 for the high swells). I processed the sounds with ableton's
# echo and glue compressor, valhalla's plate and vintage verbs), and fabfilter pro-q 3.
# Finally, I bounced the mix to my teac 22-4 1/4" reel to reel.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi

api = WarpApi()
api.song.edit(tempo=100)

DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')

api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=5, max_octave=10)
api.instruments.add('lead2_inst', device=DEVICE, channel=2, min_octave=0, base_octave=5, max_octave=10)
api.instruments.add('bass_inst', device=DEVICE, channel=3, min_octave=0, base_octave=3, max_octave=10)
api.instruments.add('bass2_inst', device=DEVICE, channel=4, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('high_inst', device=DEVICE, channel=5, min_octave=0, base_octave=7, max_octave=10)

api.tracks.add(name='lead', instrument='lead_inst', muted=False)
api.tracks.add(name='lead2', instrument='lead2_inst', muted=False)
api.tracks.add(name='bass', instrument='bass_inst', muted=False)
api.tracks.add(name='bass2', instrument='bass2_inst', muted=False)
api.tracks.add(name='high', instrument='high_inst', muted=False)

api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

api.patterns.add(name='basic', slots=['1', '4', '5'])

api.transforms.add(name='transform1', slots=['S+2,2,2,2,2,4,7 p=0.4 x p=0.5 O+1'], divide=1)
api.transforms.add(name='transform2', slots=['S+4,4,4,4,4,5,3 p=0.4 x p=0.5 O+1'], divide=1)
api.transforms.add(name='transform3', slots=['S+0', 'S+3', 'S+0', 'S+3', 'S+4', 'S+3', 'S+5', 'S+3'], divide=1)
api.transforms.add(name='transform4', slots=['x', 'S+0', 'S+4', 'S+0', 'S+4', 'S+3', 'S+3', 'S+5', 'S+3'], divide=1)
api.transforms.add(name='transform5', slots=['x', 'x', 'x', 'x', 'x', 'x', 'x', '1 p=0.5 x'], divide=1)

maxLength = 128
for i in range(1, maxLength):
    api.scenes.add(name='scene_' + str(i), rate=0.5, auto_advance=True)
    api.clips.add(name="voice1_" + str(i), scene='scene_' + str(i), track='lead', scales=['C-major'], patterns=['basic'], transforms=['transform' + str((i % 2) + 1)], repeat=2,  auto_scene_advance=False if i == maxLength else True)
    api.clips.add(name="voice2_" + str(i), scene='scene_' + str(i), track='lead2', scales=['C-major'], patterns=['basic'], transforms=['transform' + str((i % 2) + 1)], repeat=2,  auto_scene_advance=False if i == maxLength else True)
    api.clips.add(name="voice3_" + str(i), scene='scene_' + str(i), track='bass', scales=['C-major'], patterns=['basic'], transforms=['transform3'], repeat=2,  auto_scene_advance=False if i == maxLength else True)
    api.clips.add(name="voice4_" + str(i), scene='scene_' + str(i), track='bass2', scales=['C-major'], patterns=['basic'], transforms=['transform4'], repeat=2,  auto_scene_advance=False if i == maxLength else True)
    api.clips.add(name="voice5_" + str(i), scene='scene_' + str(i), track='high', scales=['C-major'], patterns=['basic'], transforms=['transform5'], repeat=2,  auto_scene_advance=False if i == maxLength else True)

# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_1')

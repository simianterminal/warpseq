# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
# What this demos shows:
# * how to use a silent (or not silent!) guide information
#   track to supply pitch values to other tracks, which
#   then use patterns/transforms to automatically generate
#   chords and a bassline
# --------------------------------------------------------------
# Learning objectives:
# * understand how to write note grab events
# * refresh your memory of mod expressions
# -------------------------------------------------------------
# Things to try:
# * change the underlying melody track, how do the other tracks
#   change?
# * can you add some interesting transforms?
# -------------------------------------------------------------

from warpseq.api.public import Api as WarpApi
from warpseq.api import demo

# setup API and song
api = WarpApi()
api.song.edit(tempo=160)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')

api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=6, max_octave=10)
api.instruments.add('chord_inst', device=DEVICE, channel=2, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('bass_inst', device=DEVICE, channel=3, min_octave=0, base_octave=3, max_octave=10)

# setup tracks
api.tracks.add(name='guide', instrument='lead_inst', muted=True)
api.tracks.add(name='lead', instrument='lead_inst')
api.tracks.add(name='chord', instrument='chord_inst')
api.tracks.add(name='bass', instrument='bass_inst')

# setup scales
api.scales.add(name='Eb-lydian', note='Eb', octave=0, scale_type='lydian')
api.scales.add(name='B-minor', note='B', octave=0, scale_type='natural_minor')

# setup patterns
api.patterns.add(name='a', slots=['1', '2', '1', '3', '', '1', '3', '4', '5', '9', '' ])
api.patterns.add(name='b', slots = [ '1', '5', '1', '5', '2' ])

api.patterns.add(name='lead1', slots = ['1 T=guide'])
api.patterns.add(name='chord1', slots = ['1 T=guide ch=major','-', '-', '-'])
api.patterns.add(name='bass1', slots = ['1 T=guide', '1 T=guide S+1', '1 T=guide', '1 T=guide S-1'])
api.patterns.add(name='lead2', slots = ['1 T=guide', '1 T=guide O+1'])
api.patterns.add(name='chord2', slots = ['1 T=guide ch=major','-', '1 T=guide ch=major', '-'])
api.patterns.add(name='bass2', slots = ['1 T=guide', '1 T=guide S+1', '1 T=guide', '1 T=guide S-1', '1 T=guide S-1'])


# setup scenes
api.scenes.add(name='scene_1', rate=1, auto_advance=False, scale='Eb-lydian')
api.scenes.add(name='scene_2', rate=1, auto_advance=False, scale='B-minor')

api.clips.add(name='s_guide1', scene='scene_1', track='guide', patterns=['a','b','a','b'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s_lead1', scene='scene_1', track='lead', patterns=['lead1'])
api.clips.add(name='s_chord1', scene='scene_1', track='chord', patterns=['chord1'], octave_shifts=[0,1])
api.clips.add(name='s_bass1', scene='scene_1', track='bass', patterns=['bass1'])

api.clips.add(name='s_guide1', scene='scene_2', track='guide', patterns=['a','a','b','b'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s_lead2', scene='scene_2', track='lead', patterns=['lead2'], octave_shifts=[0,1])
api.clips.add(name='s_chord2', scene='scene_2', track='chord', patterns=['chord2'])
api.clips.add(name='s_bass2', scene='scene_2', track='bass', patterns=['bass2'])

# play
api.player.play_scene('scene_1')
for x in range(0,128000):
    api.player.advance(5)
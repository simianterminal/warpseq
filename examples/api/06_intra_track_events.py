# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demos hows how instruments can pull notes selectively
# from a silent guide track, which can be useful to rapidly
# construct large movements without having to sequence notes
# for every single instrument

from warpseq.api.public import Api as WarpApi
from warpseq.api import demo

# setup API and song
api = WarpApi()
api.song.edit(tempo=160)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')

api.instruments.add('guide', device=DEVICE, channel=4, min_octave=0, base_octave=4, max_octave=10, muted=True)
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('chord_inst', device=DEVICE, channel=2, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('bass_inst', device=DEVICE, channel=3, min_octave=0, base_octave=4, max_octave=10)

# setup tracks
api.tracks.add(name='guide', instrument='guide')
api.tracks.add(name='lead', instrument='lead_inst')
api.tracks.add(name='chord', instrument='chord_inst')
api.tracks.add(name='bass', instrument='bass_inst')

# setup scales
api.scales.add(name='Eb-lydian', note='Eb', octave=0, scale_type='lydian')
api.scales.add(name='B-minor', note='B', octave=0, scale_type='natural_minor')

# setup patterns
api.patterns.add(name='a', slots=['1', '2', '3', '4', '5', '6', '7', '8' ])
api.patterns.add(name='b', slots = [ '7', '6', '5', '4', '3', '2', '1' ])
api.patterns.add(name='parrot', slots = ['1 T=guide'])
api.patterns.add(name='stylish parrot', slots = ['1 T=guide ch=major O+1', '1 T=guide', '1 T=guide', '1 T=guide'])
api.patterns.add(name='even', slots = ['1 T=guide','','1 T=guide', '', '5', ''])
api.patterns.add(name='odd', slots = ['','1 T=guide','','1 T=guide', '', '5' ])
api.patterns.add(name='chords', slots = ['1 T=guide ch=major', '-', '-', '-'])

# setup transforms
api.transforms.add(name='bassline', slots=['1', 'S+1', 'S+4', 'S+5'], divide=4)

# setup scenes
api.scenes.add(name='scene_1', rate=1, auto_advance=True, scale='Eb-lydian')
api.scenes.add(name='scene_2', rate=1, auto_advance=True, scale='B-minor')
api.scenes.add(name='scene_3', rate=1, auto_advance=True, scale='B-minor')
api.scenes.add(name='scene_4', rate=1, auto_advance=True, scale='B-minor')
api.scenes.add(name='scene_5', rate=1, auto_advance=True, scale='Eb-lydian')

# setup clips
# the lead just plays whatever the guide track is silently playing
api.clips.add(name='s1_guide', scene='scene_1', track='guide', patterns=['a','b','a','b'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s1_lead', scene='scene_1', track='lead', patterns=['parrot'], repeat=None) # repeat=None means infinite

# now the bass track plays the guide track instead of the lead
api.clips.add(name='s2_guide', scene='scene_2', track='guide', patterns=['a','b','a','b'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s2_bass', scene='scene_2', track='bass', patterns=['parrot'], repeat=None)

# now the lead and bass track alternate notes from the guide track and some things they have decided for themselves.
# not all slots have to grab the value from the guide track
api.clips.add(name='s3_guide', scene='scene_3', track='guide', patterns=['a','b','a','b'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3_bass', scene='scene_3', track='lead', patterns=['even'], repeat=None) # repeat=None means infinite
api.clips.add(name='s3_lead', scene='scene_3', track='bass', patterns=['odd'], repeat=None)

# now the lead track slowly plays a chord based on the silent guide track while the bass track forms a bassline around it.
api.clips.add(name='s4_guide', scene='scene_4', track='guide', patterns=['a','b','a','b'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s4_bass', scene='scene_4', track='lead', patterns=['chords'], rate=0.5, repeat=None) # repeat=None means infinite
api.clips.add(name='s4_lead', scene='scene_4', track='bass', patterns=['parrot'], rate=2, transforms=['bassline'], repeat=None)

# play
api.player.play_scene('scene_1')
for x in range(0,128000):
    api.player.advance(2)
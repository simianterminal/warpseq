# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demos hows how instruments can pull notes selectively
# from a silent guide track, which can be useful to rapidly
# construct large movements without having to sequence notes
# for every single instrument. Basically one instrument can
# "listen" to what is playing on another track, copy the note,
# and then use it to build chords, transpose up or down, or apply
# an arpeggiator.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=120)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver Bus 1')

api.instruments.add('guide', device=DEVICE, channel=4, min_octave=0, base_octave=4, max_octave=10, muted=True)
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10, muted=False)
#api.instruments.add('chord_inst', device=DEVICE, channel=2, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('bass_inst', device=DEVICE, channel=2, min_octave=0, base_octave=4, max_octave=10)

# setup tracks
api.tracks.add(name='guide', instrument='guide')
api.tracks.add(name='lead', instrument='lead_inst')
#api.tracks.add(name='chord', instrument='chord_inst')
api.tracks.add(name='bass', instrument='bass_inst')

# setup scales
api.scales.add(name='intro', note='Eb', octave=0, scale_type='natural_minor')

# setup patterns
api.patterns.add(name='a', slots=[1,2,3]) #slots=[1,4,5,1,6,5,2,3,4,5,1])
api.patterns.add(name='b', slots = [ '7', '6', '5', '4', '3', '2', '1' ])
api.patterns.add(name='copy', slots = ['1 T=guide'])
api.patterns.add(name='copy_to_power_chords', slots = ['1 T=guide ch=power'])

#api.patterns.add(name='stylish parrot', slots = ['1 T=guide ch=major O+1', '1 T=guide', '1 T=guide', '1 T=guide'])
api.patterns.add(name='even', slots = ['1 T=guide','','1 T=guide', '', '5', ''])
#api.patterns.add(name='odd', slots = ['','1 T=guide','','1 T=guide', '', '5' ])
#api.patterns.add(name='chords', slots = ['1 T=guide ch=major', '-', '-', '-'])

# setup transforms
api.transforms.add(name='bassline', slots=['1', 'S+1', 'S+4', 'S+5'], divide=4)

# setup scenes
api.scenes.add(name='scene_1', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_3', rate=1, auto_advance=True, scale='intro')
api.scenes.add(name='scene_5', rate=1, auto_advance=True, scale='intro')
#api.scenes.add(name='scene_END', rate=1, auto_advance=True, scale='intro')

# setup clips
# the lead just plays whatever the guide track is silently playing
api.clips.add(name='s1_guide', scene='scene_1', track='guide', patterns=['a','b','a','b'], repeat=1, rate=0.5, auto_scene_advance=True)
api.clips.add(name='s1_lead', scene='scene_1', track='lead', patterns=['copy_to_power_chords'], rate=0.5, repeat=None) # repeat=None means infinite

# now the lead and bass track alternate notes from the guide track and some things they have decided for themselves.
# not all slots have to grab the value from the guide track
api.clips.add(name='s3_guide', scene='scene_3', track='guide', patterns=['a','b','a','b'], repeat=1, auto_scene_advance=True)
api.clips.add(name='s3_bass', scene='scene_3', track='lead', patterns=['even'], repeat=None) # repeat=None means infinite

api.clips.add(name='s5_guide', scene='scene_5', track='guide', patterns=['a'], repeat=None, rate=0.5, auto_scene_advance=True)
api.clips.add(name='s5_lead', scene='scene_5', track='lead', patterns=['copy'], rate=0.5, repeat=None) # repeat=None means infinite
api.clips.add(name='s5_bass', scene='scene_5', track='bass', patterns=['copy'], transforms=['bassline'], rate=1, repeat=None)

# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_3')

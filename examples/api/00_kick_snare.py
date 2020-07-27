from warpseq.api.public import Api as WarpApi
from warpseq.api.demo import suggest_device

api = WarpApi()
api.song.edit(tempo=120)

# setup instruments
# - a kick drum on MIDI channel 1
# - a snare drum on MIDI channel 2

DEVICE = suggest_device(api, 'IAC Driver IAC Bus 1b')
api.instruments.add('kick_inst', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('snare_inst', device=DEVICE, channel=2, min_octave=0, base_octave=4, max_octave=10)

# setup tracks
api.tracks.add(name='kick', instrument='kick_inst', muted=False)
api.tracks.add(name='snare', instrument='snare_inst', muted=False)

# setup scales
api.scales.add(name='C-major', note='C', octave=3, scale_type='major')

# setup patterns
api.patterns.add(name='kick_4_4',  slots="C5 - -  - C5 - -  - C5 - -  - C5 - -  -".split())
api.patterns.add(name='snare_4_4', slots="-  - D5 - - -  D5 - -  - D5 - -  - D5 -".split())
api.patterns.add(name='kick_alt',  slots="C5 - C5 - C5 - -  - C5 - -  - C5 - -  -".split())
api.patterns.add(name='snare_alt', slots="-  - D5 - -  - D5 D5 -  D5 D5 - -  D5 D5 -".split())


# setup scenes
api.scenes.add(name='scene_1', scale='C-major', auto_advance=True)
api.scenes.add(name='scene_2', scale='C-major', auto_advance=True)

#
api.clips.add(name='s1k1', scene='scene_1', track='kick', patterns=['kick_4_4'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s1s1', scene='scene_1', track='snare', patterns=['snare_4_4'], repeat=4)
api.clips.add(name='s2k1', scene='scene_2', track='kick', patterns=['kick_alt'], repeat=4, auto_scene_advance=True)
api.clips.add(name='s2s1', scene='scene_2', track='snare', patterns=['snare_alt'], repeat=4)

api.player.play_scene('scene_1')

for x in range(0,64000):
    api.player.advance(2)

api.player.stop()

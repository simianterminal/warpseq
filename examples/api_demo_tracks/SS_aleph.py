# --------------------------------------------------------------
# aleph - a warpseq experiment
# (C) Steve Salevan / Vox Cadre <info@voxcadre.com>, 2020
# Check us out at https://voxcadre.com
# --------------------------------------------------------------
#
# This is a bit of an old VC jam, given a new spin with warpseq.
# Sounds a bit like a cross between Soft Cell and Angelo Badalamenti.
#
# Check it out over here: https://soundcloud.com/voxcadre/aleph
#
# We decided to switch on all the MIDI gear in the studio and see how many notes
# we could get WarpSeq to fire off at it. Turns out, the answer was quite a few!
# We used a Korg ARP 2600, Minimoog Model D, Moog One, Prophet 6 and Behringer
# VC340 alongside a D5 drumkit in Ableton, routed by way of the ARP 2600.
#
# Everything was recorded in Ableton then bounced to SoundCloud.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi


def f(l):
    '''Flattens a list of lists.'''

    return sum(l, [])


def whole(base, count):
    '''Returns a slot followed by a number of held slots.'''

    return [base] + ['-'] * (count - 1)


def rep(base, count):
    '''Repeats a slot by the provided count.'''

    return [base] * count


api = WarpApi()
api.song.edit(tempo=70)

# Base MIDI devices:

ARP_2600 = demo.suggest_device(api, 'ARP 2600 SOUND')
DRUMS = demo.suggest_device(api, 'ARP 2600 MIDI OUT')
MINIMOOG = demo.suggest_device(api, 'mio10 DIN 1')
MOOG_ONE = demo.suggest_device(api, 'Moog One')
PROPHET_6 = demo.suggest_device(api, 'Prophet 6')
VC340 = demo.suggest_device(api, 'Vocoder-VC340')

# Instruments and tracks:

api.instruments.add('arp_skronk_inst', device=ARP_2600, channel=1, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('bass_inst', device=MINIMOOG, channel=1, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('choir_inst', device=VC340, channel=1, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('drums_inst', device=DRUMS, channel=1, min_octave=0, base_octave=2, max_octave=5)
api.instruments.add('ghosts_inst', device=PROPHET_6, channel=1, min_octave=0, base_octave=4, max_octave=10)
api.instruments.add('obstrings_inst', device=MOOG_ONE, channel=1, min_octave=0, base_octave=4, max_octave=10)

api.tracks.add(name='arp_skronk', instrument='arp_skronk_inst', muted=False)
api.tracks.add(name='bass', instrument='bass_inst', muted=False)
api.tracks.add(name='choir', instrument='choir_inst', muted=False)
api.tracks.add(name='choir_harmony', instrument='choir_inst', muted=False)
api.tracks.add(name='choir_harmony_2', instrument='choir_inst', muted=False)
api.tracks.add(name='ghosts', instrument='ghosts_inst', muted=False)
api.tracks.add(name='hihat', instrument='drums_inst', muted=False)
api.tracks.add(name='kick', instrument='drums_inst', muted=False)
api.tracks.add(name='obstrings', instrument='obstrings_inst', muted=False)
api.tracks.add(name='rim', instrument='drums_inst', muted=False)

# Scales:

api.scales.add(name='G-major', note='G', octave=0, scale_type='major')
api.scales.add(name='G-minor', note='G', octave=0, scale_type='minor')
api.scales.add(name='G-minor-hi', note='G', octave=2, scale_type='minor')
api.scales.add(name='G-minor-mid', note='G', octave=1, scale_type='minor')

# Drum patterns:

api.patterns.add(name='kick_16s_chorus', slots=rep("C1", 16))
api.patterns.add(name='kick_16s_verse', slots=rep("C1", 20))
api.patterns.add(name='hihat_16s_verse', slots=rep("F#1", 20))
api.patterns.add(name='rim_jazzy', slots=". C#1 . C#1 . C#1 . C#1 . C#1 . C#1 . C#1 . C#1 . C#1 . C#1".split())

# Chord patterns and leads:

api.patterns.add(name='verse_chords', slots=f([whole('I', 8), whole('V', 8), whole('II', 8), whole('IV', 8)]))
api.patterns.add(name='verse_arp', slots=f([rep('I', 8), rep('V', 8), rep('II', 8), rep('IV', 8)]))

api.patterns.add(name='chorus_chords', slots=f([whole('I', 4), whole('VI', 4), whole('IV', 4), whole('V', 4)]))
api.patterns.add(name='chorus_arp', slots=f([rep('I', 4), rep('VI', 4), rep('IV', 4), rep('V', 4)]))
api.patterns.add(name='chorus_lead', slots=['D1', 'C1', 'B0', 'A0', 'A#1', 'A1', 'G1', 'F1', 'G1', 'F1', 'E1', 'D1', 'A1', 'G1', 'F1', 'E1'])

api.patterns.add(name='bridge_chords', slots=f([whole('I', 8), whole('vi', 8), whole('IV', 8), whole('iii', 4), whole('V', 4)]))

# Transforms:

api.transforms.add(name='arp3', slots=['1'], divide=3)
api.transforms.add(name='fifth_harmony', slots=['S+5'])
api.transforms.add(name='octave_up', slots=['O+1'])
api.transforms.add(name='whole_root', slots=['1'])

# Song structure:

api.scenes.add(name='intro_a', rate=0.5, auto_advance=True)
api.scenes.add(name='intro_b', rate=0.5, auto_advance=True)
api.scenes.add(name='verse_a', rate=0.5, auto_advance=True)
api.scenes.add(name='chorus_1a', rate=0.5, auto_advance=True)
api.scenes.add(name='chorus_1b', rate=0.5, auto_advance=True)
api.scenes.add(name='chorus_1c', rate=0.5, auto_advance=True)
api.scenes.add(name='bridge', rate=0.5, auto_advance=True)
api.scenes.add(name='verse_b', rate=0.5, auto_advance=True)
api.scenes.add(name='chorus_2a', rate=0.5, auto_advance=True)
api.scenes.add(name='chorus_2b', rate=0.5, auto_advance=True)
api.scenes.add(name='chorus_2c', rate=0.5, auto_advance=True)
api.scenes.add(name='outro', rate=0.5, auto_advance=True)

# Clips:

# Intro A:
api.clips.add(name='strings_intro_a', scene='intro_a', track='obstrings', scales=['G-minor'], patterns=['verse_chords'], repeat=2, auto_scene_advance=True)
api.clips.add(name='bassline_intro_a', scene='intro_a', track='bass', scales=['G-minor'], patterns=['verse_chords'], transforms=['whole_root'], repeat=2, auto_scene_advance=True)
api.clips.add(name='skronk_intro_a', scene='intro_a', track='arp_skronk', scales=['G-minor-hi'], patterns=['verse_chords'], transforms=['whole_root'], repeat=2, auto_scene_advance=True)

# Intro B:
api.clips.add(name='strings_intro_b', scene='intro_b', track='obstrings', scales=['G-minor'], patterns=['verse_chords'], repeat=1, auto_scene_advance=True)
api.clips.add(name='bassline_intro_b', scene='intro_b', track='bass', scales=['G-minor'], patterns=['verse_chords'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='skronk_intro_b', scene='intro_b', track='arp_skronk', scales=['G-minor-hi'], patterns=['verse_arp'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='kick_intro_b', scene='intro_b', track='kick', patterns=['kick_16s_verse'], repeat=2, auto_scene_advance=False)
api.clips.add(name='rim_intro_b', scene='intro_b', track='rim', patterns=['rim_jazzy'], repeat=2, auto_scene_advance=False)

# Verse A:
api.clips.add(name='strings_verse_a', scene='verse_a', track='obstrings', scales=['G-minor'], patterns=['verse_chords'], repeat=2, auto_scene_advance=True)
api.clips.add(name='bassline_verse_a', scene='verse_a', track='bass', scales=['G-minor'], patterns=['verse_chords'], transforms=['whole_root'], repeat=2, auto_scene_advance=True)
api.clips.add(name='skronk_verse_a', scene='verse_a', track='arp_skronk', scales=['G-minor-hi'], patterns=['verse_arp'], transforms=['arp3'], repeat=2, auto_scene_advance=True)
api.clips.add(name='kick_verse_a', scene='verse_a', track='kick', patterns=['kick_16s_verse'], repeat=4, auto_scene_advance=False)
api.clips.add(name='hihat_verse_a', scene='verse_a', track='hihat', patterns=['hihat_16s_verse'], repeat=4, auto_scene_advance=False)
api.clips.add(name='rim_verse_a', scene='verse_a', track='rim', patterns=['rim_jazzy'], repeat=4, auto_scene_advance=False)

# Chorus 1A:
api.clips.add(name='strings_chorus_1a', scene='chorus_1a', track='ghosts', scales=['G-minor'], patterns=['chorus_chords'], repeat=1, auto_scene_advance=True)
api.clips.add(name='bassline_chorus_1a', scene='chorus_1a', track='bass', scales=['G-minor'], patterns=['chorus_chords'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='skronk_chorus_1a', scene='chorus_1a', track='arp_skronk', scales=['G-minor-mid'], patterns=['chorus_arp'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='kick_chorus_1a', scene='chorus_1a', track='kick', patterns=['kick_16s_chorus'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_chorus_1a', scene='chorus_1a', track='choir', patterns=['chorus_lead'], repeat=1, auto_scene_advance=False)

# Chorus 1B:
api.clips.add(name='strings_chorus_1b', scene='chorus_1b', track='ghosts', scales=['G-minor'], patterns=['chorus_chords'], repeat=1, auto_scene_advance=True)
api.clips.add(name='bassline_chorus_1b', scene='chorus_1b', track='bass', scales=['G-minor'], patterns=['chorus_chords'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='skronk_chorus_1b', scene='chorus_1b', track='arp_skronk', scales=['G-minor-mid'], patterns=['chorus_arp'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='kick_chorus_1b', scene='chorus_1b', track='kick', patterns=['kick_16s_chorus'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_chorus_1b', scene='chorus_1b', track='choir', patterns=['chorus_lead'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_chorus_1b', scene='chorus_1b', track='choir_harmony', patterns=['chorus_lead'], transforms=['fifth_harmony'], repeat=1, auto_scene_advance=False)

# Chorus 1C:
api.clips.add(name='strings_chorus_1c', scene='chorus_1c', track='ghosts', scales=['G-minor'], patterns=['chorus_chords'], auto_scene_advance=True, repeat=1)
api.clips.add(name='bassline_chorus_1c', scene='chorus_1c', track='bass', scales=['G-minor'], patterns=['chorus_chords'], transforms=['whole_root'], auto_scene_advance=True, repeat=1)
api.clips.add(name='skronk_chorus_1c', scene='chorus_1c', track='arp_skronk', scales=['G-minor-mid'], patterns=['chorus_arp'], transforms=['whole_root'], auto_scene_advance=True, repeat=1)
api.clips.add(name='kick_chorus_1c', scene='chorus_1c', track='kick', patterns=['kick_16s_chorus'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_chorus_1c', scene='chorus_1c', track='choir', patterns=['chorus_lead'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_chorus_1c', scene='chorus_1c', track='choir_harmony', patterns=['chorus_lead'], transforms=['fifth_harmony'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_2_chorus_1c', scene='chorus_1c', track='choir_harmony_2', patterns=['chorus_lead'], transforms=['octave_up'], repeat=1, auto_scene_advance=False)

# Bridge:
api.clips.add(name='strings_bridge', scene='bridge', track='ghosts', scales=['G-major'], patterns=['bridge_chords'], repeat=2, auto_scene_advance=True)
api.clips.add(name='choir_bridge', scene='bridge', track='choir', scales=['G-major'], patterns=['bridge_chords'], repeat=2, auto_scene_advance=False)
api.clips.add(name='bassline_bridge', scene='bridge', track='bass', scales=['G-major'], patterns=['bridge_chords'], transforms=['whole_root'], repeat=2, auto_scene_advance=True)
api.clips.add(name='kick_bridge', scene='bridge', track='kick', patterns=['kick_16s_verse'], repeat=4, auto_scene_advance=False)
api.clips.add(name='rim_bridge', scene='intro_b', track='rim', patterns=['rim_jazzy'], repeat=4, auto_scene_advance=False)

# Verse B:
api.clips.add(name='strings_verse_b', scene='verse_b', track='obstrings', scales=['G-minor'], patterns=['verse_chords'], repeat=2, auto_scene_advance=True)
api.clips.add(name='bassline_verse_b', scene='verse_b', track='bass', scales=['G-minor'], patterns=['verse_chords'], transforms=['whole_root'], repeat=2, auto_scene_advance=True)
api.clips.add(name='skronk_verse_b', scene='verse_b', track='arp_skronk', scales=['G-minor-hi'], patterns=['verse_arp'], transforms=['arp3'], repeat=2, auto_scene_advance=True)
api.clips.add(name='kick_verse_b', scene='verse_b', track='kick', patterns=['kick_16s_verse'], repeat=4, auto_scene_advance=False)
api.clips.add(name='hihat_verse_b', scene='verse_b', track='hihat', patterns=['hihat_16s_verse'], repeat=4, auto_scene_advance=False)
api.clips.add(name='rim_verse_b', scene='verse_b', track='rim', patterns=['rim_jazzy'], repeat=4, auto_scene_advance=False)

# Chorus 2A:
api.clips.add(name='strings_chorus_2a', scene='chorus_2a', track='ghosts', scales=['G-minor'], patterns=['chorus_chords'], repeat=1, auto_scene_advance=True)
api.clips.add(name='bassline_chorus_2a', scene='chorus_2a', track='bass', scales=['G-minor'], patterns=['chorus_chords'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='skronk_chorus_2a', scene='chorus_2a', track='arp_skronk', scales=['G-minor-mid'], patterns=['chorus_arp'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='kick_chorus_2a', scene='chorus_2a', track='kick', patterns=['kick_16s_chorus'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_chorus_2a', scene='chorus_2a', track='choir', patterns=['chorus_lead'], repeat=1, auto_scene_advance=False)

# Chorus 2B:
api.clips.add(name='strings_chorus_2b', scene='chorus_2b', track='ghosts', scales=['G-minor'], patterns=['chorus_chords'], repeat=1, auto_scene_advance=True)
api.clips.add(name='bassline_chorus_2b', scene='chorus_2b', track='bass', scales=['G-minor'], patterns=['chorus_chords'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='skronk_chorus_2b', scene='chorus_2b', track='arp_skronk', scales=['G-minor-mid'], patterns=['chorus_arp'], transforms=['whole_root'], repeat=1, auto_scene_advance=True)
api.clips.add(name='kick_chorus_2b', scene='chorus_2b', track='kick', patterns=['kick_16s_chorus'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_chorus_2b', scene='chorus_2b', track='choir', patterns=['chorus_lead'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_chorus_2b', scene='chorus_2b', track='choir_harmony', patterns=['chorus_lead'], transforms=['fifth_harmony'], repeat=1, auto_scene_advance=False)

# Chorus 2C:
api.clips.add(name='strings_chorus_2c', scene='chorus_2c', track='ghosts', scales=['G-minor'], patterns=['chorus_chords'], auto_scene_advance=True, repeat=1)
api.clips.add(name='bassline_chorus_2c', scene='chorus_2c', track='bass', scales=['G-minor'], patterns=['chorus_chords'], transforms=['whole_root'], auto_scene_advance=True, repeat=1)
api.clips.add(name='skronk_chorus_2c', scene='chorus_2c', track='arp_skronk', scales=['G-minor-mid'], patterns=['chorus_arp'], transforms=['whole_root'], auto_scene_advance=True, repeat=1)
api.clips.add(name='kick_chorus_2c', scene='chorus_2c', track='kick', patterns=['kick_16s_chorus'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_chorus_2c', scene='chorus_2c', track='choir', patterns=['chorus_lead'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_chorus_2c', scene='chorus_2c', track='choir_harmony', patterns=['chorus_lead'], transforms=['fifth_harmony'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_2_chorus_2c', scene='chorus_2c', track='choir_harmony_2', patterns=['chorus_lead'], transforms=['octave_up'], repeat=1, auto_scene_advance=False)

# Outro:
api.clips.add(name='strings_outro', scene='outro', track='ghosts', scales=['G-minor'], patterns=['chorus_chords'], auto_scene_advance=True, repeat=1)
api.clips.add(name='bassline_outro', scene='outro', track='bass', scales=['G-minor'], patterns=['chorus_chords'], transforms=['whole_root'], auto_scene_advance=True, repeat=1)
api.clips.add(name='skronk_outro', scene='outro', track='arp_skronk', scales=['G-minor-mid'], patterns=['chorus_arp'], transforms=['whole_root'], auto_scene_advance=True, repeat=1)
api.clips.add(name='kick_outro', scene='outro', track='kick', patterns=['kick_16s_chorus'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_outro', scene='outro', track='choir', patterns=['chorus_lead'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_outro', scene='outro', track='choir_harmony', patterns=['chorus_lead'], transforms=['fifth_harmony'], repeat=1, auto_scene_advance=False)
api.clips.add(name='choir_harmony_2_outro', scene='outro', track='choir_harmony_2', patterns=['chorus_lead'], transforms=['octave_up'], repeat=1, auto_scene_advance=False)

# Starts it at the top!
api.player.loop('intro_a')

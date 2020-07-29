# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how transforms work (see docs!) and how
# to build a simple arpeggiator, as well as other MIDI effects.


from warpseq.api.public import Api as WarpApi
from warpseq.api import demo

# setup API and song
api = WarpApi()
api.song.edit(tempo=100)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=4, max_octave=10)

# setup tracks
api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# setup scales
api.scales.add(name='C-major', note='C', octave=0, scale_type='major')
api.scales.add(name='C-minor', note='C', octave=0, scale_type='natural_minor')

# setup patterns
api.patterns.add(name='basic', slots=['1', '2', '3', '4', '5', '6', '7', '8' ])
api.patterns.add(name='chords', slots=['I', 'IV', 'VI', 'VI'])


# setup scenes
api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_4', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_5', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_6', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_7', rate=0.5, auto_advance=True)

# setup transforms
api.transforms.add(name='basic arp', slots=['1'], divide=3)
api.transforms.add(name='octave arp', slots=['1','1','1','O+1','O+1','O+1'], divide=6)
api.transforms.add(name='velocity arp', slots=['1 v=120','1 v=100','1 v=80'], divide=3)
api.transforms.add(name='midi cc arp', slots=['1 cc1=80', '1 cc1=100', '1 cc1=20:100'], divide=3)
api.transforms.add(name='bassline', slots=['1','S+4','S+5','S+2','S+4','S+5','1'], divide=3)
api.transforms.add(name='octave ramp', slots=['1','O+1','O+2'], divide=1)
api.transforms.add(name='stutter', slots=['1','x','1','x','1','p=0.5 x'], divide=6)

# setup clips
api.clips.add(name='chord strum', scene='scene_1', track='lead', scales=['C-major'], patterns=['chords'], transforms=['basic arp'], repeat=1, auto_scene_advance=True)
api.clips.add(name='chord octaves', scene='scene_2', track='lead', scales=['C-major'], patterns=['chords'], transforms=['octave arp'], repeat=1, auto_scene_advance=True)
api.clips.add(name='chord velocity', scene='scene_3', track='lead', scales=['C-major'], patterns=['chords'], transforms=['velocity arp'], repeat=1, auto_scene_advance=True)
api.clips.add(name='chord ccs', scene='scene_4', track='lead', scales=['C-major'], patterns=['chords'], transforms=['midi cc arp'], repeat=1, auto_scene_advance=True)
api.clips.add(name='melody to bassline', scene='scene_5', track='lead', scales=['C-major'], patterns=['basic'], transforms=['bassline'], repeat=1, auto_scene_advance=True)
api.clips.add(name='melody octave adjustment, then stutter', scene='scene_6', track='lead', scales=['C-major'], patterns=['basic'], transforms=['octave ramp', 'stutter'], repeat=2, auto_scene_advance=True)
api.clips.add(name='stacked transforms', scene='scene_7', track='lead', scales=['C-major'], patterns=['basic'], transforms=[['octave ramp','stutter'],'bassline',['octave arp','basic arp']], repeat=3,  auto_scene_advance=True)

# play
api.player.play_scene('scene_1')
for x in range(0,128000):
    api.player.advance(5)
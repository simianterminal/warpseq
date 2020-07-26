from warpseq.api.public import Api
from warpseq.api.exceptions import *
import sys

DEVICE = 'IAC Driver IAC Bus 1'

# ----------------------------------------------------------------------------------------------------------------------

api = Api()



# ----------------------------------------------------------------------------------------------------------------------
# setup MIDI devices


print("---")
print("available MIDI devices:")
available = api.devices.list_available()
if DEVICE not in available:
    print("please change 'DEVICE' to point to one of your MIDI devices: %s" % available)
    sys.exit(1)

# ----------------------------------------------------------------------------------------------------------------------
# Devices are just names of MIDI devices - they are added for you automatically, but if an song from someone else's
# computer is loaded, you may need to change the instrument definitions to reference yours instead.

print("---")
print("working with devices")

print("Devices = %s" % api.devices.list())
print("details for %s = %s" % (DEVICE, api.devices.details(DEVICE)))

# ----------------------------------------------------------------------------------------------------------------------
# Instruments represent the combination of a MIDI Devices and a MIDI Channel

print("---")
print("working with instruments")

api.instruments.add('euro1', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10)
api.instruments.add('euro2', device=DEVICE, channel=2)
api.instruments.add('euro3', device=DEVICE, channel=3)

api.instruments.edit('euro3', channel=4, device=DEVICE)
api.instruments.remove('euro3')

print(api.instruments.list())
print(api.instruments.details('euro1'))

# ----------------------------------------------------------------------------------------------------------------------
# Tracks are a vertical lane of clips where only one clip can be playing at once, but multiple tracks CAN target
# the same instrument.

print("---")
print("working with tracks")

api.tracks.add(name='track1', instrument='euro1', muted=False)
api.tracks.add(name='track2', instrument='euro2', muted=False)

api.tracks.add(name='track3', instrument='euro1')
api.tracks.edit(name='track3', instrument='euro2')
api.tracks.remove(name='track3')
try:
    api.tracks.remove(name='does_not_exist')
except NotFound:
    pass

print(api.tracks.list())
print(api.tracks.details(name='track1'))

# ----------------------------------------------------------------------------------------------------------------------
# Warp comes with many canned scale patterns but they need to be instanced to specify a base octave. User patterns can
# also be supplied.

api.scales.add(name='C-major', note='C', octave=3, scale_type='major')
api.scales.add(name='Eb-natural-minor', note='Eb', octave=4, scale_type='natural_minor')

api.scales.add(name='F-user', note='F', octave=3, slots=[1,2,'b3',6])
api.scales.edit(name='F-user', note='G', octave=4, new_name='G-user')
api.scales.remove(name='C-major')

# verify we can't pass in both scale_type and slots together
api.scales.edit(name='G-user', slots=[1,2,3], scale_type='major')
# FIXME: why did that work?

print(api.scales.details(name='Eb-natural-minor'))
print(api.scales.details(name='G-user'))
print(api.scales.list())

# -------------------------------------------------------------------------------------------------------------
# Patterns

api.patterns.add(name='up', slots="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16".split(), tempo=90)
api.patterns.add(name='down', slots="15 14 13 12 11 10 9 8 7 6 5 4 3 2 1".split(), length=6, octave_shift=-2, scale='Eb-natural-minor')
api.patterns.add(name='chords', slots="I IV V I".split(), tempo=40)
api.patterns.edit(name='chords', slots="I V IV I", tempo=100, scale='Eb-natural-minor')
api.patterns.remove(name='up')
print(api.patterns.details('chords'))
print(api.patterns.list())




# ----------------------------------------------------------------------------------------------------------------------
# Transforms

api.transforms.add(name='a1', slots=["O+2", "O-1", "1", "O+1", "O+2"], divide=5)
api.transforms.add(name='a2', slots=["1", "1", "1"], octave_slots=[0,1,0,2], divide=6)
api.transforms.add(name='a3', slots=["1", "2", "1"], divide=4)
api.transforms.add(name='a4', slots=[0,1,2], divide=5)
api.transforms.remove(name='a3')
print(api.transforms.details('a2'))
print(api.transforms.list())

# ----------------------------------------------------------------------------------------------------------------------
# Scenes

api.scenes.add(name='s1', tempo=80, scale='Eb-natural-minor', auto_advance=True)
api.scenes.add(name='s2', scale=None, auto_advance=False)
api.scenes.edit(name='s2', auto_advance=True)
print(api.scenes.details('s1'))
print(api.scenes.list())

# FIXME: we should have a way to reorder the scenes by name
# FIXME: adding a scene without a name should be legal and result in an automatic scene name (same for tracks?)- maybe

# ----------------------------------------------------------------------------------------------------------------------
# Tracks


# ----------------------------------------------------------------------------------------------------------------------
# Clips

# simple example
api.clips.add(name='blarg',
              scene='s1',
              track='track1',
              patterns=['chords'])

# complex example
api.clips.add(name='does_not_matter',
              scene='s2',
              track='track1',
              patterns=['down','chords'],
              octave_shifts=[1,0,-1],
              degree_shifts=[0,0,0],
              tempo_shifts=[0,10,20],
              scale_note_shifts=[0,0,0],
              next_clip=None,
              transforms=['a1','a2','a4'],
              tempo=60,
              repeat=3,
              auto_scene_advance=False)
api.clips.edit(scene='s2', track='track1',
               new_name='does_not_matter2',
               patterns=['down','chords'],
               octave_shifts=[1,0,-1],
               degree_shifts=[0,0,0],
               tempo_shifts=[0,10,20],
               scale_note_shifts=[0,0,0],
               next_clip='does_not_matter',
               transforms=['a1','a2'],
               tempo=60,
               repeat=3,
               auto_scene_advance=False)
api.clips.remove(scene='s1', track='track1')

print(api.clips.list())
print(api.clips.details('does_not_matter2'))

# FIXME: probably want to add a method that returns the clip grid
# + currently playing clips
# + currently playing patterns in that clip?

# ----------------------------------------------------------------------------------------------------------------------
# Player

api.player.add_scene('s1')
api.player.add_clips(['c1','c2'])
api.player.remove_clips(['c1','c2'])

for x in range(0,64000):
    api.player.advance(2)

api.player.stop()


# player(scene='s1', track='t1')
#song.stop_clips(scene='s1', track='t2')
#song.play()

# ===

#song.save_as('test.json')
#song.save()
#song.load('test.json')


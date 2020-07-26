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

#song.add_arp(name='a1',slots=["O+2", "O-1", "1", "O+1", "O+2"], divide=5)
#song.add_arp(name='a2',slots=["1", "1", "1"], divide=3)
#song.add_arp(name='a3',slots=["1", "1", "1"], divide=4)

#song.edit_arp(name='a4', divide=5)
#song.remove_arp(name='a4')
#print(song.get_arps())



# ----------------------------------------------------------------------------------------------------------------------
# Scenes

#song.add_scene(name='s1')
#song.add_scene(name='s2', scale='bar_scale')

#song.edit_scene(name='s2', scale='baz_scale')
#song.remove_scene(name='s2')
#print(song.get_scenes())

# ----------------------------------------------------------------------------------------------------------------------
# Tracks

#song.add_track(name='euro1', instrument='euro1', muted=False)
#song.add_track(name='euro2', instrument='euro2', muted=False)
#song.add_track(name='euro3', instrument='euro3', muted=False)

#song.edit_track(name='euro3', muted=True)
#song.remove_track(name='euro3')
#print(song.get_tracks())

# ----------------------------------------------------------------------------------------------------------------------
# Clips

#song.add_clip(scene='s1', track='t1', name='c1', pattern='c_chords', arps=['a2'], repeat=4, next_clip='c2')
#song.add_clip(scene='s1', track='t2', name='c2', pattern='c_chords', length=8, repeat=4, next_clip=None)
#song.add_clip(scene='s2', track='t1', name='c3', pattern='c_chords', repeat=4, next_clip=None)

#song.copy_clip(scene='s2' track='t1', new_scene='s3', new_track='s4')
#song.edit_clip(scene='s2', track='t1', pattern='p2')
#song.move_clip(scene='s2', track='t1', new_scene='s2', new_track='t2')
#song.remove_clip(scene='s2', track='t1')
#print(song.get_clips())

# ----------------------------------------------------------------------------------------------------------------------
# Player

#song.play_clips(scene='s1', track='t1')
#song.stop_clips(scene='s1', track='t2')
#song.play()

# ===

#song.save_as('test.json')
#song.save()
#song.load('test.json')


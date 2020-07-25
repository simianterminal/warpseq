from warpseq.api.public import Api
from warpseq.api import exceptions

DEVICE='IAC Driver IAC Bus 1'

# ----------------------------------------------------------------------------------------------------------------------

api = Api()

# ----------------------------------------------------------------------------------------------------------------------
# setup MIDI devices

print(api.devices.list_available())

#if DEVICE not in devices:
#    raise Exception("this is not a valid device, try one of: %s" % devices)

api.devices.add(DEVICE)
api.devices.add('blippy')
api.devices.edit('blippy', new_name="dev2")
api.devices.remove('blippy')

print(api.devices.describe(DEVICE))

# ----------------------------------------------------------------------------------------------------------------------
# Instruments represent the combination of a MIDI Devices and a MIDI Channel

api.instruments.add('euro1', device=DEVICE, channel=1, min_octave=0, base_octave=3, max_octave=10)
api.instruments.add('euro2', device=DEVICE, channel=2)
api.instruments.add('euro3', device=DEVICE, channel=3)

api.instruments.edit(name='euro3', channel=4, device=DEVICE)
api.instruments.remove(name='euro3')

print(api.instruments.list())
print(api.instruments.describe('euro1'))

# ----------------------------------------------------------------------------------------------------------------------
# Tracks are a vertical lane of clips where only one clip can be playing at once, but multiple tracks CAN target
# the same instrument.

#song.add_track(name='euro1', instrument='euro1', muted=False)
#song.add_track(name='euro2', instrument='euro2', muted=False)

#song.add_instrument(name='test', instrument='euro1')
#song.edit_instrument(name='test', instrument='euro2')
#song.remove_instrument(name='test')
#print(song.get_tracks())

# ----------------------------------------------------------------------------------------------------------------------
# Warp comes with many canned scale patterns but they need to be instanced to specify a base octave. User patterns can
# also be supplied.

#song.add_scale(name='C-major', root='C', octave=3, scale_type='major')
#song.add_scale(name='Eb-natural-minor', root='Eb', octave=4, scale_type='natural_minor')

#song.add_scale(name='F-user', root='F', octave=3, slots=[1,2,'b3',6])
#song.edit_scale(name='F-user', root='G', new_name='G-user')
#song.remove_scale(name='G-user')
#print(song.get_scales())

# ----------------------------------------------------------------------------------------------------------------------
# Arps

#song.add_arp(name='a1',slots=["O+2", "O-1", "1", "O+1", "O+2"], divide=5)
#song.add_arp(name='a2',slots=["1", "1", "1"], divide=3)
#song.add_arp(name='a3',slots=["1", "1", "1"], divide=4)

#song.edit_arp(name='a4', divide=5)
#song.remove_arp(name='a4')
#print(song.get_arps())

# -------------------------------------------------------------------------------------------------------------
# Patterns

#song.add_pattern(name='up', slots="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16".split())
#song.add_pattern(name='down', slots="15 14 13 12 11 10 9 8 7 6 5 4 3 2 1".split(), length=6)
#song.add_pattern(name='chords', slots="I IV V I".split(), arps=[a1], tempo=40)

#song.edit_pattern(name='chords', slots="I V IV I")
#song.remove_pattern(name='chords')
#print(song.get_patterns())

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


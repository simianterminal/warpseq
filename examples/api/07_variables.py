# --------------------------------------------------------------
# Warp API Demo
# (C) Michael DeHaan <michael@michaeldehaan.net>, 2020
# --------------------------------------------------------------
#
# this demo shows how variables work, using them to control
# octave shifts, MIDI CC and velocity
#
# remember that variables are global and are accessible to all tracks
# it can be useful to set them on a muted guide track
#
# the first demo is audible, but the next two may not be depending on
# the configuration of your musical instruments.
#
# to observe MIDI CC behavior, consider recording the MIDI
# stream and looking at it in your DAW.  Then tweak the
# patterns and see how things change.

from warpseq.api import demo
from warpseq.api.public import Api as WarpApi

# setup API and song
api = WarpApi()
api.song.edit(tempo=120)

# setup instruments
DEVICE = demo.suggest_device(api, 'IAC Driver IAC Bus 1')
api.instruments.add('lead_inst', device=DEVICE, channel=1, min_octave=0, base_octave=5, max_octave=10)

# setup tracks
api.tracks.add(name='lead', instrument='lead_inst', muted=False)

# setup scales
api.scales.add(name='C-major', note='C', octave=0, scale_type='major')

# setup patterns

# example 1:
#
# the octave shift is chosen for the pattern and the octave shift
# is applied to two notes in the pattern
# two different scale shift is also chosen and applied to different notes
# (because we have assigned a scale, everything still remains within the scale)

api.patterns.add(name='variables1', slots=[
    'IV $octaveShift=1:4 $noteShift=1:4 $noteShiftB=1:4 S+=$noteShift',
    '2',
    '4 S+=$noteShiftB',
    '6',
    '1 O+=$octaveShift S+=$noteShift',
    '2 S+=$noteShiftB',
    '8 O+=2',
    '4',
    '1 O+=$octaveShift S-=$noteShift',
    '3'
])

# example 2:
#
# two MIDI CC values are selected randomly
# the first value is used on the quarter note beats
# the second value is used for all other beats
# because MIDI CCs are sticky we do not need to set them on every note
# the random values are recomputed each time the pattern changes

api.patterns.add(name='variables2', slots=[
    'IV $x=25:100 $y=25:100 cc1=$x',
    '2 cc1=$y',
    '3',
    '4',
    '1 cc1=$x',
    '2 cc1=$y',
    '3',
    '4',
    '1 cc1=$x',
    '2 cc1=$y',
    '3',
    '4',
    '1 cc1=$x',
    '2 cc1=$y',
    '3',
    '4'
])

# example 3:
#
# velocity values on quarter note beats are full strength
# in between, notes are one of two randomized values
# the randomized values change every pattern

api.patterns.add(name='variables3', slots=[
   'IV v=127 $a=20:40 $b=90:100',
   '2 v=$a',
   '3 v=$b',
   '4 v=$a',
   '1 v=127',
   '2 v=$a',
   '3 v=$b',
   '4 v=$a',
   '1 v=127',
   '2 v=$a',
   '3 v=$b',
   '4 v=$a',
   '1 v=127',
   '2 v=$a',
   '3 v=$b',
   '4 v=$a',
])

# example 3:
#
# velocity values on quarter note beats are full strength
# in between, notes use the set value every other note
# and the notes in between are random

api.patterns.add(name='velocity_variables_demo2', slots=[
    'IV $full=127 v=$full $a=20:40 $b=90:100',
    '2 v=$a',
    '3 v=90:100',
    '4 v=$a',
    '1 v=$full',
    '2 v=$a',
    '3 v=90:100',
    '4 v=$a',
    '1 v=$full',
    '2 v=$a',
    '3 v=90:100',
    '4 v=$a',
    '1 v=$full',
    '2 v=$a',
    '3 v=90:100',
    '4 v=$a',
])



# setup scenes
api.scenes.add(name='scene_1', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_2', rate=0.5, auto_advance=True)
api.scenes.add(name='scene_3', rate=0.5, auto_advance=True)

# setup clips
api.clips.add(name='s1c', scene='scene_1', track='lead', scales=['C-major'], patterns=['variables1'], repeat=8, auto_scene_advance=True)
api.clips.add(name='s2c', scene='scene_2', track='lead', scales=['C-major'], patterns=['variables2'], repeat=8, auto_scene_advance=True)
api.clips.add(name='s3c', scene='scene_3', track='lead', scales=['C-major'], patterns=['variables3'], repeat=8, auto_scene_advance=True)


# play starting on the first scene - Ctrl+C to exit.
api.player.loop('scene_1')
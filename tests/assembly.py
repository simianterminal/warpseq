from warpseq.model.arp import Arp
from warpseq.model.clip import Clip
from warpseq.model.device import Device
from warpseq.model.instrument import Instrument
from warpseq.model.pattern import Pattern
from warpseq.model.song import Song
from warpseq.model.scale import Scale
from warpseq.model.track import Track
from warpseq.model.scene import Scene
from warpseq.model.note import Note
from warpseq.playback.engine.realtime_engine import RealtimeEngine
from warpseq.playback.multi_player import MultiPlayer


import json

def test_assembly():

    # this tests the construction of the datastructures that the UI uses.
    # humans won't be using this directly.

    song = Song(
        name='A Song',
        devices = dict(),
        instruments = dict(),
        scales = dict(),
        tracks = [],
        scenes = [],
        arps = dict(),
        clips = dict(),
        patterns = dict()
    )

    d1 = Device(name='IAC Driver IAC Bus 1')
    d2 = Device(name='MIDI Interface')
    d3 = Device(name='Internal')
    d4 = Device(name='Junk')

    song.add_devices([ d1, d2, d3, d4 ])
    song.remove_device(d4)

    euro1 = Instrument(device=d1, name='eurorack1', channel=1, min_octave=0, base_octave=3, max_octave=8)
    euro2 = Instrument(device=d1, name='eurorack2', channel=2, min_octave=0, base_octave=3, max_octave=8)
    euro3 = Instrument(device=d1, name='eurorack3', channel=3, min_octave=0, base_octave=3, max_octave=8)
    euro4 = Instrument(device=d1, name='eurorack4', channel=4, min_octave=0, base_octave=3, max_octave=8)
    euro5 = Instrument(device=d1, name='eurorack5', channel=5, min_octave=0, base_octave=3, max_octave=8)
    euro6 = Instrument(device=d1, name='eurorack6', channel=6, min_octave=0, base_octave=3, max_octave=8)
    euro7 = Instrument(device=d1, name='eurorack7', channel=7, min_octave=0, base_octave=3, max_octave=8)
    euro8 = Instrument(device=d1, name='eurorack8', channel=8, min_octave=0, base_octave=3, max_octave=8)
    moog  = Instrument(device=d2, name='moog', channel=9, min_octave=2, base_octave=4, max_octave=8)
    kick  = Instrument(device=d3, name='kick', channel=1, min_octave=0, base_octave=3, max_octave=8)

    song.add_instruments([ euro1, euro2, euro3, euro4, euro5, euro6, euro7, euro8, moog, kick])

    foo_scale = Scale(name='foo', root=Note(name='C', octave=3), scale_type='major')
    bar_scale = Scale(name='bar', root=Note(name='C', octave=3), scale_type='minor')
    baz_scale = Scale(name='baz', root=Note(name='C', octave=3), scale_type='pentatonic')

    song.add_scales([ foo_scale, bar_scale, baz_scale ])

    song.scale = foo_scale
    song.tempo = 120
    song.auto_advance = True
    song.measure_length = 16
    song.repeat = 4

    t1  = Track(name='euro1', instrument=euro1, clip_ids=[], muted=False)
    t2  = Track(name='euro2', instrument=euro2, clip_ids=[])
    t3  = Track(name='euro3', instrument=euro3, clip_ids=[])
    t4  = Track(name='euro4', instrument=euro4, clip_ids=[])
    t5  = Track(name='euro5', instrument=euro5, clip_ids=[])
    t6  = Track(name='euro6', instrument=euro6, clip_ids=[])
    t7  = Track(name='euro7', instrument=euro7, clip_ids=[])
    t8  = Track(name='euro8', instrument=euro8, clip_ids=[])
    t9  = Track(name='moog',  instrument=moog, clip_ids=[])
    t10 = Track(name='kick',  instrument=kick, clip_ids=[])
    song.add_tracks([t1,t2,t3,t4,t5,t6,t7,t8,t9,t10])
    song.remove_track(t8)

    s1 = Scene(name='s1', repeat=2, clip_ids=[])
    s2 = Scene(name='s2', scale=bar_scale, clip_ids=[])
    s3 = Scene(name='s3', clip_ids=[])
    s4 = Scene(name='s4', clip_ids=[])
    s5 = Scene(name='s5', clip_ids=[])
    s6 = Scene(name='s6', clip_ids=[])

    song.add_scenes([ s1, s2, s3, s4, s5 ])
    song.remove_scene(s5)

    # FIXME: is this the right data model here?
    a1 = Arp(name='a1', slots=["O+2","O-1","0","O+1","O+2"], divide=3)
    a2 = Arp(name='a2', slots=[1,1,1], divide=4)
    song.add_arps([a1, a2])
    song.remove_arp(a2)

    #p1 = Pattern(name='p1', slots=["I","V", "Eb4 dim", "-", 1, "-", 4,5,6,2,3,8,1,4])
    #p1 = Pattern(name='p1', slots=["1","2","3","4","5","6","7"," "," ", " ", " ", " "])
    #p1 = Pattern(name='p1', slots=["1;O+1", "2;O+1", "3;O+1" ,"4;O+1",
    #                               "1" ,"2", "3", "4",
    #                               "1", "2", "3", "4",
    #                               "1", "2", "3", "4"])

    # FIXME: there seems to be an events calculation lag!

    # FIXME: pattern length seems ignored or overridden


    mixed = Pattern(name='mixed', slots="I;O+1 1 II 2;O-1 i;+1 1;O+1 ii 2;S+4 3;O+1 III 3;# iii;b 4 IV 5;O+1 V 5 v 6;b VII;# 6 vii".split())
    capture = Pattern(name='capture', slots=("1;T=euro1 - - - " * 4).split())

    chords = Pattern(name='chords', slots="I _ _ _ _ IV _ _ _ _ V _ _ _ _ VI _ _ _ _".split(), tempo=120)
    chords2 = Pattern(name='chords2', slots="I IV V VI".split(), tempo=30, length=3)
    up = Pattern(name='up', slots="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15".split(), tempo=120)
    down = Pattern(name='down', slots="15 14 13 12 11 10 9 8 7 6 5 4 3 2 1".split(), tempo=120)
    kick = Pattern(name='kick',   slots="1 _ _ _ 1 _ _ _ 1 _ _ _ 1 _ _ _".split())
    snare = Pattern(name='snare', slots="_ _ 1 _ _ _ 1 _ _ _ 1 _ _ _ 1 _".split())


    song.add_patterns([up,down,chords,snare,kick])


    c_up = Clip(name='c_up', pattern=up, scale=bar_scale, repeat=1, next_clip='c_down') # repeat=2, next_clip='c5', length=4)
    c_down = Clip(name='c_down', pattern=down, scale=bar_scale, repeat=1, next_clip='c_chords') # arp=a1, repeat=1)
    c_chords = Clip(name='c_chords', pattern=chords, scale=baz_scale, arp=a2, repeat=4) # FIXME: repeat isn't implemented
    c_kick = Clip(name='c_kick', pattern=kick, scale=baz_scale, repeat=1, next_clip='c_up')
    c_snare = Clip(name='c_snare', pattern=snare, scale=baz_scale, repeat=1)

    c_mixed = Clip(name='c_mixed', pattern=mixed, scale=baz_scale, repeat=3)
    c_capture = Clip(name='c_capture', pattern=capture, scale=baz_scale)


    song.add_clip(scene=s1, track=t1, clip=c_up)
    song.add_clip(scene=s2, track=t1, clip=c_down)
    song.add_clip(scene=s3, track=t1, clip=c_chords)
    song.add_clip(scene=s4, track=t1, clip=c_kick)
    song.add_clip(scene=s5, track=t1, clip=c_mixed)
    song.add_clip(scene=s6, track=t2, clip=c_capture)

    song.add_clip(scene=s5, track=t2, clip=c_snare)
    # song.remove_clip(scene=s2, track=t2)

    data = song.to_json()
    s2 = Song.from_json(data)
    data2 = s2.to_json()

    multi_player = MultiPlayer(song=song, engine_class=RealtimeEngine) #engine_class=LogEngine)
    multi_player.add_clip(c_chords)
    #multi_player.add_clip(c_capture)

    for x in range(0, 16000):
       multi_player.advance(milliseconds=2)
    # multi_player.remove_clip(c1)

    multi_player.stop()

    # print(data2)

if __name__ == "__main__":
    test_assembly()
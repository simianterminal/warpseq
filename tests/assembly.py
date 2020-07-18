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
from warpseq.playback.engine.log_engine import LogEngine
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
    song.tempo = 140
    song.auto_advance = True
    song.measure_length = 16
    song.repeat = 4

    t1  = Track(name='euro1', instrument=euro1, clip_ids=[])
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
    song.add_scenes([ s1, s2, s3, s4, s5 ])
    song.remove_scene(s5)

    # FIXME: is this the right data model here?
    a1 = Arp(name='a1', slots=["1","-1","-","0"])
    a2 = Arp(name='a2', slots=[1,0,1])
    song.add_arps([a1, a2])
    song.remove_arp(a2)

    #p1 = Pattern(name='p1', slots=["I","V", "Eb4 dim", "-", 1, "-", 4,5,6,2,3,8,1,4])
    p1 = Pattern(name='p1', slots=["1","2","3","4","5","6","7"," "," ", " ", " ", " "])


    p2 = Pattern(name='p2', slots=["I","IV","V","-"," ",1])
    p3 = Pattern(name='p3', slots=[1,' ',' ',' '])
    p4 = Pattern(name='p4', slots=["GRAB(1)","RAND_OFF(0.5)","+1", "IV" ])
    p5 = Pattern(name='p5', slots=[])
    song.add_patterns([p1,p2,p3,p4,p5])
    song.remove_pattern(p5)

    c1 = Clip(name='c1', pattern=p1, scale=bar_scale)
    c2 = Clip(name='c2', pattern=p1, arp=a1, repeat=None, scale=bar_scale)
    c3 = Clip(name='c3', pattern=p2, scale=baz_scale)
    c4 = Clip(name='c4', pattern=p3)
    c5 = Clip(name='c5', pattern=p3, length=4, repeat=4)
    c6 = Clip(name='c6', pattern=p2, length=8, repeat=1)

    #print("C3 scale=%s" % c3.scale)

    song.add_clip(scene=s1, track=t1, clip=c1)
    song.add_clip(scene=s1, track=t2, clip=c2)
    song.add_clip(scene=s2, track=t2, clip=c3)
    song.add_clip(scene=s3, track=t3, clip=c4)
    song.add_clip(scene=s4, track=t1, clip=c5)
    song.add_clip(scene=s2, track=t2, clip=c3)
    song.remove_clip(scene=s2, track=t2)

    clip_access = song.get_clip_for_scene_and_track(scene=s1, track=t2)
    #print("ACCESS = %s" % clip_access.scene)

    data = song.to_json()
    s2 = Song.from_json(data)
    data2 = s2.to_json()

    #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print("NOTES!!!")
    #notes = c2.get_notes(song)
    #for n in notes:
    #    print(">>> %s " % n)
    #print("~~~~~~")


    events = c2.get_events(song)
    for e in events:
        print(e)

    #player = c2.get_player(song, LogEngine)
    #for x in range(0,10):
    #    print(player.advance(milliseconds=50))

    multi_player = MultiPlayer(song=song, engine_class=RealtimeEngine) #engine_class=LogEngine)
    multi_player.add_clip(c1)
    #multi_player.add_clip(c4)

    for x in range(0, 20):
       multi_player.advance(milliseconds=50)

    #multi_player.remove_clip(c1)

    #multi_player.advance(milliseconds=50)
    #multi_player.advance(milliseconds=50)
    multi_player.stop()

    raise Exception("STOP")

    # print(data2)



if __name__=="__main__":
    test_assembly()


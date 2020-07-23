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

# fair warning: this is NOT meant to be musically listenable but is more a testbed for trying out various patterns
# and testing them through MIDI recording / audio

import json

def test_assembly():

    # this tests the construction of the datastructures that the UI uses.
    # humans won't be using this directly. (see api.py)

    #  -----------------------------------------------------------------------------------------------------------------
    # SONG BASICS

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
    song.tempo = 120

    # ------------------------------------------------------------------------------------------------------------------
    # DEVICES

    d1 = Device(name='IAC Driver IAC Bus 1')
    d2 = Device(name='MIDI Interface')
    d3 = Device(name='Internal')
    d4 = Device(name='Junk')
    song.add_devices([ d1, d2, d3, d4 ])
    song.remove_device(d4)

    # ------------------------------------------------------------------------------------------------------------------
    # INSTRUMENTS

    euro1 = Instrument(device=d1, name='eurorack1', channel=1, min_octave=0, base_octave=4, max_octave=8)
    euro2 = Instrument(device=d1, name='eurorack2', channel=2, min_octave=0, base_octave=4, max_octave=8)
    euro3 = Instrument(device=d1, name='eurorack3', channel=3, min_octave=0, base_octave=4, max_octave=8)
    euro4 = Instrument(device=d1, name='eurorack4', channel=4, min_octave=0, base_octave=4, max_octave=8)
    euro5 = Instrument(device=d1, name='eurorack5', channel=5, min_octave=0, base_octave=4, max_octave=8)
    euro6 = Instrument(device=d1, name='eurorack6', channel=6, min_octave=0, base_octave=4, max_octave=8)
    euro7 = Instrument(device=d1, name='eurorack7', channel=7, min_octave=0, base_octave=4, max_octave=8)
    euro8 = Instrument(device=d1, name='eurorack8', channel=8, min_octave=0, base_octave=4, max_octave=8)
    moog  = Instrument(device=d2, name='moog', channel=9, min_octave=2, base_octave=4, max_octave=8)
    kick  = Instrument(device=d3, name='kick', channel=1, min_octave=0, base_octave=4, max_octave=8)
    song.add_instruments([ euro1, euro2, euro3, euro4, euro5, euro6, euro7, euro8, moog, kick])

    # ------------------------------------------------------------------------------------------------------------------
    # SCALES

    foo_scale = Scale(name='foo', root=Note(name='C', octave=0), scale_type='major')
    bar_scale = Scale(name='bar', root=Note(name='C', octave=0), scale_type='pentatonic')
    baz_scale = Scale(name='c4-major', root=Note(name='C', octave=0), scale_type='major')
    akebono_scale   = Scale(name='c3-akebono', root=Note(name='C', octave=0), slots=['1', '2', 'b3', '5', '6'])
    song.add_scales([ foo_scale, bar_scale, baz_scale, akebono_scale ])
    song.scale = foo_scale

    # ------------------------------------------------------------------------------------------------------------------
    # TRACKS

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

    # ------------------------------------------------------------------------------------------------------------------
    # SCENES

    s1 = Scene(name='s1', clip_ids=[])
    s2 = Scene(name='s2', scale=bar_scale, clip_ids=[])
    s3 = Scene(name='s3', clip_ids=[])
    s4 = Scene(name='s4', clip_ids=[])
    s5 = Scene(name='s5', clip_ids=[])
    s6 = Scene(name='s6', clip_ids=[])
    song.add_scenes([ s1, s2, s3, s4, s5 ])
    song.remove_scene(s5)

    # ------------------------------------------------------------------------------------------------------------------
    # ARPS

    a1 = Arp(name='a1', slots=["O+2","1","1","O+1","O+2"], divide=5)
    a2 = Arp(name='a2', slots=[1,1,1], divide=6)
    a3 = Arp(name='octave_hop', slots="O+1 .".split(), divide=1)
    a4 = Arp(name='capture', slots=["T=euro1;O-2"], divide=1)
    a5 = Arp(name='silence', slots=["p=0.05;x"], divide=1)
    a6 = Arp(name='a1', slots=["1","2","3","4","5"], divide=5)
    song.add_arps([a1, a2, a3, a4, a5, a6])


    # ------------------------------------------------------------------------------------------------------------------
    # PATTERNS

    mixed = Pattern(name='mixed', slots=[["1", "3", "5" ],"-", "-", "-", 2, 3, "V", [ "V", "V;O+1"]], tempo=120)

    #capture = Pattern(name='capture', slots=("1;T=euro1 0 0 0" * 4).split(), tempo=30)
    chords = Pattern(name='chords', slots="I _ _ _ _ IV _ _ _ _ V _ _ _ _ VI _ _ _ _".split(), tempo=120)
    #chords2 = Pattern(name='chords2', slots="I IV V VI".split(), tempo=30, length=3)
    up = Pattern(name='up', slots="1;O+1 2 3 4 5 6 7 8 9 10 11 12 13 14 15".split(), tempo=120)
    down = Pattern(name='down', slots="15 14 13 12 11 10 9 8 7 6 5 4 3 2 1".split(), tempo=120)
    kick = Pattern(name='kick',   slots="1 _ _ _ 1 _ _ _ 1 _ _ _ 1 _ _ _".split())
    #"1;ch=major;v=50 - - - - - - - - 7;v=100 _ _ _ 7;v=128 _ _ _".split())
    snare = Pattern(name='snare', octave_shift=1, slots="_ _ 1 _ _ _ 1 _ _ _ 1 _ _ _ 1 _".split())
    #occasionally_silent = Pattern(name='silent', slots='1 _ _ _ 1 _ _ _ 1 _ _ _ 1 _ _ _'.split())
    song.add_patterns([up,down,chords,snare,kick, mixed])

    # ------------------------------------------------------------------------------------------------------------------
    # CLIPS

    c_up = Clip(name='c_up', patterns=[up], scales=[akebono_scale], repeat=4, arps=[a3]) # next_clip='c_chords') # repeat=2, next_clip='c5', length=4)
    c_down = Clip(name='c_down', patterns=[down], scales=[bar_scale], repeat=4) # arp=a1, repeat=1)
    #c_chords = Clip(name='c_chords', patterns=[chords], scales=[baz_scale], arps=[a2], repeat=4) # FIXME: repeat isn't implemented
    c_kick = Clip(name='c_kick', patterns=[kick], scales=[baz_scale], repeat=4, auto_scene_advance=True)
    c_snare = Clip(name='c_snare', patterns=[snare], scales=[baz_scale], repeat=4) # next_clip='c_down')
    c_mixed = Clip(name='c_mixed', patterns=[mixed, up, down], scales=[baz_scale, baz_scale], octave_shifts=[1,2], degree_shifts=[0], scale_note_shifts=[0], repeat=3)
    #c_capture = Clip(name='c_capture', patterns=[capture], scales=[baz_scale])
    #c_silent = Clip(name='c_silent', patterns=[occasionally_silent], scales=[baz_scale], arps=[a5], repeat=8)


    song.add_clip(scene=s1, track=t1, clip=c_kick)
    song.add_clip(scene=s1, track=t2, clip=c_snare)
    song.add_clip(scene=s2, track=t1, clip=c_mixed)
    song.add_clip(scene=s3, track=t1, clip=c_up)
    song.add_clip(scene=s4, track=t2, clip=c_down)

    # ------------------------------------------------------------------------------------------------------------------
    # SAVE/LOAD

    data = song.to_json()
    song2 = Song.from_json(data)
    data2 = song2.to_json()

    # ------------------------------------------------------------------------------------------------------------------
    # PLAYBACK

    multi_player = MultiPlayer(song=song, engine_class=RealtimeEngine)
    #multi_player.add_clip(c_mixed)
    multi_player.play_scene(s1)

    for x in range(0, 16000):

       multi_player.advance(milliseconds=2)
    # multi_player.remove_clip(c1) # FIXME: rename to stop_clip ?
    multi_player.stop()


if __name__ == "__main__":
    test_assembly()
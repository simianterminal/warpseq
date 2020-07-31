# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# some basic tests of the scale class

from warpseq.model.chord import chord
from warpseq.model.note import note
from warpseq.model.scale import Scale, scale


class TestScale(object):

   def _scale_test(self, expression=None, expected=None, length=None):
       if isinstance(expected, str):
           expected = expected.split()
       assert length is not None
       scale1 = scale(expression)
       results = [ note for note in scale1.generate(length=length) ]
       # print("generating: %s for %s" % (expression, length))
       assert chord(results) == chord(expected)

   def test_c_major(self):

       scale1 = scale('C4 major')
       results = []
       for n in scale1.generate(length=10):
           results.append(n)

       # using chords here is kind of silly but it's a useful test function
       # naturally you wouldn't play it this way
       assert chord(results) == chord(['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5'])

   def test_various(self):
       # this is adding some more in depth tests, but hiding some of the ways it would be most likely used by an API consumer
       # see test_c_major for a more idiomatic example of the scale API
       self._scale_test(length=16, expression='C4 chromatic', expected='C4 Db4 D4 Eb4 E4 F4 Gb4 G4 Ab4 A4 Bb4 B4 C5 Db5 D5 Eb5')
       self._scale_test(length=7, expression='C4 natural_minor', expected='C4 D4 Eb4 F G Ab Bb')
       # make sure we can role over octave boundaries correctly
       self._scale_test(length=7, expression='D4 natural_minor', expected='D4 E4 F4 G4 A4 Bb4 C5')
       self._scale_test(length=7, expression='A4 natural_minor', expected='A4 B4 C5 D5 E5 F5 G5')
       self._scale_test(length=7, expression='A4 major', expected='A4 B4 Db5 D5 E5 Gb5 Ab5')

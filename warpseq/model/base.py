# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# base classes for model objects

COUNTER = 0

class BaseObject(object):

    __slots__ = ()

    def one(self, alist):
        length = len(alist)
        if length == 0:
            return None
        #assert length == 1
        return alist[0]

class NewReferenceObject(BaseObject):

    __slots__ = ( 'obj_id' )

    def new_object_id(self):
        global COUNTER
        COUNTER = COUNTER + 1
        return str(COUNTER)

    def __init__(self):
        if self.obj_id in [ None, '0' ]:
            self.obj_id = self.new_object_id()

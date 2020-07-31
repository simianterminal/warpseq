# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# base classes for model objects


from classforge import Class, Field

COUNTER = 0

class BaseObject(Class):

    """
    All base classes inherit from this.
    """

    def one(self, alist):
        length = len(alist)
        if length == 0:
            return None
        assert length == 1
        return alist[0]

class ReferenceObject(BaseObject):

    """
    A reference object is a BaseObject that can be saved as part of a song file.
    The key difference is the self-assigned object ID.
    """

    obj_id = Field(type=str, nullable=False, default='0', required=False)

    def new_object_id(self):
        global COUNTER
        COUNTER = COUNTER + 1
        return str(COUNTER)

    def on_init(self):
        if self.obj_id == '0':
            self.obj_id = self.new_object_id()



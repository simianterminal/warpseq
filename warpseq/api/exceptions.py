# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# custom exception types for easier capture of specific errors

class WarpException(Exception):
    pass

class NotFound(WarpException):
    pass

class AlreadyExists(WarpException):
    pass

class InvalidInput(WarpException):
    pass

class RequiredInput(WarpException):
    pass
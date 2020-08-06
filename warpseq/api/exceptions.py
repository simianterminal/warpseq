# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

# custom exception types for easier capture of specific errors

class WarpException(Exception):
    pass

class AllClipsDone(WarpException):
    pass

class NotFound(WarpException):
    pass

class AlreadyExists(WarpException):
    pass

class InvalidInput(WarpException):
    pass

class RequiredInput(WarpException):
    pass

class InvalidExpression(InvalidInput):
    pass

class InvalidNote(InvalidInput):
    pass

class InvalidChord(InvalidInput):
    pass

class UnexpectedError(WarpException):
    pass

class ConfigError(WarpException):
    pass

class MIDIConfigError(WarpException):
    pass

class InvalidUsage(WarpException):
    pass

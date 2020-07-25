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
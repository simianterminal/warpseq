# the registry keeps track of currently playing events to allow intra-track modifiers

PLAYING_BY_TRACK = dict()
LAST_BY_TRACK = dict()

def _name(track):
    name = None
    if type(track) == str:
        return track
    else:
        return track.name


def register_playing_note(track, note):

    track = _name(track)


    global PLAYING_BY_TRACK, LAST_BY_TRACK

    item = PLAYING_BY_TRACK.get(track, None)
    if item is None:
        PLAYING_BY_TRACK[track] = []
        item = PLAYING_BY_TRACK[track]

    item.append(note)

    LAST_BY_TRACK[track] = note

def unregister_playing_note(track, note):

    track = _name(track)


    global PLAYING_BY_TRACK, LAST_BY_TRACK

    item = PLAYING_BY_TRACK.get(track, None)
    if not item:
        return

    PLAYING_BY_TRACK[track] = [ x for x in item if x != note ]

def get_first_playing_note(track):

    track = _name(track)

    global LAST_BY_TRACK

    rc = LAST_BY_TRACK.get(track, None)
    return rc


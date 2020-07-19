#NOTE_RESOLUTION = .02

# a small gap between notes that ensures the off notes fire before the on notes
NOTE_GAP = 0.01


from .. model.event import Event, NOTE_ON, NOTE_OFF

def evaluate_ties(note_list):

    # note_list is like [[ n1, n2, n3], [n4], [n5, n6]]

    results = []
    previous_notes = None

    print("NL:%s" % note_list)

    for n in note_list:
        if len(n) == 0:
            results.append([])
        elif n[0].tie:
            if previous_notes is not None:
                for p in previous_notes:
                    p.length = n[0].length
            else:
                results.append([])
        else:
            results.append(n)
    return results

def round_partial(value, resolution):
    return round(value / resolution) * resolution

def flatten(old_list):

    # incoming is a list of notes: [n1, n2, n3], [n4], [], [n5, n6]
    # output: [ n1, n2, n3, n4, n5, n6 ]

    results = []
    for x in old_list:
        for y in x:
            results.append(y)
    return results

def notes_to_events(note_list): #, resolution=NOTE_RESOLUTION):

    # takes a note list like
    # [[n1, n2, n3], [n4, n5]]
    #
    # and returns a event list like:
    #
    # [e1_on, e2_on, e3_on], [], [], [e1_off, e2_off, e3_off], [], ...
    #
    # with a finer granularity than the original input stream based on NOTE_RESOLUTION


    results = []
    note_list = flatten(note_list)
    events = []

    for note in note_list:


        start_index = note.start_time #str(round_partial(note.start_time, resolution))
        stop_index = note.end_time #str(round_partial(note.end_time, resolution))

        #storage = buckets.get(start_index, [])

        event = Event(type=NOTE_ON, note=note, time=note.start_time)
        events.append(event)

        #storage.append(event)
        #buckets[start_index] = storage

        #storage = buckets.get(stop_index, [])

        event = Event(type=NOTE_OFF, note=note, time=note.end_time - NOTE_GAP)
        events.append(event)

    def sorter(evt):


        if event.type == NOTE_OFF:
            return event.time - 0.0001

        return evt.time

    events.sort(key=sorter)

    return events


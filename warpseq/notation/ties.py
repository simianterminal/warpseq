def evaluate_ties(note_list):

    # note_list is like [[ n1, n2, n3], [n4], [n5, n6]]

    results = []
    previous_notes = None

    print("NL:%s" % note_list)

    for n in note_list:
        if len(n) == 0:
            results.append([])
        if n[0].tie:
            if previous_notes is not None:
                for p in previous_notes:
                    p.length = n[0].length
            else:
                results.append([])
        else:
            results.append(n)
    return results


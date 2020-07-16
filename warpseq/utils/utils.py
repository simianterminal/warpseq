
import importlib

def roller(alist):
    """
    Returns a generator that keeps looping around a pattern
    """
    while True:
        for item in alist:
            yield item

def roll_left(x):
    """
    Circularly shifts a list to the left
    [ 1,2,3] -> [2,3,1]
    """
    new_list = x[:]
    first = new_list.pop(0)
    new_list.append(first)
    return new_list

def roll_right(x):
    """
    Circularly shifts a list to the right
    [1,2,3] -> [3,1,2]
    """
    new_list = x[:]
    first = new_list.pop()
    new_list.insert(0, first)
    return new_list

# UNUSED?

#def instance_produce(namespace, class_name, args, kwargs):
#    """
#    Produce a class by name.
#    """
#    mod= importlib.import_module(namespace)
#    cls = getattr(mod, class_name.title())
#    return cls(*args, **kwargs)

#def exclude_dict(orig, keys):
#    """
#    Given a dictionary, return a new one without certain keys.
#    """
#    new = dict()
#    for (k,v) in orig.items():
#        if k not in keys:
#            new[k] = v
#    return new
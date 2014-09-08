# -*- coding: utf-8 -*-

"""
    gulib.utils
    ~~~~~~~~~~

    Some utilities functions and objects for gulib.
"""

def norm(name):
    return name.replace('-', '_')

def unnorm(name):
    return name.replace('_', '-')

class FreezedContext(object):
    """
    Context manager that calls ``thaw_notify`` on a given object on exti. Used
    to make ``freeze_notify`` method on `UObject`.
    """
    def __init__(self, obj):
        self._obj = obj

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self._obj.thaw_notify()


class frozendict(dict):

    def _blocked_attribute(self):
        raise AttributeError("A frozendict cannot be modified.")
    _blocked_attribute = property(_blocked_attribute)

    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute

    def __hash__(self):
        return hash(frozenset(self))

    def __repr__(self):
        return "frozendict(%s)" % dict.__repr__(self)

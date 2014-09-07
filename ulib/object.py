# -*- coding: utf-8 -*-

from ulib.signal import SignaledObject
from ulib.utils import FreezedContext, norm, frozendict


class UObject(SignaledObject):

    _freezed = False
    _thaw = set()

    def notify(self, prop_name, *args, **kw):
        if self._freezed:
            self._thaw.add((prop_name, args, frozendict(kw)))
        else:
            self.emit("notify::%s" % prop_name, *args, **kw)

    def freeze_notify(self):
        self._freezed = True
        return FreezedContext(self)

    def thaw_notify(self):
        self._freezed = False
        for prop_name, args, kw in self._thaw:
            self.emit("notify::%s" % prop_name, *args, **dict(kw))
        self._thaw.clear()

    def set_property(self, prop_name, value):
        name = norm(prop_name)
        try:
            prop = type.__getattribute__(self.__class__, name)
        except AttributeError:
            prop = None
        if not isinstance(prop, property) or not hasattr(prop, '__set__'):
            raise ValueError("not writable property named '%s' found" %\
                             prop_name)
        return setattr(self, name, value)

    def get_property(self, prop_name):
        name = norm(prop_name)
        try:
            prop = type.__getattribute__(self.__class__, name)
        except AttributeError:
            prop = None
        if not isinstance(prop, property) or not hasattr(prop, '__get__'):
            raise ValueError("not readable property named '%s' found" %\
                             prop_name)
        return getattr(self, name)

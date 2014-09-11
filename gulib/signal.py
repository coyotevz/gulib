# -*- coding: utf-8 -*-

import sys
from gulib.utils import norm
from gulib.compat import string_type

SIGNAL_RUN_FIRST, SIGNAL_RUN_LAST = list(range(2))


class Signal(object):
    """
    Signal abstraction class
    """

    def __init__(self, name, handler=None, flag=SIGNAL_RUN_LAST):
        """
        @param name: signal name
        @type name: str

        @param handler: default handler (optional)
        @type handler: callable object

        @param flag: default handler run order [SIGNAL_RUN_LAST]
        @type flag: int (SIGNAL_RUN_FIRST | SIGNAL_RUN_LAST)
        """
        self.name = name
        if handler is not None:
            assert callable(handler),\
                    "'handler' must be a callable object or None"
        self._default_handler = handler
        self._flag = flag
        self._callbacks = []
        self._callbacks_after = []
    
    def connect(self, callback, **kwargs):
        "Connect signal callback before SIGNAL_RUN_LAST default handler"
        assert callable(callback), "'callback' must be a callable object"
        handle = (callback, kwargs)
        self._callbacks.append(handle)
        return handle

        self._callbacks.append((handler, kwargs))

    def connect_after(self, callback, **kwargs):
        "Connect signal callback after SIGNAL_RUN_LAST default handler"
        assert callable(callback), "'callback' must be a callable object"
        handle = (callback, kwargs)
        self._callbacks_after.append(handle)
        return handle

    def disconnect(self, handle):
        "Disconnect signal callback connected via connect method"
        self._callbacks.remove(handle)

    def disconnect_after(self, handle):
        "Disconnect signal callback connected via connect_after method"
        self._callbacks_after.remove(handle)

    def emit(self, sender=None, *args, **kwargs):

        retval = None

        if self._default_handler and self._flag is SIGNAL_RUN_FIRST:
            retval = self._default_handler(sender, *args, **kwargs)

        for cb, ckwargs in self._callbacks:
            kw = dict(ckwargs if ckwargs else {})
            kw.update(kwargs if kwargs else {})
            cb(sender, *args, **kw)

        if self._default_handler and self._flag is SIGNAL_RUN_LAST:
            retval = self._default_handler(sender, *args, **kwargs)

        for cb, ckwargs in self._callbacks_after:
            kw = dict(ckwargs if ckwargs else {})
            kw.update(kwargs if kwargs else {})
            cb(sender, *args, **kw)

        return retval

    def __repr__(self):
        return "<Signal %s>" % self.name


def usignal(name, default=None, flag=SIGNAL_RUN_LAST):
    frame = sys._getframe(1)
    try:
        f_locals = frame.f_locals
    finally:
        del frame

    signals = f_locals.setdefault('__signals__', {})

    signals[name] = {'handler': default,
                        'flag': flag}


class SignaledObject(object):
    __signals__ = {}
    _signal_prefix = 'do_'

    def emit(self, name, *args, **kwargs):
        if name not in self._decl_signals:
            return []
        else:
            return self._decl_signals[name].emit(self, *args, **kwargs)

    def connect(self, name, callback, **data):
        if name not in self._decl_signals:
            self._decl_signals[name] = Signal(name)
        return self._decl_signals[name].connect(callback, **data)

    def connect_after(self, name, callback, **data):
        if name not in self._decl_signals:
            self._decl_signals[name] = Signal(name)
        return self._decl_signals[name].connect_after(callback, **data)

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls, *args, **kwargs)
        signals = {}
        # copy base __signals__ declarations
        declared = {}
        for base in reversed(cls.mro()):
            if hasattr(base, '__signals__'):
                declared.update(base.__signals__)
        declared.update(self.__signals__)
        for name, args in declared.items():
            handler = args.get('handler', None)
            flag = args.get('flag', SIGNAL_RUN_LAST)
            if isinstance(handler, string_type):
                if hasattr(cls, handler):
                    handler = getattr(cls, handler)
                else:
                    raise TypeError("%s does not have '%s' method to call" %\
                                    (cls.__name__, handler))
            elif handler is None:
                handler_name = cls._signal_prefix + norm(name)
                if hasattr(cls, handler_name):
                    handler = getattr(cls, handler_name)
            signals[name] = Signal(name, handler, flag)
        self._decl_signals = signals
        return self

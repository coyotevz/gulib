# -*- coding: utf-8 -*-


__version__ = '0.0.1'

from ulib.signal import (
    SIGNAL_RUN_FIRST,
    SIGNAL_RUN_LAST,
    usignal,
    SignaledObject,
)

from ulib.context import (
    PRIORITY_HIGH,
    PRIORITY_DEFAULT,
    PRIORITY_HIGH_IDLE,
    PRIORITY_LOW,
    PRIORITY_DEFAULT_IDLE,
    main_context_default,
    MainContext,
)

from ulib.loop import (
    MainLoop,
)

from ulib.object import (
    UObject,
)

# some shortcuts to work with main context
def idle_add(callback, priority=PRIORITY_DEFAULT_IDLE, context=None):
    ctx = context if context is not None else main_context_default()
    return ctx.idle_add(callback, priority)

def idle_remove(handle, context=None):
    ctx = context if context is not None else main_context_default()
    return ctx.idle_remove(handle)

def timeout_add_seconds(seconds, callback, context=None):
    ctx = context if context is not None else main_context_default()
    return ctx.timeout_add_seconds(seconds, callback)

def timeout_remove(handle, context=None):
    ctx = context if context is not None else main_context_default()
    return ctx.timeout_remove(handle)

def io_add_watch(fd, callback, context=None):
    ctx = context if context is not None else main_context_default()
    return ctx.io_add_watch(fd, callback)

def io_remove_watch(handle, context=None):
    ctx = context if context is not None else main_context_default()
    return ctx.io_remove_watch(handle)

def type_name(obj):
    return obj.__type_name__


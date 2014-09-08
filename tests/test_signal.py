# -*- coding: utf-8 -*-

import pytest

from gulib.signal import (
    SIGNAL_RUN_FIRST, SIGNAL_RUN_LAST, Signal, SignaledObject, usignal
)


class SignalEmitCallback(object):

    order_count = 0

    def __init__(self, name=None):
        self.name = name
        self.reset()

    def __call__(self, sender=None, *args, **kw):
        self.called = True
        self.sender = sender
        self.args = args
        self.kw = kw
        self.order_count = SignalEmitCallback.order_count
        SignalEmitCallback.order_count += 1
        return self.order_count

    def reset(self):
        self.called = False
        self.sender = None
        self.args = None
        self.kw = None
        self.order_count = None


class TestSignal(object):

    def test_constructor(self):
        s = Signal('s')
        assert s.name == 's'
        assert s._default_handler is None
        assert s._flag is SIGNAL_RUN_LAST

    def test_default_handler(self):
        handler = lambda x, *args: x
        s = Signal('s', handler=handler)
        assert s._default_handler is handler

    def test_connect(self):
        callback = lambda x, *args: x
        s = Signal('s')
        handle = s.connect(callback)
        assert s._callbacks == [handle]
        assert s._callbacks == [(callback, {})]

    def test_multi_connect(self):
        cb1 = lambda x, *args: x
        cb2 = lambda y, *args: y
        s = Signal('s')
        h1 = s.connect(cb1)
        assert s._callbacks == [h1]
        h2 = s.connect(cb2)
        assert s._callbacks == [h1, h2]

    def test_connect_after(self):
        cb1 = lambda x, *args: x
        cb2 = lambda y, *args: y
        s = Signal('s')
        h1 = s.connect_after(cb1)
        assert s._callbacks_after == [h1]
        h2 = s.connect_after(cb2)
        assert s._callbacks_after == [h1, h2]

    def test_disconnect(self):
        cb1 = lambda x, *args: x
        cb2 = lambda y, *args: y
        s = Signal('s')
        h1 = s.connect(cb1)
        h2 = s.connect(cb2)
        assert s._callbacks == [h1, h2]
        s.disconnect(h1)
        assert s._callbacks == [h2]
        s.disconnect(h2)
        assert s._callbacks == []

    def test_disconnect_after(self):
        cb1 = lambda x, *args: x
        cb2 = lambda y, *args: y
        s = Signal('s')
        h1 = s.connect_after(cb1)
        h2 = s.connect_after(cb2)
        assert s._callbacks_after == [h1, h2]
        s.disconnect_after(h1)
        assert s._callbacks_after == [h2]
        s.disconnect_after(h2)
        assert s._callbacks_after == []

    def test_connect_disconnect_wrong(self):
        cb1 = lambda x, *args: x
        cb2 = lambda y, *args: y
        s = Signal('s')
        h1 = s.connect(cb1)
        h2 = s.connect_after(cb2)
        with pytest.raises(ValueError):
            s.disconnect(h2)
        with pytest.raises(ValueError):
            s.disconnect_after(h1)
        s.disconnect(h1)
        s.disconnect_after(h2)
        assert s._callbacks == []
        assert s._callbacks_after == []

    def test_emit_default_handler(self):
        handler = SignalEmitCallback('handler')
        s = Signal('s', handler=handler)
        s.emit()
        assert handler.called

    def test_emit_connected(self):
        e1 = SignalEmitCallback('e1')
        e2 = SignalEmitCallback('e2')
        s = Signal('s')
        s.connect(e1)
        s.connect(e2)
        s.emit()
        assert e1.called
        assert e2.called

    def test_emit_connected_order(self):
        handler = SignalEmitCallback('handler')
        e1 = SignalEmitCallback('e1')
        e2 = SignalEmitCallback('e2')
        e3 = SignalEmitCallback('e3')
        e4 = SignalEmitCallback('e4')
        s = Signal('s', handler=handler)
        s.connect(e1)
        s.connect_after(e3)
        s.connect_after(e4)
        s.connect(e2)
        s.emit()
        assert e1.order_count < e2.order_count
        assert e2.order_count < handler.order_count
        assert handler.order_count < e3.order_count
        assert e3.order_count < e4.order_count

    def test_run_first_flag(self):
        handler = SignalEmitCallback('handler')
        e1 = SignalEmitCallback('e1')
        s = Signal('s', handler=handler, flag=SIGNAL_RUN_FIRST)
        s.connect(e1)
        s.emit()
        assert handler.called
        assert e1.called
        assert handler.order_count < e1.order_count

    # TODO: test connect with args & emit with args


class TestSignaledObject(object):

    def test_signal_decl(self):
        class T(SignaledObject):
            __signals__ = {'test-signal': {'handler': None}}
        t = T()
        assert hasattr(t, '_decl_signals')
        assert 'test-signal' in t._decl_signals

    def test_signal_emission(self):
        class T(SignaledObject):
            __signals__ = {'test-signal': {'handler': None}}
        t = T()
        e1 = SignalEmitCallback('e1')
        e2 = SignalEmitCallback('e2')
        t.connect('test-signal', e1)
        t.emit('test-signal')
        assert e1.called
        assert e1.sender is t
        t.connect('test-signal', e2)
        e1.reset()
        t.emit('test-signal')
        assert e1.called
        assert e1.sender is t
        assert e2.called
        assert e2.sender is t

    def test_individual_signals(self):
        class T(SignaledObject):
            __signals__ = {'test-signal': {'handler': None}}
        t1 = T()
        t2 = T()
        e1 = SignalEmitCallback('e1')
        e2 = SignalEmitCallback('e2')
        t1.connect('test-signal', e1)
        t2.connect('test-signal', e2)
        t1.emit('test-signal')
        assert e1.called
        assert e1.sender is t1
        assert e2.called == False
        assert e2.sender is None
        e1.reset()
        t2.emit('test-signal')
        assert e1.called == False
        assert e1.sender is None
        assert e2.called
        assert e2.sender is t2

    def test_emit_unknown_signal_do_nothing(self):
        class T(SignaledObject):
            __signals__ = {'test-signal': {'handler': None}}
        t = T()
        nothing = t.emit('non-existant', 1, 2)
        assert nothing == []

    def test_usignal_helper(self):
        class T(SignaledObject):
            usignal('test-1')
            usignal('test-2')

        t = T()
        assert 'test-1' in t._decl_signals
        assert 'test-2' in t._decl_signals

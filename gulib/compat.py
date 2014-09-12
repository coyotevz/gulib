# -*- coding: utf-8 -*-

import sys

try: # python2.4 and 2.5 compat
    bytes = bytes
except NameError:
    bytes = str

PYTHON3 = sys.version_info > (3, 0)

if PYTHON3:
    string_type = str
    ustring = str
else:
    string_type = basestring
    ustring = unicode

try:
    callable = callable
except NameError:
    def callable(obj):
        return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)

if PYTHON3:
    def b(s): return s.encode("utf-8")
    def u(s): return s
    def s(s): return s.decode("utf-8")
    ord2 = lambda x: x
    chr2 = lambda x: bytes([x])
    bytes3 = bytes
else:
    def b(s): return s
    def u(s): return unicode(s.replace(r'\\', r'\\\\'), "unicode_escape")
    def s(s): return str(s)
    ord2 = ord
    chr2 = chr
    bytes3 = lambda x: bytes().join([chr(c) for c in x])

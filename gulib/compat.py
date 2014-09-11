# -*- coding: utf-8 -*-

import sys

try: # python2.4 and 2.5 compat
    bytes = bytes
except NameError:
    bytes = str

PYTHON3 = sys.version_info > (3, 0)

if PYTHON3:
    string_type = str
else:
    string_type = basestring

try:
    callable = callable
except NameError:
    def callable(obj):
        return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)

if PYTHON3:
    def b(s): return s.encode("latin-1")
    def u(s): return s
else:
    def b(s): return s
    def u(s): return unicode(s.replace(r'\\', r'\\\\'), "unicode_escape")

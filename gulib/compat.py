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

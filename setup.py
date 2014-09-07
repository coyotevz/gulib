# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup

v_file = open(os.path.join(os.path.dirname(__file__),
                           'ulib', '__init__.py'))

VERSION = re.compile(r".*__version__ = '(.*?)'", re.S)\
            .match(v_file.read()).group(1)

setup(
    name='ulib',
    version=VERSION,
    author="Augusto Roccasalva",
    author_email="augusto@rioplomo.com.ar",
    description="Pure python implementation of some functionalities of glib/gobject",
    url="http://github.com/coyotevz/ulib",
    platforms="unix-like",
    license="LGPL",
    packages=['ulib'],
)

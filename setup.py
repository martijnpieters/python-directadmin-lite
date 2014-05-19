#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Directadmin API - Python implementation of Directadmin Web API

Copyright (C) 2009, Andrés Gattinoni
Portions (C) 2014, Martijn Pieters

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=======================================================================

Build script

Implements distutils to create distribution packages of python-directadmin

For more information about Directadmin's Web API, visit:
http://www.directadmin.com/api.html

Original author: Andrés Gattinoni <andresgattinoni@gmail.com>
Author: Martijn Pieters <python@martijnpieters.nl>
"""

import sys
from distutils.core import setup

if not hasattr(sys, 'version_info') or sys.version_info < (3, 2, 0):
    raise SystemExit("python-directadmin-lite requires Python 3.2 or higher to work")

_description = "python-directadmin-lite is a Python implementation " \
               "of Directadmin Panel Control Web API."

setup(name='python-directadmin-lite',
      version='0.6',
      description='Lite Python implementation of Directadmin\'s Web API',
      long_description=_description,
      author='Martijn Pieters',
      author_email='python@martijnpieters.nl',
      license='GPL v.3',
      url='http://code.google.com/p/python-directadmin/',
      download_url='http://code.google.com/p/python-directadmin/downloads/list',
      packages=['directadmin'],
      platforms=['POSIX'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring'
      ])

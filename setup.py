#!/usr/bin/python
# Copyright (C) 2011  Giuliano Di Pasquale
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

setup(name='audiocropper',
      version='0.9beta',
      description='Script for Cropping Sound files using Sox.',
      author='Giuliano Di Pasquale',
      author_email='nooby@gmx.eu',
      url='https://github.com/Nooby/AudioCropper',
      packages=['audiocropper',],
      scripts=['bin/audiocropper'],
     )

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

import subprocess
from shlex import split
from DebugLog import Debug
from Exceptions import AcSoxNotFoundException

soxTrim = ''' "{0}" "{1}" trim {2} {3}'''
soxLength = ''' --info "{0}" -D'''

def SetupSox(command):
    with Debug("SetupSox"):
        Debug.report("Sox command: " + command)
        global soxTrim, soxLength
        soxTrim = command + soxTrim
        soxLength = command + soxLength

def ExecCommand(cmd):
    with Debug("Exec: " + cmd, "Exec"):
        try:
            process = subprocess.Popen(split(cmd), stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, close_fds=True)
        except OSError:
            raise AcSoxNotFoundException()
        (stdout, stderr) = process.communicate()
        if not stderr == "":
            Debug.report(stderr)
        return stdout

def getLength(f):
    with Debug("getLength"):
        lengthString = ExecCommand(soxLength.format(f))
        length = float(lengthString)
        Debug.report(str(length))
        return length

def audioTrim(f, temp, s, l):
    with Debug("audioTrim"):
        ExecCommand(soxTrim.format(f, temp, s, l))
        return


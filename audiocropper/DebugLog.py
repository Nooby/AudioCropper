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

from string import join
from traceback import format_exception

class Debug():
    _depth = 0
    _text = ""
    _exceptionHandled = False
    _trace = ""

    def __init__(self, message):
        self.message = message
        self.myDepth = Debug._depth
        Debug._depth = self.myDepth + 1

    def __enter__(self):
        self.printDebug("Enter %s\n" % self.message)

    def printDebug(self, msg):
        Debug._text += " "*4*self.myDepth + msg

    @classmethod
    def report(cls, msg):
        cls._text += " "*4*(cls._depth+1) + msg + "\n"

    def __exit__(self, t, value, traceback):
        if t is not None and not Debug._exceptionHandled:
            self.printDebug("    Error: %s in %s\n" % (t.__name__, self.message))
            Debug._trace = format_exception(t, value, traceback)
            Debug._exceptionHandled = True
        Debug._depth = Debug._depth - 1
        self.printDebug("Exit %s\n" % self.message)

    @classmethod
    def getDebugData(cls):
        retVal = cls._text
        if not  cls._trace == "":
            retVal += "\n\n" + join(cls._trace, "\n")
        return retVal

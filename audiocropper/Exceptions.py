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

class AcBaseException(Exception):
    def __init__(self, message):
        self.Message = message
    def __str__(self):
        return "Error: " + self.Message

class AcSoxNotFoundException(AcBaseException):
    def __init__(self):
        AcBaseException.__init__(self, "Sox not found. Pleas add Sox to your system Path.")

class AcSoxException(AcBaseException):
    pass

class AcOptionException(AcBaseException):
    pass

class AcNotFoundException(AcBaseException):
    pass

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

from DebugLog import Debug
from Utils import setupTemp, mkTempFile, cleanTemp
from Exceptions import AcOptionException
from shutil import move
from glob import glob
from os.path import abspath, isdir, isfile, exists, join, splitext, basename
from sox import SetupSox, getLength, audioTrim

class Application:

    def __init__(self, opt, args):
        with Debug("AppInit"):
            self.Options = opt
            self.Args = args
        
            self.__checkOpt()
            setupTemp()

            SetupSox(self.Options.sox)

    def __enter__(self):
        return self

    def __checkOpt(self):
        with Debug("CheckOpt"):
            if self.Options.dir is None and len(self.Args) == 0:
                raise AcOptionException("No File or Directory given.")
            if self.Options.start == 0 and self.Options.end == 0: 
                raise AcOptionException("No Start or End Option given.")

    def run(self):
        with Debug("AppRun"):        
            files = self.__gatherFiles()
            self.__processFiles(files)

    def __gatherFiles(self):
        with Debug("gatherFiles"):
            Files = []
            if self.Options.dir is not None:
                for d in self.Options.dir:
                    directory = abspath(d)
                    if exists(directory) and isdir(directory):
                        for f in glob(join(directory, self.Options.pathExtension)):
                            file = join(directory, f)
                            Files.append(file)
                    else:
                        Debug.report("%s does not Exist or is not a Directory." % d)
            if len(self.Args) > 0:
                for f in self.Args:
                    if exists(f) and isfile(f):
                        Files.append(abspath(f))
            Debug.report("%s found." % len(Files))
            return Files

    def __processFiles(self, files):
        with Debug("ProcessFiles"):
            for f in files:
                self.__processFile(f)

    def __processFile(self, f):
        with Debug("ProcessFile: " + basename(f), "ProcessFile"):
            length = getLength(f)
            newLength = length - self.Options.start - self.Options.end
            if newLength <= 0:
                self.__show("File %s is to small to Trim." % f)
                return
            temp = mkTempFile(splitext(f)[1])
            audioTrim(f, temp, self.Options.start, newLength)
            if self.Options.backup:
                move(f, f + ".bak")
            move(temp, f)
            self.__show("File %s trimmed to %f seconds." % (basename(f), newLength))
            return

    def __show(self, msg):
        if self.Options.verbose:
            print(msg)
        return

    def __exit__(self, t, value, stacktrace):
        if self.Options.debug:
            print(Debug.getDebugData())
        cleanTemp()



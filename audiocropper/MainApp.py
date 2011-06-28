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
from Utils import setupTemp
from Exceptions import AcBaseException, AcOptionException
from glob import glob
from shutil import move
from os import remove, rmdir
from os.path import abspath, isdir, isfile, exists, join, splitext, basename


class Application:

    def __init__(self, opt, args):
        with Debug("AppInit"):
            self.Options = opt
            self.Args = args
        
            self.__checkOpt()
            setupTemp()

            self.SoxTrim = self.Options.sox + ''' "{0}" "{1}" trim {2} {3}'''
            self.SoxLength = self.Options.sox + ''' --info "{0}" -D'''

    def __checkOpt(self):
        with Debug("CheckOpt"):
            if self.Options.dir is None and len(self.Options.args) == 0:
                raise AcOptionException("No File or Directory given.")
            if self.Options.start == 0 and self.Options.end == 0: 
                raise AcOptionException("No Start or End Option given.")

    def run(self):
        with Debug("AppRun"):        
            files = self.__gatherFiles()
            #NormalizeFiles()
            #try:
            #    ProcessFiles() 
            #except AcBaseException as e:
            #    self.printError(e)
            #finally:
            #    CleanTemp()
            #    return

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

    
    def printError(self, msg):
        pass



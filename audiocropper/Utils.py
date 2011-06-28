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

import tempfile
from os.path import exists
from os import remove, rmdir
from optparse import OptionParser
from tempfile import mkdtemp, mkstemp
from DebugLog import Debug

tempFolder = ""
tempFile = {}

def mkTempFile(ext):
    with Debug("mkTempFile"):
        temp = ""
        if ext in tempFile:
            temp = tempFile[ext]
        else:
            temp = mkstemp(ext)[1]
            tempFile[ext] = temp
        Debug.report(temp)
        return temp

def setupTemp():
    with Debug("SetupTemp"):
        global tempFolder, tempFile
        tempFolder = mkdtemp()
        tempfile.tempdir = tempFolder

def cleanTemp():
    with Debug("CleanTemp"):
        for key in tempFile:
            if exists(tempFile[key]):
                remove(tempFile[key])
            rmdir(tempFolder)

def setupOptParser():
    with Debug("SetupOptParser"):
        usage = '''Usage: %prog [options] files

        Every Option is Optional, but either the Start or the End Option has to be
        given.
       
        There can be 1 or more file specified. The Files can be relative or absolute
        paths. If one or more Directory is given (With --dir or -d) then files is 
        Optional.

            Example: '%prog -s 10 file1.mp3 file2.mp3'
            This will crop the first 10 seconds of "file1.mp3" and "file2.mp3".

        With the -d or --dir option a Folder can be specified. The Folder can be a
        relative or absolute path. This path will be extended with a Unix style
        path pattern (-x or --path-extension).
        
            Example: '%prog -s 10 -d "~/Test" -d "~/Test2"'
            This will crop the first 10 seconds of every MP3 in the "Test"
            Directory in the current Users Home Directory. (on Linux)
        '''
        parser = OptionParser(usage, version="%prog 0.9rc")
        parser.add_option("-b", "--backup", action="store_true", dest="backup",
            help='''The original file will be stored with ".bak" appended to the filename. This is the Default behavior.''',
            default=True)
        parser.add_option("-B", "--no-backup", action="store_false",
            dest="backup", help='''A Backup will NOT be created. USE WITH CAUTION.''')
        parser.add_option("-d", "--dir", action="append", type="string", metavar="FOLDER", 
            dest="dir", help='''Folder with files for processing. EVERY file witch matches the Path Extension (Default: MP3) in the directory will be processed.''')
        parser.add_option("--debug", action="store_true", dest="debug", 
            default=False, help="Outputs debug Information.")
        parser.add_option("-e", "--end", action="store", type="float", dest="end", metavar="SECONDS",
            help='''time in seconds cropped from the End of the File''', default=0)
        parser.add_option("-p", "--path-to-sox", action="store", type="string",
            dest="sox", default="sox", help='''If sox is not in the System Path, it has to be specified here.''')
        parser.add_option("-q", "--quiet", action="store_false", dest="verbose",
            help='''shows NO status Messages''')
        parser.add_option("-s", "--start", action="store", type="float", metavar="SECONDS",
            dest="start", help='''time in seconds cropped from the Start of the File''',
            default=0)
        parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=True,
            help='''Shows status Messages in the Console. This is the default behavior.''')
        parser.add_option("-x", "--path-extension", action="store", type="string",
            dest="pathExtension", default="*.mp3", metavar="EXT", 
            help='''Unix style pathname pattern witch will be used to find files for processing if a Path is specified with --dir. USE WITH CAUTION.''')
        return parser


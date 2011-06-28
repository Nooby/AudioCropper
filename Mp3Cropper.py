#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

import shlex
import tempfile
import subprocess
from glob import glob
from shutil import move
from os import remove, rmdir
from optparse import OptionParser
from tempfile import mkdtemp, mkstemp
from os.path import abspath, isdir, isfile, exists, join, splitext, basename

tempFolder = ""
tempFile = {}
Options = []
Args = []
Files = []
soxTrim = ''' "{0}" "{1}" trim {2} {3}'''
soxLength = ''' --info "{0}" -D'''

def main():
    SetupEnv()
    NormalizeFiles()
    try:
        ProcessFiles()
    except SoxException as e:
        vPrint("Sox encountered an Error: " + e)
    except SoxNotFoundException as e:
        vPrint("Sox not found. Please add Sox to your system Path or specify the location of Sox with -p.")
    finally:
        CleanUp()
        return

def SetupEnv():
    global soxTrim, soxLength, Options, Args
    SetupTemp()
    optParser = SetupOptParser()
    (Options, Args) = optParser.parse_args()
    checkOpt(Options, Args)
    soxTrim = Options.sox + soxTrim
    soxLength = Options.sox + soxLength
    return

def MkTempFile(ext):
    if ext in tempFile:
        return tempFile[ext]
    else:
        temp = mkstemp(ext)[1]
        tempFile[ext] = temp
        return temp

def SetupTemp():
    global tempFolder, tempFile
    tempFolder = mkdtemp()
    tempfile.tempdir = tempFolder
    return

def CleanUp():
    for key in tempFile:
        if exists(tempFile[key]):
            remove(tempFile[key])
    rmdir(tempFolder)
    return

def SetupOptParser(): 
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

def vPrint(s):
    if Options.verbose:
        print(s)
    return

def checkOpt(opt, args):
    errorString = ""
    if opt.start == 0 and opt.end == 0:
        errorString += '''Error: No Start and End is given. One or both have to be present.\n'''
    if opt.dir is None and len(args) == 0:
        errorString += '''Error: No file and no Directory is given. One or both have to be present.\n'''
    if len(errorString) > 0:
        errorString += '''One or more Errors have occurred. No file was Processed.\nRestart the Programme with -h or --help for assistance.'''
        vPrint(errorString)
        quit()
    return

def NormalizeFiles():
    if Options.dir is not None:
        for d in Options.dir:
            directory = abspath(d)
            if exists(directory) and isdir(directory):
                for f in glob(join(directory, Options.pathExtension)):
                    file = join(directory, f)
                    Files.append(file)
            else:
                vPrint("{0} does not Exist or is not a Directory.".format(d))
    if len(Args) > 0:
        for f in Args:
            if exists(f) and isfile(f):
                Files.append(abspath(f))
    return

def ProcessFiles():
    for f in Files:
        ProcessFile(f)
    return

def ProcessFile(f):
    length = getLength(f)
    newLength = length - Options.start - Options.end
    if newLength <= 0:
        vPrint("File {0} is to small to Trim.".format(f))
        return
    temp = MkTempFile(splitext(f)[1])
    audioTrim(f, temp, Options.start, newLength)
    if Options.backup:
        move(f, f + ".bak")
    move(temp, f)
    vPrint("File {0} trimmed to {1} seconds.".format(basename(f), newLength))
    return

def getLength(f):
    lengthString = ExecCommand(soxLength.format(f))
    length = float(lengthString)
    return length

def audioTrim(f, temp, s, l):
    ExecCommand(soxTrim.format(f, temp, s, l))
    return

def ExecCommand(cmd):
    try:
         return subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    except OSError as e:
       raise SoxNotFoundException(e)

class SoxNotFoundException(Exception):
    pass

class SoxException:
    pass

if __name__ == "__main__":
    main()

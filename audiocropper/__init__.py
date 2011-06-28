from MainApp import Application
from Utils import setupOptParser
from DebugLog import Debug

def main():
    with Debug("main"):
        optParser = setupOptParser()
        (opt, args) = optParser.parse_args()
        app = Application(opt, args)
        app.run()

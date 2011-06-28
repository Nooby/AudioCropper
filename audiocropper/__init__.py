from MainApp import Application
from Utils import setupOptParser
from DebugLog import Debug
from Exceptions import AcBaseException

def main():
    with Debug("main"):
        optParser = setupOptParser()
        (opt, args) = optParser.parse_args()
        try:
            with Application(opt, args) as app:
                app.run()
        except AcBaseException as e:
            print(e)

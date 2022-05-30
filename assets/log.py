from telnetlib import SE
from assets.settings import Settings

class log:
    def __init__(self,message,weight=100,end="\n"):

        if Settings.log.printMinWeight > weight:
            return
        if Settings.printLogToConsole:
            print(message)
        if Settings.writeLogToFile:
            with open(Settings.logFileName, "a") as myfile:
                myfile.write(str(message)+end)

        
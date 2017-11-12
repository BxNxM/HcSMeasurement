try:
    import moduls.DATAlib as dlib
except ImportError:
    import DATAlib as dlib

import os
import time
try:
    import moduls.Loggerlib as Loggerlib
except ImportError:
    import Loggerlib

class RunTimerClass():

    def __init__(self):
        source_dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        timePath = source_dirname + "/systemCache/runtime.txt"
        self.timefile = dlib.FileHandling(timePath)

    def Runtimer(self):
        while True:
            refreshTime = 5
            try:
                lastTime = int(self.timefile.ReadFile())
            except ValueError:
                lastTime = 0

            lastTime += refreshTime
            self.timefile.WriteFile(str(lastTime), mode='w')

            Loggerlib.RuntimeLog.logger.info("Refresh runtime counter: " + str(lastTime) + " sec")

            time.sleep(refreshTime)

    def RuntimeWithFormat(self, mode="string"):
        try:
            timeInSec = int(self.timefile.ReadFile())

            sec = int(timeInSec % 60)
            minute = int(timeInSec / 60 % 60)
            hour = int(timeInSec / 60 / 60 % 24)
            day = int(timeInSec / 60 / 60 / 24 % 7)
            week = int(timeInSec / 60 / 60 / 24 / 7)

            fullTime = str(week) + "w:" + str(day) + "d:" + str(hour) + "h:" + str(minute) + "m:" + str(sec) + "s"
            #print(fullTime)

            if mode == "string":
                return fullTime

            if mode == "dict":
                timeList = {'w': week, 'd': day, 'h': hour, 'm': minute, 's': sec}
                return timeList

        except ValueError:
            Loggerlib.RuntimeLog.logger.critical("!!!Read error from RuntimeWithFormat()")
            return self.RuntimeWithFormat(mode=mode)

    def ResetTimer(self):
        self.timefile.WriteFile("0", mode='w')
        Loggerlib.RuntimeLog.logger.info("Runtime was reset to 0")

def InitRunTimer():
    timer = RunTimerClass()
    return timer

def main():
    t = InitRunTimer()
    t.Runtimer()
    '''
    timeInstring = t.RuntimeWithFormat(mode="string")
    timeInDict = t.RuntimeWithFormat(mode="dict")
    '''

if __name__ == "__main__":
    main()

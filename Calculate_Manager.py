from moduls.DATAlib import *
import  moduls.DATAlib as Dlib
from moduls.FilePipelib import *
import moduls.FilePipelib as fPipe
import moduls.CALCULATElib as Clib
from moduls.CALCULATElib import *

import moduls.Runtimelib as rtime
runtime = rtime.InitRunTimer()

dataFileList = []
pipe = ""
lastweekIstruction = 0
notifyIsEnable=True

def init():
    global dataFileList, pipe
    dataFileList = Dlib.InitDataFiles()
    pipe = fPipe.InitPipe()


def run_calculations():

    global lastweekIstruction, notifyIsEnable
    sleepTimeAfterInstruct=120

    while True:
        dictruntime = runtime.RuntimeWithFormat(mode="dict")
        try:
            week = int(dictruntime['w']) + 1
        except ValueError:
            week = 1


        Watertemp = float(dataFileList[0].ReadData_ToDict(1)[0, 'value'])
        Airtemp = float(dataFileList[1].ReadData_ToDict(1)[0, 'value'])
        Humidity = float(dataFileList[2].ReadData_ToDict(1)[0, 'value'])
        PH = float(dataFileList[3].ReadData_ToDict(1)[0, 'value'])
        EC = float(dataFileList[4].ReadData_ToDict(1)[0, 'value'])
        Light = float(dataFileList[5].ReadData_ToDict(1)[0, 'value'])
        Waterlvl = float(dataFileList[6].ReadData_ToDict(1)[0, 'value'])

        allStatus = Clib.RunValueChacker(week, PH, EC, Watertemp, Airtemp, Light, Humidity, Waterlvl)
        instruction = Clib.WeeklyProcess(week)


        if week != lastweekIstruction:
            lastweekIstruction = week
            pipe.WritePipe(instruction)
            time.sleep(sleepTimeAfterInstruct)

        notifyTag="<<##notify##>>\n"

        global notifyIsEnable
        if notifyIsEnable == True:
            if warningDetector(allStatus)[0]:
                pipe.WritePipe(notifyTag + warningDetector(allStatus)[1] + notifyTag)

        time.sleep(20)


def warningDetector(allStatus):

    text=""

    for key, value in allStatus.items():

        if allStatus[key] == True:
            writeEnable=True

            text += "WARNING: " + str(key[0]) + " difference " + str("%.1f" %  float(allStatus[key[0], 'diff'])) + "\n"

        #print(key)                         #get key
        #print(key[0])                      #get key[0] elemet in key
        #print(allStatus[key[0], 'diff'])   #get difference with key[0]
        #print(value)                       #get value


    return writeEnable, text

def main():
    init()
    run_calculations()

if __name__ == "__main__":
    main()

#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

from moduls.GUIlib import *
import moduls.GUIlib as GUIlib
from moduls.DATAlib import *
import  moduls.DATAlib as Dlib
from moduls.FilePipelib import *
import moduls.FilePipelib as fPipe
import moduls.Loggerlib

# init global variables for this file
dataFileList = 0
framesOnmainWindow = 0
frSwitcher = 0
pipe = 0
root = 0

# SUBFUNCTIONS FOR GUI_MANAGER
def init_GUI():

    global dataFileList, framesOnmainWindow, frSwitcher, pipe, root

    # make tk window
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    GeometryInfo.windowSize(root)           #get screen size for scaling

    #================================== MAIN WINDOW ===================================#
    #make main window frame
    mainFrameWindow = GUIlib.FrameManager(root, height=GeometryInfo.mainWindowSizeDict['height'], width=GeometryInfo.mainWindowSizeDict['width'], \
                            bd=1 , relief=FLAT, background="grey")
    #draw main window frame
    mainFrameWindow.Set_n_Draw()
    #mainFrameWindow.GetFrameInfo()

    #============================= MAIN WINDOW ELEMENTS ===============================#
    # make mainWindow elements in frame
    framesOnmainWindow = UI_Functions.mainUI(mainFrameWindow)
    Loggerlib.GuiLog.logger.info("frames in mainwindow:\n" + str(framesOnmainWindow))

    #================================= SETTINGS WINDOW ================================#
    #make settings window frame
    settingsFrameWindow = GUIlib.FrameManager(root, height=GeometryInfo.mainWindowSizeDict['height'],
                                          width=GeometryInfo.mainWindowSizeDict['width'], \
                                          bd=1, relief=FLAT, background="dim grey")
    framesOnsettingsWindow = UI_Functions.settingsUI(settingsFrameWindow)
    Loggerlib.GuiLog.logger.info("frames in settingswindow:\n" + str(framesOnsettingsWindow))

    #================================ FRAMES SWITCHER ================================#
    #init frames interface to switch it easily (main frame and settings frame)
    frSwitcher = FrameSwitcher(mainFrameWindow, settingsFrameWindow)

    #============================ INIT DATABASE FOR PATH =============================#
    # create files object and return list
    dataFileList = Dlib.InitDataFiles()

    #========================= BUFFERED PIPE FOR CONSOLE WRITEING ====================#
    #init pipe for communicate ConsoleWindow
    pipe = fPipe.InitPipe()


# Intterupt mainLoop - update UI
def UPDATE_UI():

    global dataFileList, framesOnmainWindow, frSwitcher, pipe, root

    Loggerlib.GuiLog.logger.info("<<< UPDATE UI >>>")
    # single value elements
    for i in range(0, len(dataFileList)-1):
        try:
            # dataFileList[i].AddData_WithTimestamp(int(dataFileList[i].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1))
            framesOnmainWindow[i].ChangeValue(dataFileList[i].ReadData_ToDict(1)[0, 'value'])

            # plotting
            dataBufferDict = dataFileList[i].ReadData_ToDict(200)
            dataBufferDictLenght = dataFileList[i].GetDictLenght()
            dataList = []
            for index in range(0, dataBufferDictLenght-1):
                dataList.append(float(dataBufferDict[index, 'value']))
            framesOnmainWindow[10].makePlotInPixel(*dataList, id=i)

        except KeyError:
            errorMessage = "There are no input data (KeyError)! -> " + str(dataFileList[i])
            Loggerlib.GuiLog.logger.critical(errorMessage)
            pipe.WritePipe(errorMessage)

    # switch frames by stored visibility list
    frSwitcher.SwitchManager()

    # console writings from file pipe
    framesOnmainWindow[11].WriteToConsole(pipe.ReadPipe())

    root.after(300, UPDATE_UI)

def main():
    init_GUI()
    UPDATE_UI()
    root.mainloop()

if __name__ == "__main__":
    main()

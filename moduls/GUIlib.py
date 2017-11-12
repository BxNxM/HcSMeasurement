#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

# IMPORT LIBRARY
from tkinter import *
import tkinter as tk
import time
import os
from random import randint
import moduls.CALCULATElib as Cal
from Calculate_Manager import *
import moduls.Runtimelib as rtime
runtime = rtime.InitRunTimer()
try:
    import moduls.Loggerlib as Loggerlib
except ImportError:
    import Loggerlib

'''
Elemets by id
id 0 - sensor value frame (1)  -    WaterTemp
id 1 - sensor value frame (2)  -    AirTemp
id 2 - sensor value frame (3)  -    Hum
id 3 - sensor value frame (4)  -    PH
id 4 - sensor value frame (5)  -    EC
id 5 - sensor value frame (6)  -    Light
id 6 - sensor value frame (7)  -    WaterLvl
id 7 - sensor value frame (8)  -    DataBase
id 8 - single value frame (9)  -    Time
id 9 - single value frame (10) -    Settings
id 10 - Canvas frame (11)      -    Plotting
id 11 - Text frame (12)        -    Console
'''

#plotting visibility
PlotIsVisible = [True, True, True, True, True, True, True, True]

# SETTING AND BASIC CONFIG
debugMode = True

sensor_color=['dark orange', 'green yellow', 'saddle brown', 'dark sea green', "blue", 'pale turquoise',\
              'gold', 'LightSkyBlue4', 'light cyan', 'deep pink', 'dark violet', 'LightSteelBlue3']
backgrounds = ['light grey', 'grey51', 'snow', 'white smoke']
elementTexts = {(0, 'title'): 'WaterTemp', (0, 'dim'): 'C', \
                (1, 'title'): 'AirTemp', (1, 'dim'): 'C', \
                (2, 'title'): 'Hum', (2, 'dim'): 'ml/m^3', \
                (3, 'title'): 'PH', (3, 'dim'): '', \
                (4, 'title'): 'EC', (4, 'dim'): 'mS/cm', \
                (5, 'title'): 'Light', (5, 'dim'): 'L', \
                (6, 'title'): 'WaterLvl', (6, 'dim'): 'cm', \
                (7, 'title'): 'DataBase', (7, 'dim'): '', \
                (8, 'title'): 'Time',\
                (9, 'title'): 'SETTINGS', \
                }

#-------------------------- GET GEOMETRY PARAMETERS --------------------------------#
class GeometryInfo():
    """ this is a geomerty and size calculator """
    mainWindowSizeDict={}

    @staticmethod
    def windowSize(obj):
        """ get full window size """
        GeometryInfo.mainWindowSizeDict['height'] = obj.winfo_height()
        GeometryInfo.mainWindowSizeDict['width'] = obj.winfo_width()

        #if winfo_ not working default size for raspberry ...
        if GeometryInfo.mainWindowSizeDict['height'] == 1 and GeometryInfo.mainWindowSizeDict['width'] == 1:
            GeometryInfo.mainWindowSizeDict['height'] = 480
            GeometryInfo.mainWindowSizeDict['width'] = 800

        Loggerlib.GuiLog.logger.info("GeometryInfo.mainWindowSizeDict['width']:" + str(GeometryInfo.mainWindowSizeDict['width']) + \
              " GeometryInfo.mainWindowSizeDict['height']:"+ str(GeometryInfo.mainWindowSizeDict['height']))

    def ElemetPlaceBYID(id):
        """ this method calculate the top-left corner (in pixel X-Y) for every frame """
        dict_places = {}
        #calculate parameters
        if len(GeometryInfo.mainWindowSizeDict) != 0:
            dict_places['height'] = GeometryInfo.mainWindowSizeDict['height'] / 6
            dict_places['width'] = GeometryInfo.mainWindowSizeDict['width'] / 4
        else:
            Loggerlib.GuiLog.logger.error("INIT GeometryInfo.windowSize(obj) BEFORE USEAGE!")
            return None

        if id < 4 and id >=0:
            #first line (0,0 0,1 0,2 0,3)
            dict_places['offsetX'] = dict_places['width'] * id
            dict_places['offsetY'] =  dict_places['height'] * 0
            Loggerlib.GuiLog.logger.info("element id: "+ str(id) + " " + str(dict_places))

        elif id >= 4 and id <=7:
            #second line (1,0 1,1 1,2 1,3)
            dict_places['offsetX'] = dict_places['width'] * (id-4)
            dict_places['offsetY'] = dict_places['height'] * 1
            Loggerlib.GuiLog.logger.info("element id:" + str(id) + " " + str(dict_places))

        elif id == 8 or id == 9:
            dict_places['offsetX'] = dict_places['width'] * (id-8)
            dict_places['offsetY'] = dict_places['height'] * 2
            Loggerlib.GuiLog.logger.info("element id:" + str(id) + " " + str(dict_places))

        elif id == 10:
            dict_places['offsetX'] = dict_places['width'] * 0
            dict_places['offsetY'] = dict_places['height'] * 3
            #overcalculate element width height for plotting view
            dict_places['width'] = dict_places['width'] * 2
            dict_places['height'] = dict_places['height'] * 3
            Loggerlib.GuiLog.logger.info("element id:" + str(id) + " " + str(dict_places))

        elif id == 11:
            dict_places['offsetX'] = dict_places['width'] * 2
            dict_places['offsetY'] = dict_places['height'] * 2
            # overcalculate element width height for plotting view
            dict_places['width'] = dict_places['width'] * 2
            dict_places['height'] = dict_places['height'] * 4
            Loggerlib.GuiLog.logger.info("element id:" + str(id) + " " + str(dict_places))

        elif id == 12:
            dict_places['offsetX'] = 0
            dict_places['offsetY'] = 0
            dict_places['width'] = dict_places['width']
            dict_places['height'] = dict_places['height'] * 6
            Loggerlib.GuiLog.logger.info("element id:" + str(id) + " " + str(dict_places))

        elif id == 13:
            dict_places['offsetX'] = dict_places['width'] * 1
            dict_places['offsetY'] = 0
            dict_places['width'] = dict_places['width'] * 3
            dict_places['height'] = dict_places['height'] * 6
            Loggerlib.GuiLog.logger.info("element id:" + str(id) + " " + str(dict_places))

        else:
            Loggerlib.GuiLog.logger.critical("ElementID error " + id + " not defined!")
            dict_places['offsetX'] = 0
            dict_places['offsetY'] = 0
            Loggerlib.GuiLog.logger.critical("WORNING! element id:" + str(dict_places))

        return dict_places

#-------------------------- CUSTOM FRAME OBJECT --------------------------------------#
class FrameManager(tk.Frame):
    """ this is a custom basic frame class """
    def __init__(self, motherObj, *args, **kwargs):          # constuctor
        tk.Frame.__init__(self, motherObj, *args, **kwargs)  # super - megjelolt ososztalyra hivatkozas, itt: tk.TK.__init__
        self.GetObjectSizes(**kwargs)

    def GetObjectSizes(self, **kwargs):
        for name, value in kwargs.items():
            if name == "height":
                self.height = value
            elif name == "width":
                self.width = value
            elif name == "background":
                self.color = value

    def Set_n_Draw(self, offsX_=0, offsY_=0):
        self.offsetX = offsX_
        self.offsetY = offsY_
        self.place(bordermode=OUTSIDE, x=self.offsetX, y=self.offsetY)

    def GetFrameInfo(self):
        FrameInfo_dict = {}
        FrameInfo_dict['height'] = self.height
        FrameInfo_dict['width'] = self.width
        FrameInfo_dict['offsetX'] = self.offsetX
        FrameInfo_dict['offsetY'] = self.offsetY
        Loggerlib.GuiLog.logger.info(FrameInfo_dict)
        return FrameInfo_dict

#------------------------ VALUE ELEMENT OBJECT ON FRAME -----------------------------#
class ValueElement(FrameManager):
    """ this is single value viewer element, with color id and binding """
    def __init__(self, motherObj, ID, *args, **kwargs):
        FrameManager.__init__(self, motherObj, *args, **kwargs)
        self.ID = ID
        self.IDcolor=sensor_color[self.ID]
        self.title = elementTexts[self.ID, 'title']
        self.value = "<#>"
        self.dim = elementTexts[self.ID, 'dim']

        #make id coloring square
        self.idFrameSize = self.height/3
        self.idElement = FrameManager(self, height=self.idFrameSize, width=self.idFrameSize, bd=1 , \
                                      relief=RIDGE, bg=self.IDcolor)
        self.idElement.Set_n_Draw(3, 3)

        #make label, (title: value dim)
        self.labelOffsetX = self.width/2
        self.labelOffsetY = self.height/2
        self.label = Label(self, bg=self.color, text=(self.title +": "+ str(self.value) +" "+ self.dim), font=("Helvetica", int(self.idFrameSize/2)))
        self.label.place(x=self.labelOffsetX, y=self.labelOffsetY, anchor="center")

        # binding
        self.bind('<ButtonPress-1>', self.PressedElement)
        self.idElement.bind('<ButtonPress-1>', self.PressedElement)
        self.label.bind('<ButtonPress-1>', self.PressedElement)

        # kivetel egy elemre...
        if self.ID == 7:
            self.DataBaseMonitor()

    def PressedElement(self, event):
        #self.configure(background = 'white')
        Loggerlib.GuiLog.logger.info("ElementPressed on: " + str(self.ID) + " - " + elementTexts[self.ID, 'title'])
        #call console element to write out for debug
        global debugMode
        if debugMode:
            try:
                UI_Functions.elementList_mainUI[11].WriteToConsole("element pressed id: " + str(self.ID) + " - " + elementTexts[self.ID, 'title'])
            except ValueError:
                Loggerlib.GuiLog.logger.critical("UI_Functions.elementList_mainUI[11] was not inited (ConsoleElement)")
        #TODO functions here
        self.TogglePlottingVisibility()
        self.VisibleClick()

    def VisibleClick(self):
        self.config(bg='white')
        self.label.config(bg='white')
        self.update_idletasks()
        self.label.update_idletasks()
        time.sleep(0.1)
        self.config(bg=self.color)
        self.label.config(bg=self.color)
        self.update_idletasks()
        self.label.update_idletasks()


    def TogglePlottingVisibility(self):

        if PlotIsVisible[self.ID] == True:
            PlotIsVisible[self.ID] = False
            Loggerlib.GuiLog.logger.info("Toggle plots to element id:" + str(self.ID) + " OFF ")
            UI_Functions.elementList_mainUI[11].WriteToConsole("Toggle plots to element id:" + str(self.ID) + " OFF" )
        else:
            PlotIsVisible[self.ID] = True
            Loggerlib.GuiLog.logger.info("Toggle plots to element id:" + str(self.ID) + " ON ")
            UI_Functions.elementList_mainUI[11].WriteToConsole("Toggle plots to element id:" + str(self.ID) + " ON" )


    def ChangeValue(self, value):
        self.value = value

        if self.ID != 7:
            self.value = "%.1f" % float(self.value)
            self.label.config(text=(self.title +": "+ str(self.value) +" "+ self.dim))
        else:
            self.label.config(text=(self.title +": " + str(self.value)))

    def DataBaseMonitor(self):
        try:
            DataBaseSize = os.popen("du -h DataBase | awk '{ print $1 }'").read().splitlines()
            self.ChangeValue(DataBaseSize[0])
            self.label.after(1000, self.DataBaseMonitor)
        except Exception as e:
            Loggerlib.GuiLog.logger.critical("[EXCEPTION!!!] " + str(e))

class TimenSettingsElement(FrameManager):

    def __init__(self, motherObj, ID, *args, **kwargs):
        FrameManager.__init__(self, motherObj, *args, **kwargs)
        self.motherObj = motherObj
        self.ID = ID
        self.IDcolor=sensor_color[self.ID]
        self.value = ""
        self.toggleAllPlots=True

        #make label, (title: value dim)
        self.labelOffsetX = self.width/2
        self.labelOffsetY = self.height/2
        self.label = Label(self, bg=self.color, text=str(self.value), font=("Helvetica", int(self.height/6)))
        self.label.place(x=self.labelOffsetX, y=self.labelOffsetY, anchor="center")

        # binding
        self.bind('<ButtonPress-1>', self.PressedElement)
        self.label.bind('<ButtonPress-1>', self.PressedElement)

        if self.ID == 8:
            #this is a time element
            self.ActivateClock()

        elif self.ID == 9:
            self.ChangeValue(elementTexts[self.ID, 'title'])


    def ChangeValue(self, value):
        self.value = value
        self.label.config(text=str(self.value))

    def PressedElement(self, event):
        Loggerlib.GuiLog.logger.info("ElementPressed on: " + str(self.ID) + " - " + elementTexts[self.ID, 'title'])
        global debugMode
        if debugMode:
            try:
                UI_Functions.elementList_mainUI[11].WriteToConsole("element pressed id: " + str(self.ID) + " - " + elementTexts[self.ID, 'title'])
            except ValueError:
                Loggerlib.GuiLog.logger.critical("UI_Functions.elementList_mainUI[11] was not inited (ConsoleElement)")

        if self.ID == 8:
            global PlotIsVisible
            if self.toggleAllPlots:
                Loggerlib.GuiLog.logger.info("Turn all plots visible!")
                UI_Functions.elementList_mainUI[11].WriteToConsole("Turn all plots visible!")
                PlotIsVisible = [True, True, True, True, True, True, True, True]
                self.toggleAllPlots = False
            else:
                Loggerlib.GuiLog.logger.info("Turn all plots unvisible!")
                UI_Functions.elementList_mainUI[11].WriteToConsole("Turn all plots unvisible!")
                PlotIsVisible = [False, False, False, False, False, False, False, False]
                self.toggleAllPlots = True

        if self.ID == 9:
            Loggerlib.GuiLog.logger.info("Toggle MainWindow and Settings window")
            # switch visibility flags for frames
            FrameSwitcher.SwitchFrame()

        self.VisibleClick()

    def VisibleClick(self):
        self.config(bg='white')
        self.label.config(bg='white')
        self.update_idletasks()
        self.label.update_idletasks()
        time.sleep(0.1)
        self.config(bg=self.color)
        self.label.config(bg=self.color)
        self.update_idletasks()
        self.label.update_idletasks()

    def ActivateClock(self):
        self.localtime = str(time.strftime("%H:%M:%S"))
        self.ChangeValue(self.localtime)
        self.label.after(1000, self.ActivateClock)

class PlottingElement(FrameManager):

    def __init__(self, motherObj, ID, *args, **kwargs):
        FrameManager.__init__(self, motherObj, *args, **kwargs)
        self.motherObj = motherObj
        self.ID = ID

        self.canvasbg = 'gray32'
        self.plotcanvas = tk.Canvas(self, width=self.width, height=self.height, bd=0, bg = self.canvasbg)
        self.plotcanvas.place(x=-4, y=-4)
        self.CanvasGrid()

    def CanvasGrid(self):
        self.verticalStep = self.height / 6
        self.horizontalStep = self.width / 6
        self.gridColor='white'

        for step in range(1, 6):
            if step == 3:
                self.plotcanvas.create_line(0, self.verticalStep * step, self.width, self.verticalStep * step,\
                                            fill=self.gridColor, width=3, dash=(10, 2))
                self.plotcanvas.create_line(self.horizontalStep*step, 0, self.horizontalStep*step, self.height, \
                                            fill=self.gridColor, width = 2, dash=(10, 2))
            else:
                self.plotcanvas.create_line(0, self.verticalStep*step, self.width, self.verticalStep*step, \
                                            fill=self.gridColor, width = 1, dash=(10, 2))
                self.plotcanvas.create_line(self.horizontalStep*step, 0, self.horizontalStep*step, self.height, \
                                            fill=self.gridColor, width = 1, dash=(10, 2))

    def makePlotInPixel(self, *dataList, id):

        global PlotIsVisible

        # make our tag to localize data point for one sensor
        mytag = "id" + str(id)

        # delete canvas with id
        self.plotcanvas.delete(mytag)

        if PlotIsVisible[id] == True:

            # got data points
            posY = dataList
            dataNormaized = []

            # normailze data with average value
            smallest = 1000
            biggest = -1000
            for a in range(0, int((len(posY)-1)/3)):
                if smallest > posY[a]:
                    smallest = posY[a]

                if biggest < posY[a]:
                    biggest = posY[a]
            middle = (smallest + biggest) / 2
            distance = biggest - smallest
            corrector = distance
            if distance < 2:
                #print("small data distance " + mytag)
                corrector = corrector * 10

            for a in range(0, len(posY)):
                buff = posY[a]
                dataNormaized.append((buff - middle)  * corrector)

            # calculate sizes
            dotSize = self.height / 40
            dotStepX = 4
            scaleY = 7
            nullLine = (self.height / 2)
            posYLen = len(dataNormaized)
            n = 0

            # draw dots (run time(x) steps)
            for x in range(int(self.width), 0, -dotStepX):

                xyList = [x, (nullLine - dataNormaized[n]*scaleY)]
                #smooth dots
                self.dot_begin = self.plotcanvas.create_oval(xyList[0]-3, xyList[1], xyList[0] + dotSize-3, \
                                            xyList[1] + dotSize, fill=sensor_color[id], outline = sensor_color[id], tag=mytag)
                self.dot_end = self.plotcanvas.create_oval(xyList[0]+3, xyList[1], xyList[0] + dotSize+3, \
                                            xyList[1] + dotSize, fill=sensor_color[id], outline=sensor_color[id], tag=mytag)
                #dot body
                self.dot = self.plotcanvas.create_rectangle(xyList[0], xyList[1], xyList[0] + dotSize,\
                                            xyList[1] + dotSize, fill=sensor_color[id], outline = sensor_color[id], tag=mytag)
                # run data index
                if n < posYLen-1:
                   n+=1


class ConsoleElement(FrameManager):
    """ colsole, terminal window """
    global runtime
    notifyIsEnable = True

    def __init__(self, motherObj, ID, *args, **kwargs):
        FrameManager.__init__(self, motherObj, *args, **kwargs)
        self.motherObj = motherObj
        self.ID = ID

        #scrollbar and textBox
        # height - lines, width - characters
        self.Sclbr = Scrollbar(self)
        self.Sclbr.config(bd=1, bg = self.color)

        # set Text size (in character) for Mac or Pi
        if GeometryInfo.mainWindowSizeDict['height'] == 480:
            self.textrelSize = {'h': 15, 'w': 35}
        else:
            self.textrelSize={'h': 15 + 27, 'w': 35 + 50}                   #pi sizes + mac sizes

        self.textBox = Text(self, bg = self.color, padx = 10, pady=10, \
                            height=self.textrelSize['h'], \
                            width=self.textrelSize['w'],\
                       font=("Helvetica", 12))

        #set scrollbar
        self.Sclbr.pack(side=RIGHT, fill=Y)
        self.textBox.pack(side=LEFT, fill=Y)
        self.Sclbr.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.Sclbr.set)

    def WriteToConsole(self, quote):
        inTime = runtime.RuntimeWithFormat(mode="string")
        self.prompt = ">[" + inTime + "]$ \n"
        line = ""
        formated_quote = ""
        if quote != None:
            quote += "\n"
            line +=  self.prompt
            for char in quote:
                line += char
                if char == "\n":
                    line = line
                    formated_quote += line
                    line = ""

            if not ConsoleElement.notifyIsEnable:
                formated_quote = formated_quote.split('<<##notify##>>')[0]
                self.textBox.delete('1.0', END)

            if formated_quote != self.prompt:
                self.textBox.insert(END, formated_quote + "\n")
                Loggerlib.GuiLog.logger.info("Notify status: " + str(ConsoleElement.notifyIsEnable))

            # autoscroll
            self.textBox.yview('end')

class SettingsButtons(FrameManager):

    def __init__(self, motherObj, *args, **kwargs):
        FrameManager.__init__(self, motherObj, *args, **kwargs)
        self.motherObj = motherObj
        self.buttonInframeOffsetY=self.height/6
        self.notifyStatus=True

        self.backButton = tk.Button(self, text ="BACK", command = self.back)
        self.exitButton = tk.Button(self, bg = "red", text="EXIT", command=self.exit)
        self.resetRunTime = tk.Button(self, text="RESET RUNTIME", command=self.resetRUNTIME)
        self.resetDataBase = tk.Button(self, text="RESET DATABSE", command=self.resetDATABASE)
        self.notifications = tk.Button(self, text="NOTIFICATION ENABLE", command=self.notify)
        self.runtimeDisplay = Label(self, text="runtime:\n12:12:12", font=("Helvetica", 12))

        self.backButton.place(width=self.width, height=self.height/6, y=self.buttonInframeOffsetY * 0)
        self.resetRunTime.place(width=self.width, height=self.height/6, y=self.buttonInframeOffsetY * 1)
        self.resetDataBase.place(width=self.width, height=self.height/6, y=self.buttonInframeOffsetY * 2)
        self.notifications.place(width=self.width, height=self.height/6, y=self.buttonInframeOffsetY * 3)
        self.runtimeDisplay.place(width=self.width, height=self.height/6, y=self.buttonInframeOffsetY * 4)
        self.exitButton.place(width=self.width, height=self.height/6, y=self.buttonInframeOffsetY * 5)

        self.run_Runtime()

    def run_Runtime(self):
        global runtime
        inTime = runtime.RuntimeWithFormat(mode="string")
        self.runtimeDisplay.config(text="RUNTIME\n" + str(inTime))
        self.runtimeDisplay.after(2000, self.run_Runtime)

    def back(event):
        FrameSwitcher.SwitchFrame()

    def exit(self):
        source_dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fullcommandForExit = source_dirname + '/Louncher.sh --kill'
        Loggerlib.GuiLog.logger.info(fullcommandForExit)
        # execute shell script
        os.system(fullcommandForExit)

    def resetDATABASE(event):
        source_dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fullcommandForExit = source_dirname + '/Louncher.sh --button_resetdatabase'
        Loggerlib.GuiLog.logger.info(fullcommandForExit)
        # execute shell script
        os.system(fullcommandForExit)

    def resetRUNTIME(event):
        runtime.ResetTimer()

    def notify(self):
        if self.notifyStatus:
            self.notifyStatus = False
            self.notifications.config(text="NOTIFICATION DISABLE")
            #TODO: set nofications disable
            ConsoleElement.notifyIsEnable = False

        else:
            self.notifyStatus = True
            self.notifications.config(text="NOTIFICATION ENABLE")
            # TODO: set nofications enable
            ConsoleElement.notifyIsEnable = True

class SettingsDataDisplay(FrameManager):

    def __init__(self, motherObj, *args, **kwargs):
        FrameManager.__init__(self, motherObj, *args, **kwargs)
        self.motherObj = motherObj

        #scrollbar and textBox
        # height - lines, width - characters
        self.Sclbr = Scrollbar(self)
        self.Sclbr.config(bd=1, bg = self.color)

        # set Text size (in character) for Mac or Pi
        if GeometryInfo.mainWindowSizeDict['height'] == 480:
            self.textrelSize = {'h': 32, 'w': 70}
            textSize=9
        else:
            self.textrelSize={'h': 65, 'w': 130}                   #pi sizes + mac sizes
            textSize=12

        self.textBox = Text(self, bg = self.color, padx = 10, pady=10, \
                            height=self.textrelSize['h'], \
                            width=self.textrelSize['w'],\
                       font=("Helvetica", textSize))

        #set scrollbar
        self.Sclbr.pack(side=RIGHT, fill=Y)
        self.textBox.pack(side=LEFT, fill=Y)
        self.Sclbr.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.Sclbr.set)

        self.dataString = Cal.GetDataBaseString()
        self.WriteToConsole(self.dataString)

    def WriteToConsole(self, quote):
        if quote != None:
            self.textBox.insert(END, quote + "\n")
            # autoscroll
            self.textBox.yview('end')


class FrameSwitcher():
    """ Manage MAIN frames (main and settings) """
    # frames visibility (0-mainwindow, 1-settings window)
    FrameIsVisible = [True, False]
    IsChangeHappened = False

    def __init__(self, frame1, frame2):
        self.frame1 = frame1
        self.frame2 = frame2

    #change inited frames by FrameIsVisibe list
    def SwitchManager(self):
        if FrameSwitcher.FrameIsVisible[0] == True and FrameSwitcher.FrameIsVisible[1] == False and FrameSwitcher.IsChangeHappened == True:
            #mainframe to settings frame
            self.frame2.place_forget()
            self.frame1.Set_n_Draw()
            FrameSwitcher.IsChangeHappened = False

        elif FrameSwitcher.FrameIsVisible[0] == False and FrameSwitcher.FrameIsVisible[1] == True and FrameSwitcher.IsChangeHappened == True:
            #settings frame to mainframe
            self.frame1.place_forget()
            self.frame2.Set_n_Draw()
            FrameSwitcher.IsChangeHappened = False

    # switch tags to change frames, staticmethod! call from anywhere
    @staticmethod
    def SwitchFrame():
        FrameSwitcher.IsChangeHappened = True

        if FrameSwitcher.FrameIsVisible[0] == True and FrameSwitcher.FrameIsVisible[1] == False:
            #mainframe to settings frame
            FrameSwitcher.FrameIsVisible[0] = False
            FrameSwitcher.FrameIsVisible[1] = True

        elif FrameSwitcher.FrameIsVisible[0] == False and FrameSwitcher.FrameIsVisible[1] == True:
            #settings frame to mainframe
            FrameSwitcher.FrameIsVisible[0] = True
            FrameSwitcher.FrameIsVisible[1] = False

    # UI ELEMETS CREATOR
class UI_Functions():
    """ UI element manager """
    elementList_mainUI = []
    elementList_settingsUI = []

    @staticmethod
    def mainUI(motherObj):
        # value elements in frame on motherObj (mainWindowframe)
        for id in range(0, 8):
            UI_Functions.elementList_mainUI.append(ValueElement(motherObj, id, height=GeometryInfo.ElemetPlaceBYID(id)['height'], \
                                            width=GeometryInfo.ElemetPlaceBYID(id)['width'], bd=1, relief=RIDGE,
                                            background=backgrounds[3])
                               )
            UI_Functions.elementList_mainUI[id].Set_n_Draw(GeometryInfo.ElemetPlaceBYID(id)['offsetX'],
                                       GeometryInfo.ElemetPlaceBYID(id)['offsetY'])

        # Timen & Settings frame on motherObj (mainWindowframe)
        for id in range(8, 10):
            UI_Functions.elementList_mainUI.append(TimenSettingsElement(motherObj, id, height=GeometryInfo.ElemetPlaceBYID(id)['height'], \
                                     width=GeometryInfo.ElemetPlaceBYID(id)['width'], bd=1, relief=RIDGE,
                                     background=backgrounds[3]))
            UI_Functions.elementList_mainUI[id].Set_n_Draw(GeometryInfo.ElemetPlaceBYID(id)['offsetX'],
                                       GeometryInfo.ElemetPlaceBYID(id)['offsetY'])

        # Plotting window frame
        id = 10
        UI_Functions.elementList_mainUI.append(PlottingElement(motherObj, id, height=GeometryInfo.ElemetPlaceBYID(id)['height'], \
                               width=GeometryInfo.ElemetPlaceBYID(id)['width'], bd=1, relief=RIDGE,
                               background=backgrounds[0]))
        UI_Functions.elementList_mainUI[id].Set_n_Draw(GeometryInfo.ElemetPlaceBYID(id)['offsetX'], GeometryInfo.ElemetPlaceBYID(id)['offsetY'])

        # Console window frame
        id = 11
        UI_Functions.elementList_mainUI.append(ConsoleElement(motherObj, id, height=GeometryInfo.ElemetPlaceBYID(id)['height'], \
                                 width=GeometryInfo.ElemetPlaceBYID(id)['width'], bd=3, relief=RIDGE,
                                 background=backgrounds[0]))
        UI_Functions.elementList_mainUI[id].Set_n_Draw(GeometryInfo.ElemetPlaceBYID(id)['offsetX'], GeometryInfo.ElemetPlaceBYID(id)['offsetY'])
        UI_Functions.elementList_mainUI[id].WriteToConsole(">>> WELCOME HcS MEASUREMENT <<<\n")

        Loggerlib.GuiLog.logger.info("mainUI inited successfully")
        return UI_Functions.elementList_mainUI

    @staticmethod
    def settingsUI(motherObj):
        id = 12
        UI_Functions.elementList_settingsUI.append(SettingsButtons(motherObj, height=GeometryInfo.ElemetPlaceBYID(id)['height'], width=GeometryInfo.ElemetPlaceBYID(id)['width'], \
                            bd=1 , relief=FLAT, background="grey"))
        UI_Functions.elementList_settingsUI[id-12].Set_n_Draw(GeometryInfo.ElemetPlaceBYID(id)['offsetX'], GeometryInfo.ElemetPlaceBYID(id)['offsetY'])

        id = 13
        UI_Functions.elementList_settingsUI.append(SettingsDataDisplay(motherObj, height=GeometryInfo.ElemetPlaceBYID(id)['height'], width=GeometryInfo.ElemetPlaceBYID(id)['width'], \
                            bd=1 , relief=FLAT, background="grey"))
        UI_Functions.elementList_settingsUI[id-12].Set_n_Draw(GeometryInfo.ElemetPlaceBYID(id)['offsetX'], GeometryInfo.ElemetPlaceBYID(id)['offsetY'])

        return UI_Functions.elementList_mainUI

#--------------------------------- TEST CODES -----------------------------------------#
if __name__ == "__main__":

    print(elementTexts[0, 'title'])
    print(elementTexts[0, 'dim'])
    print(elementTexts)

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    GeometryInfo.windowSize(root)           #get screen size for scaling

    #make main window frame
    mainFrameWindow = FrameManager(root, height=GeometryInfo.mainWindowSizeDict['height'], width=GeometryInfo.mainWindowSizeDict['width'], \
                            bd=1 , relief=FLAT, background="grey")
    mainFrameWindow.Set_n_Draw()
    mainFrameWindow.GetFrameInfo()

    #make mainWindow elements in frame
    framesOnmainWindow = UI_Functions.mainUI(mainFrameWindow)
    print("frames in mainwindow:\n" + str(framesOnmainWindow))

    posY = []
    for k in range(0, 100):
        posY.append(randint(-10, 10))

    framesOnmainWindow[10].makePlotInPixel(*posY, id=0)

    posY = []
    for k in range(0, 100):
        posY.append(randint(-10, 10))

    framesOnmainWindow[10].makePlotInPixel(*posY, id=1)

    root.mainloop()

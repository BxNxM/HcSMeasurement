#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3q
try:
    # IMPORT MODULS
    # default moduls
    import os
    import time, datetime
    from random import randint
    import sys
    # custom moduls
    myfolder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(myfolder)
    import Loggerlib
except Exception as e:
    print("IMPORT EXCEPTION!!! " + str(e))

# get source path parent's folder parent's folder
source_dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prePath = source_dirname + '/DataBase/'
fileExtension = '.txt'
sensorsFilePath = [prePath + 'Watertemp' + fileExtension, \
                   prePath + 'Airtemp' + fileExtension, \
                   prePath + 'Humidity' + fileExtension, \
                   prePath + 'PH' + fileExtension, \
                   prePath + 'EC' + fileExtension, \
                   prePath + 'Light' + fileExtension, \
                   prePath + 'Waterlvl' + fileExtension, \
                   prePath + 'DataBaseSize' + fileExtension
                   ]

class FileHandling():
    """ BASIC SECURE FILE READINGS AND WRITINGS """

    def __init__(self, path):
        if os.path.exists(path):
            self.path = path
            self.content = ""
            self.isEnable = True
        else:
            Loggerlib.DataLog.logger.critical(path + " IS NOT EXIST!")
            self.isEnable = False
            #TODO make the file.... -> self.isEnable = Frue
            self.CreateFile(path)
            self.__init__(path)

    def CreateFile(self, path):
        with open(path, 'w+') as newfile:
            Loggerlib.DataLog.logger.info("Create path: " + str(path) + str(newfile))
            return True

    def ReadFile(self, lastx=None):
        if self.isEnable == True:
            if lastx == None:
                with open(self.path, 'r') as file:           #automaticly open and close the file after this function (safe!)
                    try:
                        self.content = file.read()
                        return self.content

                    except ValueError:
                        return False
            else:
                cmd = "tail -n " + str(lastx) + " " + str(self.path)
                self.content = os.popen(cmd).read()
                return self.content

    def WriteFile(self, data, mode='a'):                #default mode is append 'a', but 'w' for rewrite file
        if self.isEnable == True:
            self.data = data
            if os.path.exists(self.path) and self.data != None:
                with open(self.path, mode) as file:
                    file.write(self.data)
                    return True
        else:
            return False

    def GetFilePath(self):
        #print(self.path)
        return self.path

class DataManager(FileHandling):
    """ DATA HANDLING IN FILES WITH TIMESTAMP """

    def __init__(self, path):
        FileHandling.__init__(self, path)

    def AddData_WithTimestamp(self, data, mode = 'a'):
        if self.isEnable == True:
            ts = self.TimeStamp()
            self.WriteFile(str(ts[0]) + "\t" + str(data) + "\n", mode)
        else:
            return False

    def AddList_WithTimestamp(self, *stack, mode = 'a'):
        if self.isEnable == True:
            for data in stack:
                self.AddData_WithTimestamp(data, mode)
            Loggerlib.DataLog.logger.info(str(stack) + " added successfully mode: " + str(mode))

    def ReadData_ToDict(self, lastX=None):
        if self.isEnable == True:
            self.dataDict={}
            indexdict=0
            data_str = self.ReadFile(lastX)
            dataList = data_str.split()
            for index in range(len(dataList)-1, 0, -2):
                self.dataDict[indexdict, 'timestamp'] = dataList[index-1]
                self.dataDict[indexdict, 'value'] = dataList[index]
                indexdict+=1

            # CALCULATE DICT LENGHT
            self.dictLenght = int((len(self.dataDict)/2 + 1))
            # RETURN DICTIONRY "INDEX 0" - MOST RELEVANT ELEMENT, FRESHEST
            return self.dataDict
        else:
            return False

    def GetDictLenght(self):
        return self.dictLenght

    @classmethod
    def TimeStamp(self):
        self.timeInSec = round(time.time(), 4)                                      #cut 4 digit
        self.timeInFormat = datetime.datetime.fromtimestamp(self.timeInSec).strftime('%Y-%m-%d %H:%M:%S')
        return self.timeInSec, self.timeInFormat


def InitDataFiles():

    fileObjectsList = []
    for actualPath in sensorsFilePath:
        fileObjectsList.append(DataManager(actualPath))
    return fileObjectsList


# ---------------------------------- USAGE --------------------------------------#
if __name__ == "__main__":

    fileList = InitDataFiles()
    print(fileList)

    '''
    # CREATE SENSOR LIST OBJECTS
    fileObjectsList=[]
    for actualPath in sensorsFilePath:
        fileObjectsList.append(DataManager(actualPath))


    # Make random data for testing
    print("START SENSORS RANDOM DATA GENERATING...")
    for i in range(0,len(sensorsFilePath)):
        # Test data generations
        for d in range(0, 100):
            fileObjectsList[i].AddData_WithTimestamp(randint(10, 100))

        print("Last 10 data from: " + str(sensorsFilePath[i]) + " listid: " + str(i))
        datas = fileObjectsList[i].ReadData_ToDict(2)
        print(datas)

    d = DataManager("text.txt")

    d.AddData_WithTimestamp(randint(1, 20))
    #dataDict = d.ReadData_ToDict()             #return full file in dicet
    dataDict = d.ReadData_ToDict(1)             #return last x lines in dict

    for index in range(0, (d.GetDictLenght())-1 ):
        print("index: " + str(index) + " timestamp: " + dataDict[index, 'timestamp'] + "\tvalue: " + dataDict[index, 'value'])

    stack = [1, 2, 3, 4, 5, 6, 7]
    d.AddList_WithTimestamp(*stack, mode='a')
    '''





from moduls.DATAlib import *
import moduls.DATAlib as Dlib

dataFileList=None

def Refresh_dataBase():
    global dataFileList

    '''
    Upload database here
    i = id
    id 0 - Watertemp
    id 1 - Airtemp
    id 2 - Humidity
    id 3 - PH
    id 4 - EC
    id 5 - Light
    id 6 - Waterlvl
    id 7 - DataBaseSize
    '''

    while True:
        #print("TEST DATAs IS GENERATING")
        for i in range(0, len(dataFileList) - 1):
            try:
                dataFileList[i].AddData_WithTimestamp(float(dataFileList[i].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10)
            except KeyError:
                dataFileList[i].AddData_WithTimestamp(randint(-1, 1))

        time.sleep(2)

def main():
    global dataFileList
    # init data files objects from usage
    dataFileList = Dlib.InitDataFiles()
    Refresh_dataBase()

if __name__ == "__main__":
    main()

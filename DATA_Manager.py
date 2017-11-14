from moduls.DATAlib import *
import moduls.DATAlib as Dlib
import moduls.Loggerlib as Loggerlib

'''
::: DATABASE INDEXING :::
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

dataFileList=None
# ::: SET READING PERIOD HERE :::
read_period = 2         # sec

def Watertemp_read():
    data_id = 0
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id

def Airtemp_read():
    data_id = 1
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id

def Humidity_read():
    data_id = 2
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id

def PH_read():
    data_id = 3
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id

def EC_read():
    data_id = 4
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id

def Light_read():
    data_id = 5
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id

def Waterlvl_read():
    data_id = 6
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id

def DataBaseSize_read():
    data_id = 7
    # --- GET TEST VALUE ---
    # SET REAL SENSOR READING HERE TAKE THE SENSOR VALUE TO VALUE VARIABLE - AND YOU ARE DONE :)
    try:
        value = float(dataFileList[data_id].ReadData_ToDict(1)[0, 'value']) + randint(-1, 1)/10
    except Exception as e:
        Loggerlib.DataLog.logger.critical(e)
        value = randint(-1, 1)
    # ----------------------
    return value, data_id


def debug_print(text, state=False):
    if state:
        print(str(text))

def Refresh_dataBase():
    global dataFileList, read_period

    while True:
        debug_print("TEST DATAs IS GENERATING")

        output_tuple = Watertemp_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor Watertemp index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        output_tuple = Airtemp_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor Airtemp index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        output_tuple = Humidity_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor Humidity index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        output_tuple = PH_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor PH index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        output_tuple = EC_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor EC index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        output_tuple = Light_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor Light index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        output_tuple = Waterlvl_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor Waterlvl index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        output_tuple = DataBaseSize_read()
        dataFileList[output_tuple[1]].AddData_WithTimestamp(output_tuple[0])
        debug_print("\tSensor Database index: {} value: {}".format(output_tuple[1], output_tuple[0]))

        time.sleep(read_period)

def main():
    global dataFileList
    # init data files objects from usage
    dataFileList = Dlib.InitDataFiles()
    Refresh_dataBase()

if __name__ == "__main__":
    main()

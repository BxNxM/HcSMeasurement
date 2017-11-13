# -*- encoding: utf-8 -*-
#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
try:
    import json
    import os
    import sys
    myfolder = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(myfolder)
    import Loggerlib
except Exception as e:
    print("IMPORT EXCEPTON!!! " + str(__name__) + "\n" +  str(e))

generalValue_path = myfolder + "/../config/generalValue.json"
nutritionValues_path = myfolder + "/../config/nutritionValues.json"

class ConfigHandler():
    def __init__(self, cfg_path):
            self.cfg_path = cfg_path

    # EXTERNAL FUNCTIONS - GET VALUE
    def get(self, key):
        config = self.read_cfg_file()
        try:
            value = config[key]
        except:
            value = None
        return value

    # EXTERNAL FUNCTION - GET ALL
    def get_all(self):
        config = self.read_cfg_file()
        return config

    # EXTERNAL FUNCTION - PUT VALUE
    def put(self, key, value):
        config = self.read_cfg_file()
        config[key] = value
        self.write_cfg_file(config)

    def write_cfg_file(self, dictionary):
        try:
            with open(self.cfg_path, 'w') as f:
                json.dump(dictionary, f, sort_keys=True, indent=2)
        except Exception as e:
            Loggerlib.GuiLog.logger.critical("ConfigHandler.write_cfg_file write json: " + str(e))

    def read_cfg_file(self):
        try:
            with open(self.cfg_path, 'r') as f:
                data_dict = json.load(f)
        except:
            data_dict = {}
        return data_dict

def test_json_dict_convert():
    generalValueMatrix = {   'PH' : { ('value'): 5.8, ('+/-'): 0.1, ('dim'): '-' },\
                         'EC' : { ('value'): 1.8, ('+/-'): 0.1, ('dim'): 'mS/cm' },\
                         'waterTemp' : { ('value'): 25, ('+/-'): 1, ('dim'): 'C' },\
                         'airTemp' : { ('value'): 25, ('+/-'): 1, ('dim'): 'C' },\
                         'light' : { ('value'): 600, ('+/-'): 10, ('dim'): 'lm' },\
                         'hum' : { ('value'): 20, ('+/-'): 1, ('dim'): '%' },\
                         'waterlvl' : { ('value'): 20, ('+/-'): 2, ('dim'): 'cm'}, \
                         'PH+': {('value'): 5, ('dim'): 'ml'}, \
                         'PH-': {('value'): 5, ('dim'): 'ml'}
    }

    nutritionValuesMatrix = {'week1' : { ('hydroA'): 10, ('hydroB'): 10, ('EC'): 1.4, ('state'): 'grow' ,('dim'): 'ml' },\
                         'week2' : { ('hydroA'): 10, ('hydroB'): 10, ('EC'): 1.4, ('state'): 'grow' ,('dim'): 'ml' },\
                         'week3' : { ('hydroA'): 12, ('hydroB'): 12, ('EC'): 1.5, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week4': { ('hydroA'): 14, ('hydroB'): 14, ('EC'): 1.7, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week5': { ('hydroA'): 16, ('hydroB'): 16, ('EC'): 1.9, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week6': { ('hydroA'): 14, ('hydroB'): 14, ('EC'): 2.1, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week7': { ('hydroA'): 16, ('hydroB'): 16, ('EC'): 2.2, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week8': { ('hydroA'): 16, ('hydroB'): 16, ('EC'): 2.2, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week9': { ('hydroA'): 16, ('hydroB'): 16, ('EC'): 2.2, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week10': { ('hydroA'): 16, ('hydroB'): 16, ('EC'): 2.2, ('state'): 'bloom' ,('dim'): 'ml' }, \
                         'week11': { ('hydroA'): 0, ('hydroB'): 0, ('EC'): '', ('state'): 'harvest' ,('dim'): 'ml' },\
    }

    generalValueMatrix_obj = ConfigHandler(generalValue_path)
    print("GENERATE: generalValue.json")
    for key in generalValueMatrix:
        print("generate - general: " + str(key) + " - " + str(generalValueMatrix[key]))
        generalValueMatrix_obj.put(key, generalValueMatrix[key])
    print(">>>>>>>>>>>>>>>>\n" + str(generalValueMatrix_obj.get_all()))

    nutritionValuesMatrix_obj = ConfigHandler(nutritionValues_path)
    print("GENERATE: nutritionValues.json")
    for key in nutritionValuesMatrix:
        print("generate - nutrition: " + str(key) + " - " + str(nutritionValuesMatrix[key]))
        nutritionValuesMatrix_obj.put(key, nutritionValuesMatrix[key])
    print(">>>>>>>>>>>>>>>>\n" + str(nutritionValuesMatrix_obj.get_all()))
    fromjson = nutritionValuesMatrix_obj.get_all()
    print("<><><><><>" + str(fromjson["week1"]))

    # Check json module - nutritionValuesMatrix
    dict1 = nutritionValuesMatrix_obj.get_all()
    dict2 = nutritionValuesMatrix
    diffkeys = [k for k in dict1 if dict1[k] != dict2[k]]
    if len(diffkeys) != 0:
        for k in diffkeys:
            print(str(k) + ':' +  str(dict1[k]) + '->' + str(dict2[k]))
    else:
        print("directorys equel nutritionValuesMatrix - nodiff")

    # Check json module - generalValueMatrix
    dict1 = generalValueMatrix_obj.get_all()
    dict2 = generalValueMatrix
    diffkeys = [k for k in dict1 if dict1[k] != dict2[k]]
    if len(diffkeys) != 0:
        for k in diffkeys:
            print(str(k) + ':' +  str(dict1[k]) + '->' + str(dict2[k]))
    else:
        print("directorys equel generalValueMatrix - nodiff")

if "Configlib" in __name__:
    generalValueMatrix_obj = ConfigHandler(generalValue_path)
    nutritionValuesMatrix_obj = ConfigHandler(nutritionValues_path)

if __name__ in "__main__":
    test_json_dict_convert()

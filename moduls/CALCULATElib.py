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

def SensorValue_Checker(tag, sensorValue, week):

    global generalValueMatrix, nutritionValuesMatrix

    isCritical = False
    state = nutritionValuesMatrix['week' + str(week)]['state']
    top = CalculateByTag(tag, week, 'top')
    bottom = CalculateByTag(tag, week, 'bottom')
    differemnce = GetOptimalValue(tag, week) - sensorValue

    if bottom <= sensorValue <= top:
        print("OK - tag: " + tag + " value: " + str(sensorValue) + " state: " + state + ", ragne: " + str(bottom) + " - " + str(top)\
              + " differnece: " + str(differemnce) + " week: " + str(week))
        return differemnce, isCritical
    else:
        print("WARNING - tag: " + tag + " value: " + str(sensorValue) + " state: " + state + ", ragne: " + str(bottom) + " - " + str(top) \
              + " differnece: " + str(differemnce) + " week: " + str(week))
        isCritical = True
        return differemnce, isCritical


def CalculateByTag(tag, week, mode):

    #calculate from general datas
    if mode == 'top':
        data = generalValueMatrix[tag]['value'] + generalValueMatrix[tag]['+/-']
    elif mode == 'bottom':
        data = generalValueMatrix[tag]['value'] - generalValueMatrix[tag]['+/-']

    # override data - EC is weekly value...
    if tag == 'EC':
        if mode == 'top':
            data = nutritionValuesMatrix['week'+str(week)]['EC'] + generalValueMatrix[tag]['+/-']
        elif mode == 'bottom':
            data = nutritionValuesMatrix['week'+str(week)]['EC'] - generalValueMatrix[tag]['+/-']

    return data

def GetOptimalValue(tag, week):

    data = generalValueMatrix[tag]['value']
    # override with weekly data
    if tag == 'EC':
        data = nutritionValuesMatrix['week'+str(week)]['EC']
    return data

def RunValueChacker(week, mPH, mEC, mwTemp, maTemp, mlight, mhum, mwaterlvl):

    resultDisct = {}

    resultDisct['PH', 'diff'], resultDisct['PH', 'isCritic'] = SensorValue_Checker('PH', mPH, week)
    resultDisct['EC', 'diff'], resultDisct['EC', 'isCritic'] = SensorValue_Checker('EC', mEC, week)
    resultDisct['waterTemp', 'diff'], resultDisct['waterTemp', 'isCritic'] = SensorValue_Checker('waterTemp', mwTemp, week)
    resultDisct['airTemp', 'diff'], resultDisct['airTemp', 'isCritic'] = SensorValue_Checker('airTemp', maTemp, week)
    resultDisct['light', 'diff'], resultDisct['light', 'isCritic'] = SensorValue_Checker('light', mlight, week)
    resultDisct['hum', 'diff'], resultDisct['hum', 'isCritic'] = SensorValue_Checker('hum', mhum, week)
    resultDisct['waterlvl', 'diff'], resultDisct['waterlvl', 'isCritic'] = SensorValue_Checker('waterlvl', mwaterlvl, week)

    return resultDisct


def WeeklyProcess(week):
    global nutritionValuesMatrix, eneralValueMatrix

    default_wait_time="10 minute"

    text = "Add 1/3 part destilled and 2/3 part tap water to the sytem\n"\
            + "add hydroA " + str(nutritionValuesMatrix['week'+str(week)]['hydroA']) + " " + str(nutritionValuesMatrix['week'+str(week)]['dim']) + "\n"\
            + "wait " + default_wait_time + "\n"\
            + "add hydroB " + str(nutritionValuesMatrix['week'+str(week)]['hydroB']) + " " + str(nutritionValuesMatrix['week'+str(week)]['dim']) + "\n"\
            + "this is a " +  str(nutritionValuesMatrix['week'+str(week)]['state']) + " status\n"\
            + "EC need to be " + str(nutritionValuesMatrix['week'+str(week)]['EC']) + " " + str(generalValueMatrix['EC']['dim'])

    return text + "\n"

def GetDataBaseString():
    universalDataString=">>>Univeral Data Settings:\n"
    WeeklyDataString=">>>Weekly Data Settings:\n"

    #get universal settings
    for key, value in generalValueMatrix.items():
        #print(">>>Univeral Data Settings:\n" + str(key) + "\t" + " <-> " + str(value))
        universalDataString += str(key) + "\t" + " <-> " + str(value) + "\n"

    # get universal settings
    for key, value in nutritionValuesMatrix.items():
        #print(">>>Weekly Data Settings:\n" + str(key) + "\t" + " <-> " + str(value))
        WeeklyDataString += str(key) + "\t" + " <-> " + str(value) + "\n"

    print(universalDataString + "\n" + WeeklyDataString)
    return universalDataString + "\n" + WeeklyDataString

if __name__ == "__main__":
    #SensorValue_Checker('PH', 5.8, 1)
    #SensorValue_Checker('EC', 1.8, 1)

    #restult = RunValueChacker(1, 5.8, 3, 25, 25, 600, 20, 10)
    #print(restult)
    #WeeklyProcess(1)

    GetDataBaseString()

# HcSMeasurement
Measure system for hydrophonic growing systems. Collect and visualize data with smart data monitoring.

Main Window
![main_window](https://github.com/BxNxM/HcSMeasurement/blob/master/demo_images/HcSmainScreen.png?raw=true)

Settings Window
![settings_window](https://github.com/BxNxM/HcSMeasurement/blob/master/demo_images/HcSsettingsScreen.png?raw=true)


* install python3

```
sudo apt-get install python3
```
Tkinter graphic library is built in.

* get git repository

```
cd ~/Destop
https://github.com/BxNxM/HcSMeasurement.git
```

* Create louncger incon on Desktop

```
cd ~/Desktop/HcSMeasurement
./Louncher.sh --create_louncher
```

***For more informations and options***

* Goo to the ~/Desktop/HcSMeasurement folder

```
cd ~/Desktop/HcSMeasurement
./Louncher.sh --man 
``` 

* write your sensors data request calls in:

```
~/Desktop/HcSMeasurement/moduls/DATA_Manager.py
```

* set Database in

```
~/Desktop/HcSMeasurement/config/generalValue.json
~/Desktop/HcSMeasurement/config/nutritionValues.json
```

* sensors color indexing code modification in

```
~/Desktop/HcSMeasurement/moduls/GUIlib.py
line: 
sensor_color=['dark orange', 'green yellow', 'saddle brown', 'dark sea green', "blue", 'pale turquoise','gold', 'LightSkyBlue4', 'light cyan', 'deep pink', 'dark violet', 'LightSteelBlue3']
```

# GIT
git push -u origin master

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import json
from screeninfo import get_monitors

mainPath = os.getcwd()

default_pic = os.path.join(mainPath, "1000014238.png")
default_csv = os.path.join(mainPath, "hymnlist.csv")

monitors = []
for m in get_monitors():
   monitors.append(m.name) 

default_monitor = monitors[len(monitors)-1]

defaultDictionary = {
    'background': default_pic.replace('\\','/'),
    'monitor':  default_monitor,
    'csvFile':  default_csv.replace('\\','/')
}

def read_json_file(filepath):
    try:
        f = open(filepath,'r')
    except FileNotFoundError:
        json_object = json.dumps(defaultDictionary, indent=4)
        with open(filepath, "w") as outfile:
            outfile.write(json_object)

        with open(filepath,'r') as newFile:
            data = json.load(newFile)

    else:
        with f:
            data = json.load(f)

    return data 

def gettingHymnName():
    filepath = 'Setting.json'
    data1 = read_json_file(filepath)

    creatingHymnImage = os.path.join(mainPath,data1['background'])
    hymnPic = creatingHymnImage.replace('\\', "/")

    return hymnPic

def gettingMonitor():
    filepath = 'Setting.json'
    data2 = read_json_file(filepath)
    selectedMonitor = data2['monitor']

    return selectedMonitor

def gettingCSVFile():
    filepath = 'Setting.json'
    data3 = read_json_file(filepath)
    selectedCsvFile = data3['csvFile']

    return selectedCsvFile 





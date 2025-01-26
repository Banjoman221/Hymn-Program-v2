from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import json
from screeninfo import get_monitors

mainPath = os.getcwd()
parentDirectory = os.path.dirname(mainPath)
new_parentDirectory = parentDirectory.replace('\\','/') 
print(parentDirectory.replace('\\','/'))

default_pic = os.path.join(new_parentDirectory,"resources/1000014238.png")
default_csv = os.path.join(new_parentDirectory,"resources/hymnlist.csv")
jsonFile = os.path.join(new_parentDirectory,"backend/Setting.json")

monitors = []
for m in get_monitors():
   monitors.append(m.name) 

default_monitor = monitors[len(monitors)-1]

defaultDictionary = {
    'background': default_pic,
    'monitor':  default_monitor,
    'csvFile':  default_csv
}

def read_json_file(filepath):
    try:
        f = open(filepath,'r')
    except FileNotFoundError:
        json_object = json.dumps(defaultDictionary, indent=4)
        with open(filepath , "w") as outfile:
            outfile.write(json_object)

        with open(filepath,'r') as newFile:
            data = json.load(newFile)
    else:
        with f:
            data = json.load(f)

    return data 

def gettingHymnName():
    data1 = read_json_file(jsonFile)
    creatingHymnImage = os.path.join(mainPath,data1['background'])
    hymnPic = creatingHymnImage.replace('\\', "/")
    return hymnPic

def gettingMonitor():
    data2 = read_json_file(jsonFile)
    selectedMonitor = data2['monitor']
    return selectedMonitor

def gettingCSVFile():
    data3 = read_json_file(jsonFile)
    selectedCsvFile = data3['csvFile']
    return selectedCsvFile 





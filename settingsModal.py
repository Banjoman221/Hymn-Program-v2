from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import json
from screeninfo import get_monitors

mainPath = os.getcwd()
newPath = mainPath.replace('\\','/')
print(mainPath.replace('\\','/'))

dir_backend = os.path.join(newPath,"backend/").replace('\\','/')
default_pic = os.path.join(newPath,"resources/1000014238.png").replace('\\','/')
default_csv = os.path.join(newPath,"resources/hymnlist.csv").replace('\\','/')
default_powerpoint = os.path.join(newPath,"resources/church slides.pptx").replace('\\','/')
jsonFile = os.path.join(newPath,"backend/Setting.json")
slidesJsonFile = os.path.join(newPath,"backend/picsSlides.json")

monitors = []
for m in get_monitors():
   monitors.append(m.name) 

default_monitor = monitors[len(monitors)-1]

defaultDictionary = {
    'background': default_pic,
    'monitor':  default_monitor,
    'csvFile':  default_csv,
    'powerpoint':  default_powerpoint
}

def read_json_file(filepath):
    try:
        f = open(filepath,'r')
    except FileNotFoundError:
        os.mkdir(dir_backend)
        if dir_backend:
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

def gettingSlides():
    data4 = read_json_file(slidesJsonFile)
    selectedSlide = data4['slideShow']
    return selectedSlide 




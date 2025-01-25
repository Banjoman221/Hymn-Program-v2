from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import json

mainPath = os.getcwd()

def read_json_file(filepath):
    with open('Setting.json','r') as file:
        data = json.load(file)
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
    selectedMonitor =data2['monitor']

    return selectedMonitor

def gettingCSVFile():
    filepath = 'Setting.json'
    data3 = read_json_file(filepath)
    selectedCsvFile = data3['csvFile']

    return selectedCsvFile 





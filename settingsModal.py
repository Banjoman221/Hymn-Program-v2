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
    data = read_json_file(filepath)
    # dictionary['background'] = data['background']
    print(data['background'])

    creatingHymnImage = os.path.join(mainPath,data['background'])
    hymnPic = creatingHymnImage.replace('\\', "/")

    return hymnPic

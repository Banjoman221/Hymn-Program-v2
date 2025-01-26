from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import settingsModal as SettingsModal 
import SettingsWindow as settingsWindow
import os, sys
import json
from screeninfo import get_monitors

mainPath = os.getcwd()
parentDirectory = os.path.dirname(mainPath)
jsonFile = os.path.join(parentDirectory, "/resources/Setting.json")

dictionary = {
    'background': SettingsModal.gettingHymnName(),
    'monitor': SettingsModal.gettingMonitor(),
    'csvFile': SettingsModal.gettingCSVFile()
}

def nonPrimaryMonitors():
    monitors = []
    for m in get_monitors():
        if(m.name != SettingsModal.gettingMonitor()):
            monitors.append(m.name)

    return monitors 

def get_CSV_File(self):
    filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "CSV Files (*.csv)")
    if filename:
        print(filename)
        dictionary['csvFile'] = filename
        print(dictionary['csvFile'])

        json_object = json.dumps(dictionary, indent=4)
        with open("Setting.json", "w") as outfile:
            outfile.write(json_object)


class Settings(QWidget):
    def __init__(self,hymnPic):
        super().__init__()
        self.setGeometry(200, 100, 400, 200)
        
        self.layout = QGridLayout()

        self.backGroundPreview = QLabel()
        self.backGroundPreview.setStyleSheet("border-image: url('" + hymnPic + "');")
        self.backGroundPreview.setFixedHeight(180)
        self.backGroundPreview.setFixedWidth(300)
        self.layout.addWidget(self.backGroundPreview, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.backGroundSetting = QLabel(hymnPic)
        self.layout.addWidget(self.backGroundSetting, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.changeBackgroundButton = QPushButton('Upload New BackGround')
        self.changeBackgroundButton.clicked.connect(lambda: self.uploadingNewBackground())
        self.layout.addWidget(self.changeBackgroundButton, 2,0, Qt.AlignmentFlag.AlignRight)

        self.monitorSelectLabel = QLabel('Monitors:')
        self.monitorSelectLabel.setStyleSheet("position:relative;margin-left: 40px;")
        self.layout.addWidget(self.monitorSelectLabel,3,0,Qt.AlignmentFlag.AlignLeft)

        self.monitorSelect = QComboBox()
        self.monitorSelect.addItem(SettingsModal.gettingMonitor())
        self.monitorSelect.addItems(nonPrimaryMonitors())
        self.monitorSelect.setFixedWidth(180)
        self.monitorSelect.activated.connect(self.setMonitorSettings)
        self.layout.addWidget(self.monitorSelect,3,0,Qt.AlignmentFlag.AlignCenter)

        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(lambda: self.savingSetting())
        self.layout.addWidget(self.saveButton , 5,0, Qt.AlignmentFlag.AlignLeft)
        
        self.saveButton = QPushButton('Save and Exit')
        self.saveButton.clicked.connect(lambda: self. savingSettingAndExit())
        self.layout.addWidget(self.saveButton , 5,0, Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.layout)

    def uploadingNewBackground(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *bmp)")
        if filename:
            print(filename)
            newFileName = filename.replace("\\","/")
            hymnPic = newFileName 
            hymnImage = "border-image: url('" + newFileName + "');"

            self.backGroundPreview.setStyleSheet(hymnImage)
            self.backGroundSetting.setText(newFileName)

            dictionary['background'] = newFileName

    def savingSetting(self):
        json_object = json.dumps(dictionary, indent=4)
        with open(jsonFile , "w") as outfile:
            outfile.write(json_object)

    def savingSettingAndExit(self):
        json_object = json.dumps(dictionary, indent=4)
        with open(jsonFile , "w") as outfile:
            outfile.write(json_object)

        self.close()

    def setMonitorSettings(self, index):
        ctext = self.monitorSelect.itemText(index) 
        print(ctext)
        dictionary['monitor'] = ctext   


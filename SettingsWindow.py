from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import settingsModal as SettingsModal
import os, sys
import json
from screeninfo import get_monitors

mainPath = os.getcwd()
new_parentDirectory = mainPath.replace('\\','/') 
print(new_parentDirectory)

jsonFile = os.path.join(new_parentDirectory,"backend/Setting.json")

dictionary = {
    'background': SettingsModal.gettingHymnName(),
    'monitor': SettingsModal.gettingMonitor(),
    'csvFile': SettingsModal.gettingCSVFile(),
    'powerpoint': SettingsModal.gettingPowerpoint(),
    'darkmode': SettingsModal.gettingDarkMode()
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
        with open(jsonFile, "w") as outfile:
            outfile.write(json_object)
    print("importing CSV file......")

def get_Powerpoint(self):
    filename, _ = QFileDialog.getOpenFileName(self, "Select Powerpoint", "", "Powerpoint Files (*.pptx)")
    if filename:
        print(filename)
        dictionary['powerpoint'] = filename
        print(dictionary['powerpoint'])

        json_object = json.dumps(dictionary, indent=4)
        with open(jsonFile, "w") as outfile:
            outfile.write(json_object)

    print("importing powerpoint......")

class Settings(QWidget):
    def __init__(self,hymnPic):
        super().__init__()
        self.setGeometry(200, 100, 500, 400)
        self.setFixedSize(500, 400)
        
        self.layout = QGridLayout()

        self.backGroundPreview = QLabel()
        self.backGroundPreview.setStyleSheet("border-image: url('" + hymnPic + "');")
        self.backGroundPreview.setFixedHeight(180)
        self.backGroundPreview.setFixedWidth(300)
        self.layout.addWidget(self.backGroundPreview, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.backGroundSetting = QLabel(hymnPic)
        self.layout.addWidget(self.backGroundSetting, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.changeBackgroundButton = QPushButton('Upload New BackGround')
        self.changeBackgroundButton.clicked.connect(SettingsModal.safe(lambda: self.uploadingNewBackground()))
        self.layout.addWidget(self.changeBackgroundButton, 2,0, Qt.AlignmentFlag.AlignRight)

        self.settingsRow = QHBoxLayout()
        self.settingsRow.setSpacing(10)
        self.settingsRow.addWidget(QLabel('Monitors:'))
        self.monitorSelect = QComboBox()
        self.monitorSelect.addItem(SettingsModal.gettingMonitor())
        self.monitorSelect.addItems(nonPrimaryMonitors())
        self.monitorSelect.setFixedWidth(180)
        self.monitorSelect.activated.connect(SettingsModal.safe(self.setMonitorSettings))
        self.settingsRow.addWidget(self.monitorSelect)
        self.settingsRow.addStretch()
        self.settingsRow.addWidget(QLabel('   Dark Mode:'))
        self.darkModeCheckbox = QCheckBox()
        self.darkModeCheckbox.setChecked(SettingsModal.gettingDarkMode())
        self.darkModeCheckbox.toggled.connect(SettingsModal.safe(self.setDarkModeSetting))
        self.settingsRow.addWidget(self.darkModeCheckbox)

        self.darkLayoutWidget = QWidget()
        self.darkLayoutWidget.setLayout(self.settingsRow)
        self.layout.addWidget(self.darkLayoutWidget, 3, 0, Qt.AlignmentFlag.AlignLeft)

        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(SettingsModal.safe(lambda: self.savingSetting()))
        self.layout.addWidget(self.saveButton , 4,0, Qt.AlignmentFlag.AlignLeft)
        
        self.saveButton = QPushButton('Save and Exit')
        self.saveButton.clicked.connect(SettingsModal.safe(lambda: self. savingSettingAndExit()))
        self.layout.addWidget(self.saveButton , 4,0, Qt.AlignmentFlag.AlignRight)
        
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

    def setDarkModeSetting(self, checked):
        print(checked)
        dictionary['darkmode'] = checked
        SettingsModal.apply_dark_mode(checked)   


from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import json

dictionary = {
    'background': ''
}
class Settings(QWidget):
    def __init__(self,hymnPic,hymnImage):
        super().__init__()

        self.setGeometry(200, 100, 400, 200)

        self.layout = QGridLayout()

        self.backGroundPreview = QLabel()
        self.backGroundPreview.setStyleSheet(hymnPic)
        self.backGroundPreview.setFixedHeight(180)
        self.backGroundPreview.setFixedWidth(300)
        self.layout.addWidget(self.backGroundPreview, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.backGroundSetting = QLabel(hymnImage)
        self.layout.addWidget(self.backGroundSetting, 1, 0, Qt.AlignmentFlag.AlignCenter)

        self.changeBackgroundButton = QPushButton('Upload New BackGround')
        self.changeBackgroundButton.clicked.connect(lambda: self.uploadingNewBackground())
        self.layout.addWidget(self.changeBackgroundButton, 2,0, Qt.AlignmentFlag.AlignRight)
        
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(lambda: self.savingSetting())
        self.layout.addWidget(self.saveButton , 3,0, Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.layout)

    def uploadingNewBackground(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *bmp)")
        if filename:
            print(filename)
            newFileName = filename.replace("\\","/")
            hymnPic = "border-image: url('" + newFileName + "');"

            self.backGroundPreview.setStyleSheet(hymnPic)
            self.backGroundSetting.setText(newFileName)
            dictionary['background'] = newFileName

    def savingSetting(self):
        json_object = json.dumps(dictionary, indent=4)
        with open("Setting.json", "w") as outfile:
            outfile.write(json_object)

        print(dictionary['background'])



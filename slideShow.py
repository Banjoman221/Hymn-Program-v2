from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
from screeninfo import get_monitors

# Getting main path of this folder
mainPath = os.getcwd()
# Getting CSV file
hymn = os.path.join(mainPath,"\jg.jpg")

class Slide(QWidget):

    def __init__(self, theHymn, num):
        super().__init__()
        self.setWindowTitle("Hymn Slide V2")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        backGround = QLabel(self)
        backGround.setPixmap(QPixmap('C:/Users/jedij/Desktop/Hymn-Program-v2/jg.jpg'))
        backGround.setScaledContents(True)
        self.layout.addWidget(backGround, 0, 0)

        hymnName = QLabel(theHymn)
        hymnName.setWordWrap(True)
        hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(hymnName, 0 , 0 , Qt.AlignmentFlag.AlignTop)

        hymnNum = QLabel(num)
        hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(hymnNum, 0, 0, Qt.AlignmentFlag.AlignHCenter)

        for m in get_monitors():
            print(m.width)
            self.monWidth = m.width
            if m.is_primary == False:
                self.move(int(m.x), int(m.y))
                hymnName.move(int(m.x), int(m.y))

        print(self.monWidth)
        if self.monWidth < 3840: 
            if len(theHymn) <= 20:
                hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 250px; padding-top: 70px;")
                hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 250px; margin-top: 50px;")
            elif len(theHymn) >= 20:
                hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 200px; padding-top:100px;")
                hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 200px; padding-bottom: 50px;")
        elif self.monWidth >= 3840:
            if len(theHymn) <= 20:
                hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 190px; padding-top: 50px;")
                hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 250px; margin-top: 50px;")
            elif len(theHymn) >= 20:
                hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 205px; padding-top:275px;")
                hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 200px; padding-bottom: 50px;")
            
        print(len(theHymn))
        self.showMaximized() 
        self.showFullScreen()
        self.show()


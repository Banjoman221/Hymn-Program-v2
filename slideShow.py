from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
from screeninfo import get_monitors


class Slide(QWidget):

    def __init__(self, theHymn, num):
        super().__init__()
        self.setWindowTitle("Hymn Slide V2")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        backGround = QLabel(self)
        backGround.setStyleSheet("border-image: url('C:/Users/jedij/Desktop/Hymn-Program-v2/bg.jpg');")
        backGround.setScaledContents(True)
        self.layout.addWidget(backGround, 0, 0)

        hymnName = QLabel(theHymn)
        hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 125px; padding-top:200px; padding-top:150px;")
        hymnName.setWordWrap(True)
        hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(hymnName, 0 , 0 , Qt.AlignmentFlag.AlignTop)

        hymnNum = QLabel(num)
        hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 200px;padding-bottom:50px;")
        hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(hymnNum, 0, 0, Qt.AlignmentFlag.AlignHCenter)
        
        for m in get_monitors():
            if m.is_primary == False:
                self.move(int(m.x), int(m.y))
                hymnName.move(int(m.x), int(m.y))

        self.showMaximized() 
        self.showFullScreen()
        self.show()


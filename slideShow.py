from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
from screeninfo import get_monitors

# Getting main path of this folder
mainPath = os.getcwd()
# Getting CSV file
hymn = os.path.join(mainPath,"jg.jpg")
print(hymn)
class Slide(QMainWindow):

    def __init__(self, theHymn, num):
        super().__init__()
        self.setWindowTitle("Hymn Slide V2")

        self.layout = QGridLayout()
        self.layoutVertical = QVBoxLayout()

        backGround = QLabel(self)
        backGround.setPixmap(QPixmap(hymn))
        backGround.setScaledContents(True)
        self.layout.addWidget(backGround, 0, 0)

        hymnName = QLabel(theHymn)
        hymnName.setWordWrap(True)
        hymnName.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        hymnName.adjustSize()
        hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 230px;")
        
        if len(theHymn) >= 25:
            hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 210px;margin-top: 20px;")
        if len(theHymn) < 25:
            hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 230px;margin-top: 20px;")
            
        self.layoutVertical.addWidget(hymnName)

        hymnNum = QLabel(num)
        hymnNum.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        hymnNum.adjustSize()
        hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 275px")
        self.layoutVertical.addWidget(hymnNum)

        self.layout.addLayout(self.layoutVertical, 0, 0)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)


        for m in get_monitors():
            print(m.width)
            self.monWidth = m.width
            if m.is_primary == False:
                self.move(int(m.x), int(m.y))
                hymnName.move(int(m.x), int(m.y))

        print(self.monWidth)
        self.showMaximized() 
        self.showFullScreen()
        self.show()


from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import csv
from screeninfo import get_monitors
import slideShow
application_path = os.path.dirname(sys.executable)

# Getting main path of this folder
mainPath = os.path.dirname(__file__)
# Getting CSV file
hymn = os.path.join(mainPath, "hymnlist.csv")
hymnPic = "border-image: url('" + os.path.join(mainPath, "\jg.jpg") + "');"

data = []
theHymn = ""
# Accessing CSV file and adding to an array to be accessed later
with open(hymn, newline="") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        data.append(row)


class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.w = None
        
        # Add label             
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('HymnsOS') 

        self.layout = QGridLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)

        self.preview = QLabel()
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.layout.addWidget(self.preview, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.backGround = QLabel(self)
        self.backGround.setStyleSheet("")

        self.hymnName = QLabel()
        self.hymnName.setText("")
        self.hymnName.setStyleSheet("")

        self.hymnNum = QLabel()
        self.hymnNum.setText("")
        self.hymnNum.setStyleSheet("")
    
        self.le = QLineEdit(self)
        self.le.setPlaceholderText("Enter Page Number:")
        onlyInt = QIntValidator()
        onlyInt.setRange(2, 479)
        self.le.setValidator(onlyInt)
        self.layout.addWidget(self.le, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.le.returnPressed.connect(self.show_new_window2) 
        self.le.returnPressed.connect(self.preview_widget) 
        self.le.textChanged.connect(self.preview_widget3)

        self.btn = QPushButton('Change Hymn', self)
        self.btn.setFixedWidth(130)
        self.layout.addWidget(self.btn, 1, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.btn.clicked.connect(self.preview_widget)  
        self.btn.clicked.connect(self.show_new_window2)  

        self.btn2 = QPushButton('Start Slide Show', self)
        self.btn2.setFixedWidth(275)
        self.layout.addWidget(self.btn2, 2, 0, Qt.AlignmentFlag.AlignJustify | Qt.AlignmentFlag.AlignVCenter)
        self.btn2.clicked.connect(self.preview_widget2)  
        self.btn2.clicked.connect(self.show_new_window)  

        self.btn3 = QPushButton('<<< Front Page', self)
        self.btn3.setFixedWidth(120)
        self.layout.addWidget(self.btn3, 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.btn3.clicked.connect(self.preview_widgetF)  
        self.btn3.clicked.connect(self.show_front_page)  

        self.btn4 = QPushButton('Back Page >>>', self)
        self.btn4.setFixedWidth(120)
        self.layout.addWidget(self.btn4, 3, 0, Qt.AlignmentFlag.AlignRight)
        self.btn4.clicked.connect(self.preview_widgetB)  
        self.btn4.clicked.connect(self.show_back_page)  

        self.show()

    def show_new_window2(self):
        if (self.le.text() != "" and self.w is not None):
            num = int(self.le.text())
            theHymn = str(data[num - 1][0])
            self.w = slideShow.Slide(theHymn, self.le.text())
            self.w.show()
            
    def show_new_window(self):
        if self.w is None:
            if (self.le.text() != "" and int(self.le.text()) <= 479 and int(self.le.text()) > 0):
                    num = int(self.le.text())
                    theHymn = str(data[num - 1][0])
                    self.w = slideShow.Slide(theHymn, self.le.text())            
                    self.btn2.setText('Stop Slide Show')
                    self.w.show()
            else:
                print("try again")
        else:
            self.btn2.setText('Start Slide Show')
            self.preview.setText("No Preview")
            self.preview.setFixedHeight(180)
            self.backGround.setStyleSheet("")
            self.hymnNum.setStyleSheet("")
            self.hymnNum.setText("")
            self.hymnName.setStyleSheet("")
            self.hymnName.setText("")
            self.w.close()
            self.w = None

    def show_front_page(self):
        num = 480
        theHymn = str(data[num - 1][0])
        self.w = slideShow.Slide(theHymn, "Front Page") 
        self.btn2.setText('Stop Slide Show')
        self.w.show()
        
    def show_back_page(self):
        num = 481
        theHymn = str(data[num - 1][0])
        self.w = slideShow.Slide(theHymn, "Back Page") 
        self.btn2.setText('Stop Slide Show')
        self.w.show()

    def preview_widget3(self):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.backGround.setStyleSheet("")
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        if (self.le.text() != ""):
            num = int(self.le.text())
            theHymn = str(data[num - 1][0])
            self.backGround = QLabel(self)
            self.backGround.setStyleSheet(hymnPic)
            self.backGround.setScaledContents(True)
            self.layout.addWidget(self.backGround, 0, 0)

            self.hymnName = QLabel()
            self.hymnName.setText(theHymn)
            self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
            self.hymnName.setWordWrap(True)
            self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.hymnName, 0 , 0 , Qt.AlignmentFlag.AlignTop)

            self.hymnNum = QLabel()
            self.hymnNum.setText(str(num))
            self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
            self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
            self.layout.addWidget(self.hymnNum, 0, 0, Qt.AlignmentFlag.AlignHCenter)

    def preview_widget2(self):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.backGround.setStyleSheet("")
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        if self.w is None:
            if (self.le.text() != "" and int(self.le.text()) <= 479 and int(self.le.text()) > 0):
                num = int(self.le.text())
                theHymn = str(data[num - 1][0])
                self.backGround = QLabel(self)
                self.backGround.setStyleSheet(hymnPic)
                self.backGround.setScaledContents(True)
                self.layout.addWidget(self.backGround, 0, 0)

                self.hymnName = QLabel()
                self.hymnName.setText(theHymn)
                self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
                self.hymnName.setWordWrap(True)
                self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.layout.addWidget(self.hymnName, 0 , 0 , Qt.AlignmentFlag.AlignTop)

                self.hymnNum = QLabel()
                self.hymnNum.setText(str(num))
                self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
                self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
                self.layout.addWidget(self.hymnNum, 0, 0, Qt.AlignmentFlag.AlignHCenter)
            else:
                print("try again")

    def preview_widget(self):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.backGround.setStyleSheet("")
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        if (self.le.text() != "" and self.w is not None):
            num = int(self.le.text())
            theHymn = str(data[num - 1][0])
            self.backGround = QLabel(self)
            self.backGround.setStyleSheet(hymnPic)
            self.backGround.setScaledContents(True)
            self.layout.addWidget(self.backGround, 0, 0)

            self.hymnName = QLabel()
            self.hymnName.setText(theHymn)
            self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
            self.hymnName.setWordWrap(True)
            self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.hymnName, 0 , 0 , Qt.AlignmentFlag.AlignTop)

            self.hymnNum = QLabel()
            self.hymnNum.setText(str(num))
            self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
            self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
            self.layout.addWidget(self.hymnNum, 0, 0, Qt.AlignmentFlag.AlignHCenter)

    def preview_widgetF(self):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.backGround.setStyleSheet("")
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        num = 480
        theHymn = str(data[num - 1][0])
        self.backGround = QLabel(self)
        self.backGround.setStyleSheet(hymnPic)
        self.backGround.setScaledContents(True)
        self.layout.addWidget(self.backGround, 0, 0)

        self.hymnName = QLabel()
        self.hymnName.setText(theHymn)
        self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
        self.hymnName.setWordWrap(True)
        self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.hymnName, 0 , 0 , Qt.AlignmentFlag.AlignTop)

        self.hymnNum = QLabel()
        self.hymnNum.setText("Front Page")
        self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
        self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.hymnNum, 0, 0, Qt.AlignmentFlag.AlignHCenter)

    def preview_widgetB(self):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.backGround.setStyleSheet("")
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        num = 481
        theHymn = str(data[num - 1][0])
        self.backGround = QLabel(self)
        self.backGround.setStyleSheet(hymnPic)
        self.backGround.setScaledContents(True)
        self.layout.addWidget(self.backGround, 0, 0)

        self.hymnName = QLabel()
        self.hymnName.setText(theHymn)
        self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
        self.hymnName.setWordWrap(True)
        self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.hymnName, 0 , 0 , Qt.AlignmentFlag.AlignTop)

        self.hymnNum = QLabel()
        self.hymnNum.setText("Back Page")
        self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
        self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.hymnNum, 0, 0, Qt.AlignmentFlag.AlignHCenter)
    
    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


app = QApplication(sys.argv)

ex = Example()
ex.show()
sys.exit(app.exec())

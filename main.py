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
        data.append(row[0])


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
        self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
        self.preview.setFixedHeight(180)
        self.preview.setFixedWidth(300)
        self.layout.addWidget(self.preview, 0, 1, Qt.AlignmentFlag.AlignCenter)
        self.backGround = QLabel(self)
        self.backGround.setStyleSheet("")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hymnName = QLabel()
        self.hymnName.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnNum = QLabel()
        self.hymnNum.setText("")
        self.hymnNum.setStyleSheet("")
    
        self.placeHold = QLabel('')
        self.placeHold.setFixedWidth(80)
        self.layout.addWidget(self.placeHold, 1, 0, Qt.AlignmentFlag.AlignLeft)

        self.placeHold = QLabel('')
        self.placeHold.setFixedWidth(80)
        self.layout.addWidget(self.placeHold, 1, 2, Qt.AlignmentFlag.AlignLeft)

        self.le = QLineEdit(self)
        self.le.setPlaceholderText("Enter Page Number:")
        onlyInt = QIntValidator()
        onlyInt.setRange(2, 479)
        #self.le.setValidator(onlyInt)
        self.le.setFixedWidth(130)
        self.layout.addWidget(self.le, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        self.le.returnPressed.connect(self.show_new_window_preview) 
        self.le.returnPressed.connect(self.preview_widgetPOnly) 
        self.le.textChanged.connect(self.preview_widgetPOnly)

        self.btn2 = QPushButton('Start Slideshow')
        self.btn2.setFixedWidth(130)
        self.layout.addWidget(self.btn2, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.btn2.clicked.connect(self.preview_widgetStart)  
        self.btn2.clicked.connect(self.show_new_window_start)  

        self.btn3 = QPushButton('<<< Front Page', self)
        self.btn3.setFixedWidth(130)
        self.layout.addWidget(self.btn3, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.btn3.clicked.connect(lambda: self.preview_widgetFB("Front Page"))  
        self.btn3.clicked.connect(lambda: self.show_front_back_page("Front Page"))  

        self.btn4 = QPushButton('Back Page >>>', self)
        self.btn4.setFixedWidth(130)
        self.layout.addWidget(self.btn4, 1, 1, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.btn4.clicked.connect(lambda: self.preview_widgetFB("Back Page"))  
        self.btn4.clicked.connect(lambda: self.show_front_back_page("Back Page"))  

        self.show()

    def show_new_window_preview(self):
        if (self.le.text() != "" and self.w is not None):
            try: 
                self.nnum = int(self.le.text())
                if(self.nnum <= 479 and self.nnum > 0): 
                    self.num = self.nnum
                    self.theHymn = data[self.num - 1]
            except:
                i = 0 
                for x in data:
                    i += 1
                    if self.le.text().lower() in x.lower():
                        self.theHymn = x
                        self.num = i
            self.w = slideShow.Slide(str(self.theHymn), str(self.num))            
            self.btn2.setText('Stop Slide Show')
            self.w.show()
        
    def show_new_window_start(self):
        if (self.le.text() != "" and self.w is None):
            try: 
                self.nnum = int(self.le.text())
                if(self.nnum <= 479 and self.nnum > 0): 
                    self.num = self.nnum
                    self.theHymn = data[self.num - 1]
            except:
                i = 0 
                for x in data:
                    i += 1
                    if self.le.text().lower() in x.lower():
                        self.theHymn = x
                        self.num = i
            self.w = slideShow.Slide(str(self.theHymn), str(self.num))            
            self.btn2.setText('Stop Slide Show')
            self.w.show()
        else:
            self.btn2.setText('Start Slide Show')
            self.preview.setText("No Preview")
            self.preview.setFixedHeight(180)
            self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
            self.backGround.setStyleSheet("")
            self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hymnNum.setStyleSheet("")
            self.hymnNum.setText("")
            self.hymnName.setStyleSheet("")
            self.hymnName.setText("")
            self.w.close()
            self.w = None

    def show_front_back_page(self, hn):
        num = 480
        theHymn = str(data[num - 1])
        self.w = slideShow.Slide(theHymn, hn) 
        self.btn2.setText('Stop Slide Show')
        self.w.show() 

    def preview_widgetPOnly(self):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
        self.backGround.setStyleSheet("")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        self.theHymn = ""
        self.num = ""
        if self.le.text() != "":
            try: 
                self.nnum = int(self.le.text())
                if(self.nnum <= 479 and self.nnum > 0): 
                    self.num = self.nnum
                    self.theHymn = data[self.num - 1]
            except:
                i = 0 
                for x in data:
                    i += 1
                    if self.le.text().lower() in x.lower():
                        self.theHymn = x
                        self.num = i
                        

            self.backGround = QLabel(self)
            self.backGround.setStyleSheet(hymnPic)
            self.backGround.setScaledContents(True)
            self.layout.addWidget(self.backGround, 0, 1)

            self.hymnName = QLabel()
            self.hymnName.setText(str(self.theHymn))
            self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
            self.hymnName.setWordWrap(True)
            self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.hymnName, 0 , 1 , Qt.AlignmentFlag.AlignTop)

            self.hymnNum = QLabel()
            self.hymnNum.setText(str(self.num))
            self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
            self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
            self.layout.addWidget(self.hymnNum, 0, 1, Qt.AlignmentFlag.AlignHCenter)
            

    def preview_widgetStart(self):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
        self.backGround.setStyleSheet("")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        self.theHymn = ""
        self.num = ""
        if self.le.text() != "" and self.w is None:
            try: 
                self.nnum = int(self.le.text())
                if(self.nnum <= 479 and self.nnum > 0): 
                    self.num = self.nnum
                    self.theHymn = data[self.num - 1]
            except:
                i = 0 
                for x in data:
                    i += 1
                    if self.le.text().lower() in x.lower():
                        self.theHymn = x
                        self.num = i
                        

            self.backGround = QLabel(self)
            self.backGround.setStyleSheet(hymnPic)
            self.backGround.setScaledContents(True)
            self.layout.addWidget(self.backGround, 0, 1)

            self.hymnName = QLabel()
            self.hymnName.setText(str(self.theHymn))
            self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
            self.hymnName.setWordWrap(True)
            self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.hymnName, 0 , 1 , Qt.AlignmentFlag.AlignTop)

            self.hymnNum = QLabel()
            self.hymnNum.setText(str(self.num))
            self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
            self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
            self.layout.addWidget(self.hymnNum, 0, 1, Qt.AlignmentFlag.AlignHCenter)
         

    def preview_widgetFB(self, hnfb):
        self.preview.setText("No Preview")
        self.preview.setFixedHeight(180)
        self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
        self.backGround.setStyleSheet("")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hymnNum.setStyleSheet("")
        self.hymnNum.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnName.setText("")
        num = 480
        theHymn = str(data[num - 1])
        self.backGround = QLabel(self)
        self.backGround.setStyleSheet(hymnPic)
        self.backGround.setScaledContents(True)
        self.layout.addWidget(self.backGround, 0, 1)
        self.backGround.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hymnName = QLabel()
        self.hymnName.setText(theHymn)
        self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
        self.hymnName.setWordWrap(True)
        self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.preview, 0, 1, Qt.AlignmentFlag.AlignCenter)


        self.hymnNum = QLabel()
        self.hymnNum.setText(hnfb)
        self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
        self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.layout.addWidget(self.hymnNum, 0, 1, Qt.AlignmentFlag.AlignHCenter) 
    
    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


app = QApplication(sys.argv)

ex = Example()
ex.show()
sys.exit(app.exec())

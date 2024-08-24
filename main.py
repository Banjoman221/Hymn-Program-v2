from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import csv
from screeninfo import get_monitors
import slideShow

# Getting main path of this folder
mainPath = os.getcwd()
# Getting CSV file
hymn = os.path.join(mainPath, "hymnlist.csv")
hymnImage = os.path.join(mainPath,"\jg.jpg")
hymnPic = "border-image: url('" + hymnImage + "');"

data = []
theHymn = ""
# Accessing CSV file and adding to an array to be accessed later
with open(hymn, newline="") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        data.append(row[0].upper())


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.w = None

        # Add label              
        self.setGeometry(400, 200, 300, 375)
        self.setWindowTitle('HymnsOS') 

        self.layout = QGridLayout()
        self.layoutVertical = QVBoxLayout()
        #self.layout.setContentsMargins(10, 10, 10, 10)

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
        self.layout.addWidget(self.placeHold, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.layoutVertical, 0, 0, 1, 1)

        self.le = QLineEdit(self)
        self.le.setFocus()
        self.le.setPlaceholderText("Enter Page Number:")
        onlyInt = QIntValidator()
        onlyInt.setRange(2, 479)
        #self.le.setValidator(onlyInt)
        self.le.setFixedWidth(130)
        self.layoutVertical.addWidget(self.le)
        self.le.returnPressed.connect(lambda: self.show_new_window_start(self.le.text())) 
        self.le.textChanged.connect(self.preview_widgetPOnly)

        self.btn2 = QPushButton('Start Slideshow')
        self.btn2.setFixedWidth(130)
        self.layoutVertical.addWidget(self.btn2)
        self.btn2.clicked.connect(lambda: self.show_new_window_start(self.le.text()))  

        self.btn3 = QPushButton('Front Page Top Song', self)
        self.btn3.setFixedWidth(130)
        self.layoutVertical.addWidget(self.btn3)
        self.btn3.clicked.connect(lambda: self.creating_Preview(hymnPic,"Heaven's Jubilee","Front Page"))  
        self.btn3.clicked.connect(lambda: self.show_front_back_page("Heaven's Jubilee","Front Page"))  

        self.btn4 = QPushButton('Front Page Bottom Song', self)
        self.btn4.setFixedWidth(130)
        self.layoutVertical.addWidget(self.btn4)
        self.btn4.clicked.connect(lambda: self.creating_Preview(hymnPic,"I Feel Like Traveling On","Front Page"))  
        self.btn4.clicked.connect(lambda: self.show_front_back_page("I Feel Like Traveling On","Front Page"))  

        self.btn5 = QPushButton('Back Page ', self)
        self.btn5.setFixedWidth(130)
        self.layoutVertical.addWidget(self.btn5)
        self.btn5.clicked.connect(lambda: self.creating_Preview(hymnPic,"I Know My Name Is There","Back Page"))  
        self.btn5.clicked.connect(lambda: self.show_front_back_page("I Know My Name Is There","Back Page"))  

        self.listHymn = QListWidget()
        self.layout.addWidget(self.listHymn, 1, 1)
        self.listHymn.addItems(data)
        self.listHymn.currentItemChanged.connect(self.printListItems)


        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.show()

    def printListItems(self, i):
        print(i.text())

        j = 0
        for d in data:
            j += 1 
            if i.text().lower() in d.lower():
                self.num = j

        self.creating_Preview(hymnPic, str(i.text()), self.num)
        self.show_new_window_start(str(i.text()))

    #Starting the slideShow from the start slideShow button
    def show_new_window_start(self, hymnName):
        if (hymnName != "" and self.w is None):
            try: 
                self.nnum = int(hymnName)
                if(self.nnum <= 479 and self.nnum > 0): 
                    self.num = self.nnum
                    self.theHymn = data[self.num - 1]
            except:
                i = 0 
                for x in data:
                    i += 1
                    if hymnName.lower() in x.lower():
                        self.theHymn = x
                        self.num = i

            self.w = slideShow.Slide(str(self.theHymn), str(self.num))            
            self.btn2.setText('Stop Slide Show')
            self.w.show()
        elif (self.le.text() != "" or self.btn2.text() == "Stop Slide Show"):
            self.creating_Preview("","","")
            self.btn2.setText('Start Slide Show')
            self.w.close()
            self.w = None

    #Starting the slideShow from the front an back page
    def show_front_back_page(self, hymnName, hymnNum):
        self.w = slideShow.Slide(hymnName, hymnNum) 
        self.w.show() 
        self.btn2.setText('Stop Slide Show')

    #Getting the 
    def preview_widgetPOnly(self):
        self.creating_Preview("","","")
        if self.le.text() != "":
            self.listOfHymn = []

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
                        self.listOfHymn.append(x)
                        self.theHymn = x
                        self.num = i
                    

            self.creating_Preview(hymnPic,self.theHymn, self.num)

            self.listHymn = QListWidget()
            self.layout.addWidget(self.listHymn, 1, 1)
            self.listHymn.addItems(self.listOfHymn)
            self.listHymn.currentItemChanged.connect(self.printListItems)

    #Handling the preview creation
    def creating_Preview(self,hymnPicture, theHymn, theNum):
        self.backGround = QLabel(self)
        self.backGround.setStyleSheet(hymnPicture)
        self.backGround.setScaledContents(True)
        self.layout.addWidget(self.backGround, 0, 1)
        self.backGround.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hymnName = QLabel()
        self.hymnName.setText(theHymn)
        self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
        self.hymnName.setWordWrap(True)
        self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hymnName.adjustSize()
        self.layout.addWidget(self.hymnName, 0, 1, Qt.AlignmentFlag.AlignTop)


        self.hymnNum = QLabel()
        self.hymnNum.setText(str(theNum))
        self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
        self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hymnNum.adjustSize()
        self.layout.addWidget(self.hymnNum, 0, 1, Qt.AlignmentFlag.AlignBottom) 
    
    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()

app = QApplication(sys.argv)
app.setStyle('fusion')

ex = Example()
ex.show()
sys.exit(app.exec())

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import csv
import json
from screeninfo import get_monitors
import slideShow
import SettingsWindow as settingsWindow
import settingsModal as SettingsModal 
import tempfile

import subprocess

mainPath = os.getcwd()

dictionarySlideOut = {
    'slideShow': SettingsModal.gettingSlides(),
}

data = []
data2 = []
theHymn = ""
dataNumbers = 0

# Accessing CSV file and adding to an array to be accessed later
with open(SettingsModal.gettingCSVFile(), newline="") as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        dataNumbers += 1
        data.append(row[0].upper())
        data2.append(str(dataNumbers) + ") " + row[0].upper())

class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.w = None

        # Add label              
        self.setGeometry(300, 100, 500, 500)
        self.setWindowTitle('HymnsOS') 

        #Grid Layout        
        self.layout = QGridLayout()

        self.preview = QLabel()
        self.preview.setText("No Preview")
        self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
        self.preview.setFixedHeight(180)
        self.preview.setFixedWidth(350)
        self.layout.addWidget(self.preview, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.backGround = QLabel(self)
        self.backGround.setStyleSheet("")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.le = QLineEdit(self)
        self.le.setFocus()
        self.le.setPlaceholderText("Enter Page Number or Name of Hymn:")
        self.le.setClearButtonEnabled(True)
        onlyInt = QIntValidator()
        onlyInt.setRange(2, 479)
        #self.le.setValidator(onlyInt)
        self.le.setFixedWidth(300)
        self.le.setFixedHeight(30)
        self.layout.addWidget(self.le, 1,0)
        # self.le.returnPressed.connect(lambda: self.show_new_window_start(self.le.text())) 
        self.le.textChanged.connect(self.preview_widgetPOnly)
        
        self.btn2 = QPushButton('Start')
        self.btn2.setFixedWidth(50)
        self.btn2.setFixedHeight(30)
        self.layout.addWidget(self.btn2,1,0, Qt.AlignmentFlag.AlignRight)
        self.btn2.clicked.connect(lambda: self.show_new_window_start(self.le.text()))  
        #
        # self.btn21 = QPushButton('Add Slide')
        # self.btn21.setFixedWidth(60)
        # self.btn21.setFixedHeight(30)
        # self.layout.addWidget(self.btn21,1,0)
        # self.btn21.clicked.connect(lambda: self.addingSlide(self.le.text()))  
        #
        self.hymnName = QLabel()
        self.hymnName.setText("")
        self.hymnName.setStyleSheet("")
        self.hymnNum = QLabel()
        self.hymnNum.setText("")
        self.hymnNum.setStyleSheet("")

        self.placeHold = QLabel('')
        self.placeHold.setFixedWidth(80)
        self.layout.addWidget(self.placeHold, 0, 0, Qt.AlignmentFlag.AlignLeft)

        self.listHymn = QListWidget()
        self.layout.addWidget(self.listHymn, 2, 0)
        # self.listHymn.addItems(data2)
        self.listHymn.currentItemChanged.connect(self.printListItems)

        self.scroll = QScrollArea()
        self.widget1 = QWidget()
        self.verticallayout = QVBoxLayout()
        self.widget1.setLayout(self.verticallayout)
        print(SettingsModal.gettingSlides())

        for slide in SettingsModal.gettingSlides():
            self.powerpointList = QLabel()
            self.powerpointList.key = slide
            self.powerpointList.setFixedWidth(300)
            self.powerpointList.setFixedHeight(150)
            pixmap = QPixmap(slide)
            self.powerpointList.setPixmap(pixmap)
            self.powerpointList.setScaledContents(True)
            self.powerpointList.mousePressEvent = lambda event,sld=self.powerpointList: self.clickingImage(event,sld)
            self.verticallayout.addWidget(self.powerpointList)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn) 
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        self.scroll.setWidgetResizable(True) 
        self.scroll.setFixedWidth(330)
        self.scroll.setWidget(self.widget1)

        self.layout.addWidget(self.scroll, 0, 1,3,1)

        self.startSlideBtn = QPushButton('Start Slide')
        self.startSlideBtn.clicked.connect(lambda: self.startStopSlides(SettingsModal.gettingSlides()[0]))
        self.layout.addWidget(self.startSlideBtn,3,1,3,1, Qt.AlignmentFlag.AlignLeft)

        self.addSlideButton = QPushButton('Add New Slide')
        self.addSlideButton.clicked.connect(lambda: self.uploadingNewSlide())
        self.layout.addWidget(self.addSlideButton,3,1,3,1, Qt.AlignmentFlag.AlignRight)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Menu
        self.btn3 = QAction('FP Top Song', self)
        self.btn3.triggered.connect(lambda: self.creating_Preview(SettingsModal.gettingHymnName(),"Heaven's Jubilee","Front Page"))  
        self.btn3.triggered.connect(lambda: self.show_front_back_page("Heaven's Jubilee","Front Page"))  

        self.btn4 = QAction('FP Bottom Song', self)
        self.btn4.triggered.connect(lambda: self.creating_Preview(SettingsModal.gettingHymnName(),"I Feel Like Traveling On","Front Page"))  
        self.btn4.triggered.connect(lambda: self.show_front_back_page("I Feel Like Traveling On","Front Page"))  

        self.btn5 = QAction('&Back Page ', self)
        self.btn5.triggered.connect(lambda: self.creating_Preview(SettingsModal.gettingHymnName(),"I Know My Name Is There","Back Page"))  
        self.btn5.triggered.connect(lambda: self.show_front_back_page("I Know My Name Is There","Back Page"))  
        
        self.update = QAction('Update', self)
        self.update.triggered.connect(lambda: self.update_file())  
        
        self.exitAction = QAction('E&xit', self)
        self.exitAction.triggered.connect(lambda: self.close())  
        self.exitAction.setShortcut(QKeySequence("Ctrl+q"))  

        self.settingsAction = QAction('&Settings', self)
        self.settingsAction.triggered.connect(lambda: self.show_settings())  

        self.importCsv = QAction('Import &CSV', self)
        self.importCsv.triggered.connect(lambda: settingsWindow.get_CSV_File(self))

        self.importPowerpoint = QAction('Import &Powerpoint', self)
        self.importPowerpoint.triggered.connect(lambda: settingsWindow.get_Powerpoint(self))

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(self.settingsAction)
        file_menu.addSeparator()
        file_menu.addAction(self.exitAction)

        import_menu = menu.addMenu("&Import")
        import_menu.addAction(self.importCsv)
        import_menu.addSeparator()
        import_menu.addAction(self.importPowerpoint)

        other_menu = menu.addMenu("&Other Pages")
        other_submenu = other_menu.addMenu("&Front Pages")
        other_submenu.addAction(self.btn3)
        other_submenu.addSeparator()
        other_submenu.addAction(self.btn4)
        other_menu.addSeparator()
        other_menu.addAction(self.btn5)

        self.show()

    def addingSlide(self, r):
        if(r):
            print(r)

    def clickingImage(self, event,slide):
        allLabels = self.scroll.findChildren(QLabel)
        for s in allLabels:
            s.setStyleSheet('border-style:none')
        if event.button() == Qt.MouseButton.LeftButton:
            print('1')
            print(slide.key)
            slide.setStyleSheet('border: 5px solid lightblue')
            self.startStopSlides(slide.key)
        if event.button() == Qt.MouseButton.RightButton:
            slide.setStyleSheet('border: 5px solid lightblue')
            print('2')
            context_menu = QMenu(self)
            self.deleteTrigger = QAction("delete", self)
            self.deleteTrigger.triggered.connect(lambda: self.deleteTheSlide(slide))
            context_menu.addAction(self.deleteTrigger)
            context_menu.popup(QCursor.pos())

    def deleteTheSlide(self, j):
        allLabels = self.scroll.findChildren(QLabel)
        for s3 in allLabels:
            if(s3.key == j.key):
                s3.setParent(None)
                print('deleted')

        for d in range(len(dictionarySlideOut['slideShow'])):
            print(d)
            if(dictionarySlideOut['slideShow'][d] == s3.key):
                dictionarySlideOut['slideShow'].remove(s3.key)

        print(dictionarySlideOut['slideShow'])

        json_object = json.dumps(dictionarySlideOut, indent=4)
        with open('./backend/picsSlides.json' , "w") as outfile:
            outfile.write(json_object)


    def startStopSlides(self, i):
        allLabels1 = self.scroll.findChildren(QLabel)
        for s1 in allLabels1:
            s1.setStyleSheet('border-style:none')
        if (self.startSlideBtn.text() == "Start Slide" and i != ""):
            print('showing.....')
            for s2 in allLabels1:
                if(s2.key == i):
                    s2.setStyleSheet('border: 5px solid lightblue')
            self.w = slideShow.Slide('', '',i)            
            self.startSlideBtn.setText('Stop Slide')
            self.w.show()
        elif (self.startSlideBtn.text() == "Stop Slide" and self.w):
            # self.creating_Preview("","","")
            self.startSlideBtn.setText('Start Slide')
            self.w.close()
            self.w = None

    def uploadingNewSlide(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *bmp)")
        if filename:
            print(filename)
            newFileName = filename.replace("\\","/")

            dictionarySlideOut['slideShow'].append(newFileName)

            json_object = json.dumps(dictionarySlideOut, indent=4)
            with open('./backend/picsSlides.json' , "w") as outfile:
                outfile.write(json_object)

            self.powerpointList = QLabel()
            self.powerpointList.key = newFileName
            self.powerpointList.setFixedWidth(300)
            self.powerpointList.setFixedHeight(150)
            pixmap = QPixmap(newFileName)
            self.powerpointList.setPixmap(pixmap)
            self.powerpointList.setScaledContents(True)
            self.powerpointList.mousePressEvent = lambda event,sld=self.powerpointList: self.clickingImage(event,sld)
            self.verticallayout.addWidget(self.powerpointList)


    def show_settings(self):
        self.s = settingsWindow.Settings(SettingsModal.gettingHymnName())
        self.s.show()

    def update_file(self):
        print('updating....')

    def printListItems(self, i):
        print(i.text())

        for j in data2:
            if str(i.text().split(")")[1]).lower() in j.lower():
                self.num = j.split(")")[0]

                self.creating_Preview("","","")
                self.creating_Preview(SettingsModal.gettingHymnName(), str(i.text().split(")")[1]), self.num)
        self.show_new_window_start(str(i.text()))

    #starting the slideshow from the start slideshow button
    def show_new_window_start(self, hymnName):
        print(hymnName)
        if (self.btn2.text() == "Stop" and self.w):
            allLabels1 = self.scroll.findChildren(QLabel)
            for s1 in allLabels1:
                s1.setStyleSheet('border-style:none')
            # self.creating_Preview("","","")
            self.btn2.setText('Start')
            self.w.close()
            self.w = None
        else:
            self.startSlideBtn.setText('Start Slide')
            if (hymnName != ""):
                self.allHymn = []
                for y in data2:
                    if hymnName in y:
                        self.allHymn.append(y)

                print(self.allHymn)
                if len(self.allHymn) != 0:
                    self.theHymn = self.allHymn[0].split(")")[1]
                    self.num = self.allHymn[0].split(")")[0]


                    self.w = slideShow.Slide(str(self.theHymn), str(self.num),SettingsModal.gettingHymnName())            
                    self.btn2.setText('Stop')
                    self.w.show()

    #Starting the slideShow from the front an back page
    def show_front_back_page(self, hymnName, hymnNum):
        self.startSlideBtn.setText('Start Slide')
        self.w = slideShow.Slide(hymnName, hymnNum,SettingsModal.gettingHymnName()) 
        self.w.show() 
        self.btn2.setText('Stop')

    #Getting the 
    def preview_widgetPOnly(self):
        self.creating_Preview("","","")
        if self.le.text() != "":
            self.listOfHymn = []

            for y in data2:
                if str(self.le.text()).lower() in y.lower():
                    self.listOfHymn.append(y)
            
            if len(self.listOfHymn) != 0:
                self.theHymn = self.listOfHymn[0].split(")")[1]
                self.num = self.listOfHymn[0].split(")")[0]

                self.creating_Preview(SettingsModal.gettingHymnName(),self.theHymn, self.num)

            self.listHymn = QListWidget()
            self.layout.addWidget(self.listHymn, 2, 0)
            self.listHymn.addItems(self.listOfHymn)
            self.listHymn.currentItemChanged.connect(self.printListItems) 
        elif self.le.text() == "":
            self.creating_Preview("","","")
        
    #Handling the preview creation
    def creating_Preview(self,hymnPicture, theHymn, theNum):
        if hymnPicture != "" and theHymn != "" and theNum != "":
            self.backGround = QLabel(self)
            self.backGround.setStyleSheet("border-image: url('" + hymnPicture + "');"
)
            self.backGround.setScaledContents(True)
            self.layout.addWidget(self.backGround, 0, 0)
            self.backGround.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.hymnName = QLabel()
            self.hymnName.setText(theHymn)
            # self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 25px; padding-top:30px;")
            self.hymnName.setWordWrap(True)
            self.hymnName.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hymnName.adjustSize()
            self.layout.addWidget(self.hymnName, 0, 0, Qt.AlignmentFlag.AlignTop)

            if len(theHymn) >= 25:
                self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 30px;margin-top: 20px;")
            if len(theHymn) < 25:
                self.hymnName.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;margin-top: 20px;")
                

            self.hymnNum = QLabel()
            self.hymnNum.setText(str(theNum))
            self.hymnNum.setStyleSheet("color: black; font-family: ALGERIAN; font-size: 40px;padding-bottom:5px;")
            self.hymnNum.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hymnNum.adjustSize() 
            self.layout.addWidget(self.hymnNum, 0, 0, Qt.AlignmentFlag.AlignBottom) 
        else:
            self.preview = QLabel()
            self.preview.setText("No Preview")
            self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
            self.preview.setFixedHeight(180)
            self.preview.setFixedWidth(300)
            self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.preview, 0, 0, Qt.AlignmentFlag.AlignCenter)
            self.backGround.setStyleSheet("border-image: none;")

            self.hymnName.setText("")
            self.hymnNum.setText("")       

            self.listHymn = QListWidget()
            self.layout.addWidget(self.listHymn, 2, 0)
            # self.listHymn.addItems(data2)
            self.listHymn.currentItemChanged.connect(self.printListItems)

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()

app = QApplication(sys.argv)
app.setStyle('fusion')

ex = Example()
ex.show()
sys.exit(app.exec())

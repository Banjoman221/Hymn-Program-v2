from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import csv
import slideShow
import SettingsWindow as settingsWindow
import settingsModal as SettingsModal

mainPath = os.getcwd()


data = []
data2 = []
dataNumbers = 0

# Accessing CSV file and adding to an array to be accessed later
try:
    hymn = SettingsModal.gettingCSVFile()
    with open(hymn, newline="") as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            dataNumbers += 1
            data.append(row[0].upper())
            data2.append(str(dataNumbers) + ") " + row[0].upper())
except (FileNotFoundError, IndexError) as e:
    print("Could not load hymn list:", e)


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None

        # Add label
        self.setGeometry(400, 200, 440, 520)
        self.setFixedSize(440, 520)
        self.setWindowTitle("HymnsOS")

        # Grid Layout
        self.layout = QGridLayout()
        self.mainWidgetLayout = QVBoxLayout()
        self.mainWidgetLayout.addLayout(self.layout, 1)

        self.previewWidth = 320
        self.previewHeight = 180  # 16:9 to match fullscreen output

        self.previewContainer = QWidget()
        self.previewContainer.setFixedSize(self.previewWidth, self.previewHeight)
        self.previewLayout = QGridLayout()
        self.previewLayout.setContentsMargins(0, 0, 0, 0)
        self.previewLayout.setSpacing(0)
        self.previewContainer.setLayout(self.previewLayout)
        self.layout.addWidget(
            self.previewContainer, 0, 0, Qt.AlignmentFlag.AlignCenter
        )

        self.backGround = QLabel()
        self.backGround.setScaledContents(True)
        self.backGround.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored
        )
        self.backGround.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previewLayout.addWidget(self.backGround, 0, 0)

        self.previewOverlay = QVBoxLayout()
        self.previewOverlay.setContentsMargins(0, 0, 0, 0)
        self.previewOverlay.setSpacing(0)
        self.previewOverlay.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.previewLayout.addLayout(self.previewOverlay, 0, 0)

        self.hymnName = QLabel()
        self.hymnName.setText("")
        self.hymnName.setWordWrap(True)
        self.hymnName.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.previewOverlay.addWidget(self.hymnName)

        self.hymnNum = QLabel()
        self.hymnNum.setText("")
        self.hymnNum.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        self.previewOverlay.addWidget(self.hymnNum)

        self.preview = QLabel("No Preview", self.previewContainer)
        self.preview.setStyleSheet("font-family: ALGERIAN; font-size: 40px;")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setGeometry(0, 0, self.previewWidth, self.previewHeight)

        self.le = QLineEdit(self)
        self.le.setFocus()
        self.le.setPlaceholderText("Enter Page Number or Name of Hymn:")
        self.le.setClearButtonEnabled(True)
        onlyInt = QIntValidator()
        onlyInt.setRange(2, 479)
        # self.le.setValidator(onlyInt)
        self.le.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.le.setMinimumWidth(0)
        self.le.textChanged.connect(SettingsModal.safe(self.preview_widgetPOnly))

        self.btn2 = QPushButton("Start")
        self.btn2.setFixedWidth(50)
        self.btn2.setFixedHeight(30)
        self.btn2.clicked.connect(
            SettingsModal.safe(lambda: self.show_new_window_start(self.le.text()))
        )

        self.btnAdd = QPushButton("Add")
        self.btnAdd.setFixedWidth(50)
        self.btnAdd.setFixedHeight(30)
        self.btnAdd.setToolTip("Add the selected hymn to the queue")
        self.btnAdd.clicked.connect(SettingsModal.safe(lambda: self.add_to_queue()))

        inputRow = QWidget()
        inputLayout = QHBoxLayout()
        inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setSpacing(6)
        inputLayout.addWidget(self.le, 1)
        inputLayout.addWidget(self.btnAdd, 0)
        inputLayout.addWidget(self.btn2, 0)
        inputRow.setLayout(inputLayout)
        self.layout.addWidget(inputRow, 1, 0)

        self.playlist = []
        self.queueIndex = -1

        self.queuePanel = QVBoxLayout()
        self.queuePanel.setContentsMargins(0, 0, 0, 0)
        self.queuePanel.setSpacing(4)

        self.queueLabel = QLabel("Queue:")
        self.clearAllBtn = QPushButton("Clear All")
        self.clearAllBtn.setFixedWidth(90)
        self.clearAllBtn.clicked.connect(SettingsModal.safe(self.clear_queue))
        queueHeaderLayout = QHBoxLayout()
        queueHeaderLayout.setContentsMargins(0, 0, 0, 0)
        queueHeaderLayout.addWidget(self.queueLabel)
        queueHeaderLayout.addStretch()
        queueHeaderLayout.addWidget(self.clearAllBtn)
        self.queuePanel.addLayout(queueHeaderLayout)

        self.queueList = QListWidget()
        self.queueList.setMinimumHeight(60)
        self.queueList.setMaximumHeight(80)
        self.queueList.itemDoubleClicked.connect(
            SettingsModal.safe(self.remove_from_queue)
        )
        self.queueList.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.queueList.customContextMenuRequested.connect(
            SettingsModal.safe(self.queue_context_menu)
        )
        self.queuePanel.addWidget(self.queueList, 1)

        self.prevBtn = QPushButton("< Prev")
        self.nextBtn = QPushButton("Next >")
        self.prevBtn.setFixedWidth(60)
        self.nextBtn.setFixedWidth(60)
        self.prevBtn.clicked.connect(SettingsModal.safe(self.prev_in_queue))
        self.nextBtn.clicked.connect(SettingsModal.safe(self.next_in_queue))
        queueNavLayout = QHBoxLayout()
        queueNavLayout.setContentsMargins(0, 0, 0, 0)
        queueNavLayout.addWidget(self.prevBtn)
        queueNavLayout.addStretch()
        queueNavLayout.addWidget(self.nextBtn)
        self.queuePanel.addLayout(queueNavLayout)

        self.mainWidgetLayout.addLayout(self.queuePanel)

        self.listHymn = QListWidget()
        self.listHymn.addItems(data2)
        self.layout.addWidget(self.listHymn, 2, 0)
        self.listHymn.currentItemChanged.connect(SettingsModal.safe(self.printListItems))

        self.widget = QWidget()
        self.widget.setLayout(self.mainWidgetLayout)
        self.setCentralWidget(self.widget)

        # Menu
        self.btn3 = QAction("FP Top Song", self)
        self.btn3.triggered.connect(
            SettingsModal.safe(
                lambda: self.creating_Preview(
                    SettingsModal.gettingHymnName(), "Heaven's Jubilee", "Front Page"
                )
            )
        )
        self.btn3.triggered.connect(
            SettingsModal.safe(
                lambda: self.show_front_back_page("Heaven's Jubilee", "Front Page")
            )
        )

        self.btn4 = QAction("FP Bottom Song", self)
        self.btn4.triggered.connect(
            SettingsModal.safe(
                lambda: self.creating_Preview(
                    SettingsModal.gettingHymnName(),
                    "I Feel Like Traveling On",
                    "Front Page",
                )
            )
        )
        self.btn4.triggered.connect(
            SettingsModal.safe(
                lambda: self.show_front_back_page(
                    "I Feel Like Traveling On", "Front Page"
                )
            )
        )

        self.btn5 = QAction("&Back Page ", self)
        self.btn5.triggered.connect(
            SettingsModal.safe(
                lambda: self.creating_Preview(
                    SettingsModal.gettingHymnName(),
                    "I Know My Name Is There",
                    "Back Page",
                )
            )
        )
        self.btn5.triggered.connect(
            SettingsModal.safe(
                lambda: self.show_front_back_page(
                    "I Know My Name Is There", "Back Page"
                )
            )
        )

        self.update = QAction("Update", self)
        self.update.triggered.connect(SettingsModal.safe(lambda: self.update_file()))

        self.exitAction = QAction("E&xit", self)
        self.exitAction.triggered.connect(SettingsModal.safe(lambda: self.close()))
        self.exitAction.setShortcut(QKeySequence("Ctrl+q"))

        self.settingsAction = QAction("&Settings", self)
        self.settingsAction.triggered.connect(SettingsModal.safe(lambda: self.show_settings()))

        self.importCsv = QAction("Import &CSV", self)
        self.importCsv.triggered.connect(
            SettingsModal.safe(lambda: settingsWindow.get_CSV_File(self))
        )

        self.importPowerpoint = QAction("Import &Powerpoint", self)
        self.importPowerpoint.triggered.connect(
            SettingsModal.safe(lambda: settingsWindow.get_Powerpoint(self))
        )

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

    def showPowerPoint(self, ppi):
        print("showing.....")
        print(ppi)
        if self.btn2.text() == "Start":
            self.w = slideShow.Slide("", "", ppi)
            self.btn2.setText("Stop")
            self.w.closed.connect(self.on_slide_closed)
            self.w.show()
        elif self.btn2.text() == "Stop":
            # self.creating_Preview("","","")
            self.btn2.setText("Start")
            self.w.close()
            self.w = None

    def on_slide_closed(self):
        self.btn2.setText("Start")
        self.listHymn.clearSelection()
        self.creating_Preview("", "", "")
        self.le.clear()

    def play_index(self, idx):
        if idx < 0 or idx >= len(self.playlist):
            return False
        self.queueIndex = idx
        self.queueList.setCurrentRow(idx)
        entry = self.playlist[idx]
        hymn = str(entry.split(")")[1])
        num = str(entry.split(")")[0])
        self.w = slideShow.Slide(hymn, num, SettingsModal.gettingHymnName())
        self.w.closed.connect(self.on_slide_closed)
        self.btn2.setText("Stop")
        self.w.show()
        return True

    def next_in_queue(self):
        if not self.playlist:
            return
        if self.w:
            self.w.close()
        nxt = self.queueIndex + 1
        if nxt >= len(self.playlist):
            self.queueIndex = -1
            self.queueList.clearSelection()
            self.btn2.setText("Start")
            return
        self.play_index(nxt)

    def prev_in_queue(self):
        if not self.playlist:
            return
        if self.queueIndex <= 0:
            return
        if self.w:
            self.w.close()
        self.play_index(self.queueIndex - 1)

    def add_to_queue(self):
        entry = self.current_selection()
        if entry is None:
            QMessageBox.warning(
                self,
                "No Hymn Selected",
                "Select or type a hymn to add to the queue first.",
            )
            return
        self.playlist.append(entry)
        self.queueList.addItem(entry)

    def remove_from_queue(self, item):
        row = self.queueList.row(item)
        self.queueList.takeItem(row)
        self.playlist.pop(row)
        if self.queueIndex > row:
            self.queueIndex -= 1
        elif self.queueIndex == row:
            self.queueIndex = -1
            if self.w:
                self.w.close()
        self.creating_Preview("", "", "")

    def current_selection(self):
        text = ""
        item = self.listHymn.currentItem()
        if item:
            text = item.text()
        if text == "":
            text = self.le.text().strip()
        if text == "":
            return None
        matches = [y for y in data2 if text.lower() in y.lower()]
        if not matches:
            return None
        return matches[0]

    def clear_queue(self):
        self.playlist.clear()
        self.queueList.clear()
        self.queueIndex = -1
        if self.w:
            self.w.close()
        self.creating_Preview("", "", "")

    def queue_context_menu(self, pos):
        item = self.queueList.itemAt(pos)
        if item is None:
            return
        menu = QMenu(self)
        deleteAction = menu.addAction("Delete")
        action = menu.exec(self.queueList.mapToGlobal(pos))
        if action == deleteAction:
            self.remove_from_queue(item)

    def show_settings(self):
        self.s = settingsWindow.Settings(SettingsModal.gettingHymnName())
        self.s.show()

    def update_file(self):
        print("updating....")

    def printListItems(self, i):
        if i is None:
            return
        print(i.text())

        for j in data2:
            if str(i.text().split(")")[1]).lower() in j.lower():
                self.num = j.split(")")[0]

                self.creating_Preview("", "", "")
                self.creating_Preview(
                    SettingsModal.gettingHymnName(),
                    str(i.text().split(")")[1]),
                    self.num,
                )

# Starting the slideShow from the start slideShow button
    def show_new_window_start(self, hymnName):
        print(hymnName)
        if self.btn2.text() == "Start":
            if self.playlist:
                self.queueIndex = -1
                self.play_index(0)
                return

            entry = self.current_selection()
            if entry is None:
                QMessageBox.warning(
                    self,
                    "No Hymn Selected",
                    "Please select a hymn or type a hymn name/number first.",
                )
                return

            self.theHymn = str(entry.split(")")[1])
            self.num = str(entry.split(")")[0])

            self.w = slideShow.Slide(
                str(self.theHymn),
                str(self.num),
                SettingsModal.gettingHymnName(),
            )
            self.btn2.setText("Stop")
            self.w.closed.connect(self.on_slide_closed)
            self.w.show()
        elif self.btn2.text() == "Stop":
            # self.creating_Preview("","","")
            self.btn2.setText("Start")
            self.w.close()
            self.w = None

    # Starting the slideShow from the front an back page
    def show_front_back_page(self, hymnName, hymnNum):
        self.w = slideShow.Slide(hymnName, hymnNum, SettingsModal.gettingHymnName())
        self.w.closed.connect(self.on_slide_closed)
        self.w.show()
        self.btn2.setText("Stop")

    # Getting the
    def preview_widgetPOnly(self):
        self.creating_Preview("", "", "")
        if self.le.text() != "":
            self.listOfHymn = []

            for y in data2:
                if str(self.le.text()).lower() in y.lower():
                    self.listOfHymn.append(y)

            if len(self.listOfHymn) != 0:
                self.theHymn = self.listOfHymn[0].split(")")[1]
                self.num = self.listOfHymn[0].split(")")[0]

                self.creating_Preview(
                    SettingsModal.gettingHymnName(), self.theHymn, self.num
                )

            self.listHymn.clear()
            self.listHymn.addItems(self.listOfHymn)
        elif self.le.text() == "":
            self.creating_Preview("", "", "")
            self.listHymn.clear()
            self.listHymn.addItems(data2)

    # Handling the preview creation
    # Mirrors slideShow.Slide: same background pixmap handling, same
    # centered overlay layout, same font-size math scaled to preview size.
    def creating_Preview(self, hymnPicture, theHymn, theNum):
        if hymnPicture != "" and theHymn != "" and theNum != "":
            scale = self.previewWidth / slideShow.Slide.BASE_WIDTH
            nameSize, numSize, topMargin = slideShow.Slide.font_sizes(
                theHymn, scale
            )

            self.backGround.setPixmap(QPixmap(hymnPicture))
            self.backGround.setScaledContents(True)

            self.hymnName.setText(theHymn)
            self.hymnName.setWordWrap(True)
            self.hymnName.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
            )
            self.hymnName.adjustSize()
            self.hymnName.setStyleSheet(
                f"color: black; font-family: ALGERIAN; font-size: {nameSize}px;"
                f"margin-top: {topMargin}px;"
            )

            self.hymnNum.setText(str(theNum))
            self.hymnNum.setStyleSheet(
                f"color: black; font-family: ALGERIAN; font-size: {numSize}px"
            )
            self.hymnNum.setAlignment(
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
            )
            self.hymnNum.adjustSize()
            self.preview.setText("")
            self.preview.hide()
        else:
            self.preview.setText("No Preview")
            self.preview.show()
            self.preview.raise_()
            self.backGround.setPixmap(QPixmap())
            self.backGround.setStyleSheet("")

            self.hymnName.setText("")
            self.hymnNum.setText("")

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()


app = QApplication(sys.argv)
app.setStyle("fusion")
sys.excepthook = SettingsModal.excepthook

SettingsModal.apply_dark_mode(SettingsModal.gettingDarkMode())

ex = Example()
SettingsModal.style_line_edits(SettingsModal.gettingDarkMode())
ex.show()
sys.exit(app.exec())

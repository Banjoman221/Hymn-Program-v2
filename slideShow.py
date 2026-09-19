from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import settingsModal as SettingsModal
import os, sys
import json
from screeninfo import get_monitors


class Slide(QMainWindow):
    closed = pyqtSignal()

    def __init__(self, theHymn, num, hymnPic):
        super().__init__()
        self.setWindowTitle("Hymn Slide V2")

        monWidth = 1920
        for m in get_monitors():
            print(m.width)
            if m.name == SettingsModal.gettingMonitor():
                monWidth = m.width
                self.move(int(m.x), int(m.y))

        scale = monWidth / 1920.0

        self.layout = QGridLayout()
        self.layoutVertical = QVBoxLayout()

        backGround = QLabel(self)
        backGround.setPixmap(QPixmap(hymnPic))
        backGround.setScaledContents(True)
        self.layout.addWidget(backGround, 0, 0)

        hymnName = QLabel(theHymn)
        hymnName.setWordWrap(True)
        hymnName.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        hymnName.adjustSize()

        nameSize = int(230 * scale)
        if len(theHymn) >= 25:
            nameSize = int(200 * scale)

        hymnName.setStyleSheet(
            f"color: black; font-family: ALGERIAN; font-size: {nameSize}px;margin-top: {int(40 * scale)}px;"
        )

        self.layoutVertical.addWidget(hymnName)

        hymnNum = QLabel(num)
        hymnNum.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )
        hymnNum.adjustSize()
        numSize = int(275 * scale)
        hymnNum.setStyleSheet(
            f"color: black; font-family: ALGERIAN; font-size: {numSize}px"
        )
        self.layoutVertical.addWidget(hymnNum)

        self.layout.addLayout(self.layoutVertical, 0, 0)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        print(monWidth)
        self.showMaximized()
        self.showFullScreen()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

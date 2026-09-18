from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, sys
import json
import inspect
import traceback
from screeninfo import get_monitors


def safe(func):
    def wrapper(*args, **kwargs):
        try:
            params = list(inspect.signature(func).parameters.values())
            has_varargs = any(p.kind == p.VAR_POSITIONAL for p in params)
            if not has_varargs:
                max_pos = sum(
                    1
                    for p in params
                    if p.kind
                    in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                )
                if len(args) > max_pos:
                    args = args[:max_pos]
            return func(*args, **kwargs)
        except Exception:
            traceback.print_exc()

    return wrapper


def excepthook(exc_type, exc_value, exc_tb):
    traceback.print_exception(exc_type, exc_value, exc_tb)

mainPath = os.getcwd()
newPath = mainPath.replace("\\", "/")
print(mainPath.replace("\\", "/"))

dir_backend = os.path.join(newPath, "backend/").replace("\\", "/")
default_pic = os.path.join(newPath, "resources/1000014238.png").replace("\\", "/")
default_csv = os.path.join(newPath, "resources/hymnlist.csv").replace("\\", "/")
default_powerpoint = os.path.join(newPath, "resources/church slides.pptx").replace(
    "\\", "/"
)
jsonFile = os.path.join(newPath, "backend/Setting.json")

monitors = []
for m in get_monitors():
    monitors.append(m.name)

default_monitor = monitors[len(monitors) - 1]

defaultDictionary = {
    "background": default_pic,
    "monitor": default_monitor,
    "csvFile": default_csv,
    "powerpoint": default_powerpoint,
    "darkmode": False,
}


def style_line_edits(enabled):
    if enabled:
        style = (
            "QLineEdit { color: white; } "
            "QLineEdit::placeholder { color: white; }"
        )
    else:
        style = ""
    for widget in QApplication.allWidgets():
        if isinstance(widget, QLineEdit):
            widget.setStyleSheet(style)


def apply_dark_mode(enabled):
    app = QApplication.instance()
    if enabled:
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(palette)
    else:
        app.setPalette(app.style().standardPalette())

    style_line_edits(enabled)


def read_json_file(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        os.makedirs(dir_backend, exist_ok=True)
        json_object = json.dumps(defaultDictionary, indent=4)
        with open(filepath, "w") as outfile:
            outfile.write(json_object)

        with open(filepath, "r") as newFile:
            data = json.load(newFile)

    return data


def gettingHymnName():
    data1 = read_json_file(jsonFile)
    creatingHymnImage = os.path.join(mainPath, data1["background"])
    hymnPic = creatingHymnImage.replace("\\", "/")
    return hymnPic


def gettingMonitor():
    data2 = read_json_file(jsonFile)
    selectedMonitor = data2["monitor"]
    return selectedMonitor


def gettingCSVFile():
    data3 = read_json_file(jsonFile)
    selectedCsvFile = data3["csvFile"]
    return selectedCsvFile


def gettingPowerpoint():
    data4 = read_json_file(jsonFile)
    selectedPowerpointFile = data4["powerpoint"]
    return selectedPowerpointFile


def gettingDarkMode():
    data5 = read_json_file(jsonFile)
    darkMode = data5.get("darkmode", False)
    return darkMode

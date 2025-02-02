from __future__ import annotations

from cx_Freeze import setup, Executable

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None

include_files = [("./resources/hymnlist.csv","./resources/hymnlist.csv"),("./resources/jg.jpg","./resources/jg.jpg"),("./resources/1000014238.png","./resources/1000014238.png"),("./resources/gospel.ico","./resources/gospel.ico")]

if get_qt_plugins_paths:
    # Inclusion of extra plugins (since cx_Freeze 6.8b2)
    # cx_Freeze automatically imports the following plugins depending on the
    # module used, but suppose we need the following:
    include_files += get_qt_plugins_paths("PyQt6", "multimedia")

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "HymnOS",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]HymnOS.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     "./resources/gospel.ico",   # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {
    "Shortcut": shortcut_table,
    "ProgId": [
        ("Prog.Id", None, None, "This is a description", "IconId", None),
    ],
    "Icon": [
        ("IconId", "./resources/gospel.ico"),
    ],
}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

# build_exe_options = {"excludes": ["tkinter", "unittest", "email", "http", "xml", "pydoc"],"include_msvcr": True, "include_files": include_files}

executables = [
    Executable(
        "main.py",
        copyright="Copyright (C) 2025 cx_Freeze",
        base="Win32Gui",
        icon="./resources/gospel.ico",
        # shortcut_dir="DekstopFolder",
        # shortcut_name="HymnOS",
    )
]

setup(
    name="HymnOS",
    version="0.1",
    description="A Powerpoint type program for displaying Hymns",
    executables=executables,
    options={
        "build_exe": {
                "packages":["PyQt6"],
                "include_files":include_files
            },
        "bdist_msi":bdist_msi_options
    },
)

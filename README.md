# HymnOS

A fullscreen hymn display application built with **Python** and **PyQt6**. Designed for churches and congregations, HymnOS puts the current hymn name and page number on a projector or secondary monitor so nobody misses the page turn.

## Features

- **Instant search** — search hymns by name or page number as you type
- **Live preview** — see the hymn rendered on the background before you show it
- **Fullscreen display** — sends the hymn to your projector or selected secondary monitor
- **Playlist queue** — build a list of upcoming hymns, navigate with <kbd>Prev</kbd>/<kbd>Next</kbd>, and remove items with a right-click
- **Dark mode** — toggle a dark theme from Settings (persisted between sessions)
- **Custom backgrounds** — upload your own image to render hymn slides on
- **Multi-monitor** — choose exactly which monitor the display uses
- **CSV import** — load your church's hymn book from a CSV file
- **PowerPoint import** — use slides from a `.pptx` file

## Requirements

- [Python 3.12](https://www.python.org/downloads/) (or newer)
- PyQt6

## Installation

```bash
pip install PyQt6
```

## Running

Clone the repository and run:

```bash
git clone https://github.com/Banjoman221/Hymn-Program-v2.git
cd Hymn-Program-v2
python main.py
```

## Usage

1. **Find a hymn** — type a page number or hymn name in the search box. Matching hymns appear below with a live preview.
2. **Queue it** — select a hymn in the list and click **Add** to place it in the playlist, or just click **Start** to show it immediately.
3. **Present** — the hymn appears fullscreen on your selected monitor. Use the queue's **Prev** / **Next** buttons to move between slides.
4. **Settings** — choose your background image, display monitor, and enable dark mode from **File → Settings**.
5. **Exit** — close the main window or press <kbd>Ctrl</kbd>+<kbd>Q</kbd>.

## Packaging (Windows)

Build an executable with [cx_Freeze](https://cx-freeze.readthedocs.io/en/latest/installation.html):

```bash
pip install --upgrade cx_Freeze
python setup.py build
```

A preconfigured PowerShell script (`updater.ps1`) pulls the latest changes and rebuilds the executable.

## Project Structure

| Path | Purpose |
| --- | --- |
| `main.py` | Main application window, search, preview, and queue |
| `slideShow.py` | Fullscreen slide display window |
| `SettingsWindow.py` | Settings dialog (background, monitor, dark mode) |
| `settingsModal.py` | Shared settings persistence and helpers |
| `backend/Setting.json` | Saved application settings |
| `resources/` | Default background, hymn list, and PowerPoint assets |

## License

Copyright (C) 2025. All rights reserved.
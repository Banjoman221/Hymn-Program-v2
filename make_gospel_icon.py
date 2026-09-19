"""Regenerate resources/gospel.ico from the larger resources/gospel.png.

The Windows MSI desktop shortcut and HymnOS.exe use the ICO file, but the old
resources/gospel.ico was only 32x32 pixels, so the desktop icon looked tiny and
blurry. This script rebuilds the ICO from the high-resolution gospel.png as a
multi-size icon (16..256 px, PNG-compressed frames) so the desktop icon renders
large and crisp on Windows.

Run with the build venv (which already includes PyQt6):

    .venv-build\\Scripts\\python make_gospel_icon.py

Resources/gospel.ico was generated from gospel.png by this script.
"""

from __future__ import annotations

import struct

from PyQt6.QtCore import QBuffer, QIODevice, Qt
from PyQt6.QtGui import QImage

SRC = "resources/gospel.png"
DST = "resources/gospel.ico"
SIZES = (16, 24, 32, 48, 64, 128, 256)


def png_bytes(image: QImage) -> bytes:
    """Encode a QImage into PNG bytes."""
    buf = QBuffer()
    buf.open(QIODevice.OpenModeFlag.WriteOnly)
    if not image.save(buf, "PNG"):
        raise RuntimeError("Failed to encode icon frame as PNG")
    return bytes(buf.data())


def build_ico(frames: list[bytes]) -> bytes:
    """Assemble an ICO container from PNG-compressed frames (Vista+ format)."""
    count = len(frames)
    # ICONDIR: reserved(0), type(1=icon), count
    header = struct.pack("<HHH", 0, 1, count)

    # ICONDIRENTRY (16 bytes each): width, height, colors, reserved,
    # planes, bitcount, bytes-in-res, offset-in-file
    entries = b""
    offset = 6 + 16 * count
    for size, data in zip(SIZES, frames):
        dimension = 0 if size >= 256 else size  # 0 means 256 in an entry
        entries += struct.pack(
            "<BBBBHHII",
            dimension,
            dimension,
            0,  # colors
            0,  # reserved
            1,  # planes
            32,  # bit count
            len(data),
            offset,
        )
        offset += len(data)

    return header + entries + b"".join(frames)


def main() -> None:
    image = QImage(SRC)
    if image.isNull():
        raise SystemExit(f"Could not load {SRC}")

    frames = []
    for size in SIZES:
        scaled = image.scaled(
            size,
            size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        frames.append(png_bytes(scaled))

    icon = build_ico(frames)
    with open(DST, "wb") as icon_file:
        icon_file.write(icon)

    print(
        f"Wrote {DST}: {len(icon)} bytes with sizes "
        + ", ".join(str(s) for s in SIZES)
    )


if __name__ == "__main__":
    main()
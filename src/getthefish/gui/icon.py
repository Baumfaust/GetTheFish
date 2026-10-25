"""The application icon, drawn in code so the window, the taskbar and the exe share one source.

``python -m getthefish.gui.icon OUT.ico`` writes it as a multi-size Windows icon (used by the
release build for the exe).
"""

from __future__ import annotations

import struct
import sys
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QGuiApplication, QIcon, QImage, QLinearGradient, QPainter, QPixmap

SIZES = (16, 24, 32, 48, 64, 128, 256)


def render(size: int) -> QImage:
    """The icon at ``size`` x ``size`` pixels, drawn on a 64-unit grid."""
    image = QImage(size, size, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)
    p = QPainter(image)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.scale(size / 64, size / 64)

    background = QLinearGradient(0, 2, 0, 62)
    background.setColorAt(0, QColor("#4f8cff"))
    background.setColorAt(1, QColor("#1d4ed8"))
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(background)
    p.drawRoundedRect(QRectF(2, 2, 60, 60), 14, 14)

    white = QColor("white")
    p.setBrush(white)
    p.drawEllipse(QRectF(10, 25, 34, 20))  # body
    p.drawPolygon([QPointF(40, 35), QPointF(54, 25), QPointF(51, 35), QPointF(54, 45)])  # tail
    p.setBrush(QColor("#1d4ed8"))
    p.drawEllipse(QPointF(19, 33), 2.4, 2.4)  # eye
    bubble = QColor(255, 255, 255, 170)
    p.setBrush(bubble)
    p.drawEllipse(QPointF(15, 18), 2.6, 2.6)
    p.drawEllipse(QPointF(21, 12), 1.7, 1.7)
    p.end()
    return image


def app_icon() -> QIcon:
    icon = QIcon()
    for size in SIZES:
        icon.addPixmap(QPixmap.fromImage(render(size)))
    return icon


def _png(image: QImage) -> bytes:
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")  # type: ignore[call-overload]  # stubs say bytes, runtime wants str
    return bytes(data.data())


def ico_bytes(sizes: tuple[int, ...] = SIZES) -> bytes:
    """A Windows .ico with one PNG-compressed image per size."""
    images = [_png(render(size)) for size in sizes]
    header = struct.pack("<HHH", 0, 1, len(images))
    offset = len(header) + 16 * len(images)
    entries = b""
    for size, png in zip(sizes, images, strict=True):
        dim = 0 if size >= 256 else size  # 0 means 256 in the ICO directory
        entries += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32, len(png), offset)
        offset += len(png)
    return header + entries + b"".join(images)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python -m getthefish.gui.icon OUT.ico", file=sys.stderr)
        return 2
    app = QGuiApplication.instance() or QGuiApplication([argv[0], "-platform", "offscreen"])
    assert app is not None
    out = Path(argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(ico_bytes())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

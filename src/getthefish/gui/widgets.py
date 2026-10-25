"""Custom-painted widgets: live preview, bite meter and a log bridge."""

from __future__ import annotations

import contextlib
import logging
from collections import deque

import numpy as np
import numpy.typing as npt
from PySide6.QtCore import QObject, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QImage,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import QWidget

from getthefish.config import Point
from getthefish.detection import Image
from getthefish.gui import theme


def _rgb_image(image: Image) -> QImage:
    h, w, _ = image.shape
    data = np.ascontiguousarray(image)
    return QImage(data.data, w, h, 3 * w, QImage.Format.Format_RGB888).copy()


def _mask_image(mask: npt.NDArray[np.bool_], color: QColor) -> QImage:
    h, w = mask.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[mask] = (color.red(), color.green(), color.blue(), 220)
    return QImage(rgba.data, w, h, 4 * w, QImage.Format.Format_RGBA8888).copy()


class PreviewView(QWidget):
    """The search area with the pixels matching the bobber colour and the detected bobber.

    Points are relative to the top-left corner of the frame.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(240, 140)
        self._frame: QImage | None = None
        self._mask: QImage | None = None
        self._found: Point | None = None
        self._message = "Preview off"

    def set_frame(
        self, image: Image, mask: npt.NDArray[np.bool_] | None, found: Point | None
    ) -> None:
        self._frame = _rgb_image(image)
        self._mask = None if mask is None else _mask_image(mask, QColor(theme.colors().match))
        self._found = found
        self.update()

    def set_message(self, text: str) -> None:
        """Show ``text`` instead of a frame."""
        self._frame = self._mask = None
        self._message = text
        self.update()

    def _target(self) -> QRectF:
        assert self._frame is not None
        fw, fh = self._frame.width(), self._frame.height()
        scale = min(self.width() / fw, self.height() / fh)
        w, h = fw * scale, fh * scale
        return QRectF((self.width() - w) / 2, (self.height() - h) / 2, w, h)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        c = theme.colors()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(c.sunken))
        if self._frame is None:
            p.setPen(QColor(c.muted))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._message)
            return
        target = self._target()
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        p.drawImage(target, self._frame)
        if self._mask is not None:
            p.drawImage(target, self._mask)
        if self._found is not None:
            scale = target.width() / self._frame.width()
            center = QPointF(
                target.left() + (self._found.x + 0.5) * scale,
                target.top() + (self._found.y + 0.5) * scale,
            )
            p.setPen(QPen(QColor(c.accent), 2))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawEllipse(center, 12, 12)
        p.setPen(QPen(QColor(c.border), 1))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRect(target)


class BiteMeter(QWidget):
    """Scrolling graph of the watched pixel's colour change against ``threshold_catch``.

    Click or drag vertically to move the threshold line.
    """

    threshold_dragged = Signal(int)

    HISTORY = 200
    """Samples kept on screen (20 s at the default poll interval)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(110)
        self.setCursor(Qt.CursorShape.SizeVerCursor)
        self.setToolTip("Click or drag to set Threshold Catch")
        self.samples: deque[int] = deque(maxlen=self.HISTORY)
        self.threshold = 60
        self._frozen_max: float | None = None

    def add_sample(self, change: int) -> None:
        self.samples.append(change)
        self.update()

    def reset(self) -> None:
        self.samples.clear()
        self.update()

    def set_threshold(self, value: int) -> None:
        self.threshold = value
        self.update()

    @property
    def peak(self) -> int:
        return max(self.samples, default=0)

    def y_max(self) -> float:
        if self._frozen_max is not None:
            return self._frozen_max
        return float(min(255, max(32, self.threshold * 1.5, self.peak * 1.2)))

    def _plot(self) -> QRectF:
        return QRectF(self.rect()).adjusted(8, 24, -8, -6)

    def _value_at(self, y: float) -> int:
        plot = self._plot()
        frac = (plot.bottom() - y) / plot.height()
        return max(0, min(255, round(frac * self.y_max())))

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._frozen_max = self.y_max()
            self.threshold_dragged.emit(self._value_at(event.position().y()))

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if self._frozen_max is not None:
            self.threshold_dragged.emit(self._value_at(event.position().y()))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        self._frozen_max = None
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        c = theme.colors()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(c.sunken))
        plot = self._plot()
        y_max = self.y_max()

        def y_of(value: float) -> float:
            return plot.bottom() - min(value, y_max) / y_max * plot.height()

        p.setPen(QPen(QColor(c.grid), 1))
        for i in range(1, 4):
            y = plot.top() + plot.height() * i / 4
            p.drawLine(QPointF(plot.left(), y), QPointF(plot.right(), y))

        if self.samples:
            step = plot.width() / (self.HISTORY - 1)
            points = [QPointF(plot.left() + i * step, y_of(v)) for i, v in enumerate(self.samples)]
            line = QPainterPath(points[0])
            for pt in points[1:]:
                line.lineTo(pt)
            area = QPainterPath(line)
            area.lineTo(points[-1].x(), plot.bottom())
            area.lineTo(points[0].x(), plot.bottom())
            area.closeSubpath()
            fill = QColor(c.accent)
            fill.setAlpha(40)
            p.fillPath(area, fill)
            p.setPen(QPen(QColor(c.accent), 1.5))
            p.drawPath(line)
            if self.samples[-1] > self.threshold:
                p.setBrush(QColor(c.danger))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawEllipse(points[-1], 4.5, 4.5)

        ty = y_of(self.threshold)
        p.setPen(QPen(QColor(c.warn), 1.5, Qt.PenStyle.DashLine))
        p.drawLine(QPointF(plot.left(), ty), QPointF(plot.right(), ty))

        current = self.samples[-1] if self.samples else 0
        p.setPen(QColor(c.muted))
        p.drawText(
            QRectF(10, 4, self.width() - 20, 20),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            f"change {current}   peak {self.peak}",
        )
        p.setPen(QColor(c.warn))
        p.drawText(
            QRectF(10, 4, self.width() - 20, 20),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
            f"threshold {self.threshold}",
        )


class _LogSignal(QObject):
    message = Signal(str)


class QtLogHandler(logging.Handler):
    """Forwards log records to the GUI thread through :attr:`message`."""

    def __init__(self) -> None:
        super().__init__()
        self._signal = _LogSignal()
        self.message = self._signal.message
        self.setFormatter(logging.Formatter("%(asctime)s  %(message)s", "%H:%M:%S"))

    def emit(self, record: logging.LogRecord) -> None:
        # RuntimeError: the receiving window was already deleted.
        with contextlib.suppress(RuntimeError):
            self._signal.message.emit(self.format(record))

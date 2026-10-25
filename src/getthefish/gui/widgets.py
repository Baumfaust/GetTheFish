"""Custom-painted widgets: status LED, bite meter, round history and a log bridge."""

from __future__ import annotations

import contextlib
import logging
import math
from collections import deque

from PySide6.QtCore import QObject, QPointF, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import QSizePolicy, QWidget

from getthefish.gui import theme


class StatusLed(QWidget):
    """A tinted pill with a glowing dot and the current state.

    While ``pulse`` is on the glow breathes slowly, to show the loop is busy.
    """

    DOT = 8.0
    PAD = 10.0
    PULSE_MS = 1600
    WIDEST = "Waiting for bite"
    """Width reserved for the text, so the header does not jump when the state changes."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.text = "Idle"
        self.tone = ""
        self.pulse = False
        self._phase = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(40)
        self._timer.timeout.connect(self._tick)

    def set_state(self, text: str, tone: str, *, pulse: bool) -> None:
        """``tone`` is a theme colour name (accent, success, warn, danger) or empty for idle."""
        self.text, self.tone, self.pulse = text, tone, pulse
        if pulse and not self._timer.isActive():
            self._phase = 0.0
            self._timer.start()
        elif not pulse:
            self._timer.stop()
        self.setToolTip(text)
        self.update()

    def _tick(self) -> None:
        self._phase = (self._phase + self._timer.interval() / self.PULSE_MS) % 1.0
        self.update()

    def _font(self) -> QFont:
        font = QFont(self.font())
        font.setWeight(QFont.Weight.DemiBold)
        return font

    def sizeHint(self) -> QSize:  # noqa: N802
        fm = QFontMetrics(self._font())
        width = max(fm.horizontalAdvance(self.WIDEST), fm.horizontalAdvance(self.text))
        return QSize(round(self.PAD * 2.5 + self.DOT + width), max(26, fm.height() + 10))

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        c = theme.colors()
        color = QColor(getattr(c, self.tone) if self.tone else c.muted)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pill = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = pill.height() / 2
        fill, edge = QColor(color), QColor(color)
        fill.setAlphaF(0.10 if self.tone else 0.06)
        edge.setAlphaF(0.35)
        p.setPen(QPen(edge, 1))
        p.setBrush(fill)
        p.drawRoundedRect(pill, radius, radius)

        center = QPointF(self.PAD + self.DOT / 2, pill.center().y())
        if self.tone:
            # 0..1..0 once per pulse period; a steady medium glow when not pulsing.
            breath = 0.5 - 0.5 * math.cos(2 * math.pi * self._phase) if self.pulse else 0.5
            glow_radius = self.DOT * (1.0 + 0.6 * breath)
            glow = QRadialGradient(center, glow_radius)
            inner = QColor(color)
            inner.setAlphaF(0.25 + 0.35 * breath)
            outer = QColor(color)
            outer.setAlphaF(0.0)
            glow.setColorAt(0.4, inner)
            glow.setColorAt(1.0, outer)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(glow)
            p.drawEllipse(center, glow_radius, glow_radius)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(color)
        p.drawEllipse(center, self.DOT / 2, self.DOT / 2)

        p.setFont(self._font())
        p.setPen(color if self.tone else QColor(c.muted))
        text_left = self.PAD * 1.5 + self.DOT
        p.drawText(
            QRectF(text_left, 0, self.width() - text_left - self.PAD, self.height()),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            self.text,
        )


class RoundHistory(QWidget):
    """The outcome of the last rounds as dots, newest on the right."""

    SIZE = 30
    DOT = 8
    GAP = 4

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(self.DOT + 4)
        self.setToolTip("Last rounds: green caught, orange missed, red no bobber")
        self.outcomes: deque[str] = deque(maxlen=self.SIZE)

    def add(self, outcome: str) -> None:
        """``outcome`` is ``caught``, ``missed`` or ``no_bobber``."""
        self.outcomes.append(outcome)
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        c = theme.colors()
        colors = {"caught": c.success, "missed": c.warn, "no_bobber": c.danger}
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        y = (self.height() - self.DOT) / 2
        fits = max(0, (self.width() + self.GAP) // (self.DOT + self.GAP))
        shown = list(self.outcomes)[-fits:] if fits else []
        # Empty slots first, so the newest dot always sits at the right edge.
        slots = [None] * (min(fits, self.SIZE) - len(shown)) + shown
        x = self.width() - len(slots) * (self.DOT + self.GAP) + self.GAP
        for outcome in slots:
            p.setBrush(QColor(c.grid if outcome is None else colors[outcome]))
            p.drawEllipse(QRectF(x, y, self.DOT, self.DOT))
            x += self.DOT + self.GAP


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

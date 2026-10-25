"""Main window: edit settings, pick colour and area, start/stop fishing.

A compact view shows only what matters during a session, so the window fits beside
the game.
"""

from __future__ import annotations

import logging
import sys
import time
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from PySide6.QtCore import (
    QByteArray,
    QObject,
    QPoint,
    QRect,
    QSettings,
    QSize,
    Qt,
    QThread,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import (
    QCloseEvent,
    QColor,
    QDesktopServices,
    QKeyEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QRubberBand,
    QSizePolicy,
    QWidget,
)

from getthefish.bot import BiteSample, BobberFound, Event, GetTheFish, RoundFinished, Stats
from getthefish.config import (
    ConfigError,
    FishConfig,
    Point,
    default_config_path,
    load_or_migrate,
    normalize_key,
)
from getthefish.detection import color_mask, locate_cluster
from getthefish.devices import MssScreen, PyAutoGuiInput, ScreenSource, is_known_key
from getthefish.gui import theme
from getthefish.gui.ui_main import Ui_MainWindow
from getthefish.gui.widgets import QtLogHandler
from getthefish.logs import setup_logging

logger = logging.getLogger(__name__)

BotFactory = Callable[[FishConfig, Callable[[str], None]], GetTheFish]

PREVIEW_INTERVAL_MS = 200
UI_SETTINGS_FILENAME = "window.ini"
FULL_SIZE = QSize(1040, 680)
COMPACT_SIZE = QSize(320, 210)
NO_VALUE = "\N{EN DASH}"


def default_bot_factory(config: FishConfig, on_status: Callable[[str], None]) -> GetTheFish:
    return GetTheFish(config, MssScreen(), PyAutoGuiInput(), on_status=on_status)


class FishingWorker(QThread):
    """Runs one :class:`GetTheFish` instance in a background thread."""

    status = Signal(str)
    live = Signal(object)

    def __init__(self, factory: BotFactory, config: FishConfig, parent: QObject | None = None):
        super().__init__(parent)
        self.bot = factory(config, self.status.emit)
        self.bot.on_event = self.live.emit

    def run(self) -> None:
        try:
            self.bot.run()
        except Exception as e:  # pragma: no cover - defensive, reported to the UI
            logger.exception("Fishing failed")
            self.status.emit(f"Error: {e}")

    def stop(self) -> None:
        self.bot.stop()


class ScreenOverlay(QLabel):
    """Full-screen frozen screenshot used for picking a colour or an area.

    Coordinates are reported in physical pixels so they match ``mss``.
    """

    def __init__(self, pixmap: QPixmap | None = None) -> None:
        super().__init__()
        if pixmap is None:
            screen = QApplication.primaryScreen()
            assert screen is not None
            pixmap = screen.grabWindow(0)  # 0 = whole screen
        self._pixmap = pixmap
        self._image = pixmap.toImage()
        self._ratio = pixmap.devicePixelRatio()
        self.setPixmap(pixmap)
        self.setCursor(Qt.CursorShape.CrossCursor)

    def to_physical(self, pos: QPoint) -> Point:
        return Point(round(pos.x() * self._ratio), round(pos.y() * self._ratio))

    def color_at(self, pos: QPoint) -> tuple[int, int, int]:
        p = self.to_physical(pos)
        c = QColor(self._image.pixel(p.x, p.y))
        return (c.red(), c.green(), c.blue())

    def keyPressEvent(self, event: QKeyEvent | None) -> None:  # noqa: N802
        if event is not None and event.key() == Qt.Key.Key_Escape:
            self.close()


class ColorPicker(ScreenOverlay):
    """Click a pixel to choose the bobber colour. Esc cancels.

    A magnifier next to the cursor shows the surrounding pixels and the colour under it.
    """

    color_picked = Signal(tuple)

    LOUPE_RADIUS = 7
    """Pixels shown on each side of the centre pixel."""
    LOUPE_ZOOM = 10

    def __init__(self, pixmap: QPixmap | None = None) -> None:
        super().__init__(pixmap)
        self.setMouseTracking(True)
        self.cursor_pos: QPoint | None = None

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event is not None:
            self.cursor_pos = event.position().toPoint()
            self.update()

    def mousePressEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event is not None and event.button() == Qt.MouseButton.LeftButton:
            self.color_picked.emit(self.color_at(event.position().toPoint()))
            self.close()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        super().paintEvent(event)
        if self.cursor_pos is None:
            return
        cursor, r, zoom = self.cursor_pos, self.LOUPE_RADIUS, self.LOUPE_ZOOM
        size = (2 * r + 1) * zoom
        center = self.to_physical(cursor)
        patch = self._image.copy(QRect(center.x - r, center.y - r, 2 * r + 1, 2 * r + 1))
        # Keep the loupe on screen: flip it to the other side of the cursor near an edge.
        x = cursor.x() + 24 if cursor.x() + 24 + size <= self.width() else cursor.x() - 24 - size
        y = cursor.y() + 24 if cursor.y() + 54 + size <= self.height() else cursor.y() - 54 - size
        p = QPainter(self)
        p.drawImage(QRect(x, y, size, size), patch)
        p.setPen(QPen(QColor(theme.colors().accent), 2))
        p.drawRect(x, y, size, size)
        p.setPen(QPen(QColor("white"), 1))
        p.drawRect(x + r * zoom, y + r * zoom, zoom, zoom)
        red, green, blue = self.color_at(cursor)
        color = QColor(red, green, blue)
        p.fillRect(x, y + size + 2, size + 1, 26, QColor(theme.colors().panel))
        p.fillRect(x + 4, y + size + 6, 18, 18, color)
        p.setPen(QColor(theme.colors().text))
        p.drawText(
            QRect(x + 28, y + size + 2, size - 28, 26),
            Qt.AlignmentFlag.AlignVCenter,
            f"{color.name()}  {red} {green} {blue}",
        )


class AreaSelector(ScreenOverlay):
    """Drag with the left button to choose the search area. Esc cancels."""

    area_selected = Signal(object, object)

    def __init__(self, pixmap: QPixmap | None = None) -> None:
        super().__init__(pixmap)
        self._origin: QPoint | None = None
        self._band = QRubberBand(QRubberBand.Shape.Rectangle, self)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event is None:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            self._origin = event.position().toPoint()
            self._band.setGeometry(QRect(self._origin, QSize()))
            self._band.show()
        elif event.button() == Qt.MouseButton.RightButton:
            self.close()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event is not None and self._origin is not None:
            self._band.setGeometry(QRect(self._origin, event.position().toPoint()).normalized())

    def mouseReleaseEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event is None or event.button() != Qt.MouseButton.LeftButton or self._origin is None:
            return
        rect = QRect(self._origin, event.position().toPoint()).normalized()
        self._origin = None
        self._band.hide()
        if rect.width() < 2 or rect.height() < 2:
            return
        self.area_selected.emit(
            self.to_physical(rect.topLeft()), self.to_physical(rect.bottomRight())
        )
        self.close()


class MainWindow(QMainWindow):
    def __init__(
        self,
        config: FishConfig,
        config_path: Path,
        bot_factory: BotFactory = default_bot_factory,
        screen_factory: Callable[[], ScreenSource] = MssScreen,
    ) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = config
        self.config_path = config_path
        self.bot_factory = bot_factory
        self.screen_factory = screen_factory
        self.preview_screen: ScreenSource | None = None
        self.worker: FishingWorker | None = None
        self.overlay: ScreenOverlay | None = None
        self.stats = Stats()
        self.started_at: float | None = None
        self.compact_before_session = False
        self.dark = False
        self.compact = False
        # Window preferences (theme, view, positions) live next to config.json.
        self.settings = QSettings(
            str(config_path.parent / UI_SETTINGS_FILENAME), QSettings.Format.IniFormat
        )
        self.meters = (self.ui.biteMeter, self.ui.compactMeter)
        self.start_buttons = (self.ui.startButton, self.ui.compactStartButton)

        for spin in (self.ui.thresholdBobberSpinBox, self.ui.thresholdCatchSpinBox):
            spin.setRange(0, 255)
        self.refresh()
        self.show_stats()

        self.log_handler = QtLogHandler()
        self.log_handler.message.connect(self.ui.logView.appendPlainText)
        logging.getLogger("getthefish").addHandler(self.log_handler)

        self.preview_timer = QTimer(self)
        self.preview_timer.setInterval(PREVIEW_INTERVAL_MS)
        self.preview_timer.timeout.connect(self.update_preview)
        self.clock_timer = QTimer(self)
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self.show_stats)

        for button in self.start_buttons:
            button.clicked.connect(self.toggle_fishing)
        for meter in self.meters:
            meter.threshold_dragged.connect(self.ui.thresholdCatchSpinBox.setValue)
        self.ui.areaButton.clicked.connect(self.select_area)
        self.ui.colorButton.clicked.connect(self.pick_color)
        self.ui.openConfigFolderButton.clicked.connect(self.open_config_folder)
        self.ui.thresholdBobberSpinBox.valueChanged.connect(self.settings_changed)
        self.ui.thresholdCatchSpinBox.valueChanged.connect(self.settings_changed)
        self.ui.jumpToBobberCheck.stateChanged.connect(self.settings_changed)
        self.ui.verboseCheck.stateChanged.connect(self.settings_changed)
        self.ui.castKeyEdit.editingFinished.connect(self.cast_key_changed)
        self.ui.previewCheck.toggled.connect(self.update_preview_timer)
        self.ui.themeButton.clicked.connect(lambda: self.set_dark(not self.dark))
        self.ui.viewButton.clicked.connect(lambda: self.set_compact(not self.compact))

        self.dark = bool(self.settings.value("dark", theme.system_prefers_dark(), type=bool))
        self.set_dark(self.dark)
        self.compact = bool(self.settings.value("compact", False, type=bool))
        self._show_view()

    @property
    def is_fishing(self) -> bool:
        return self.worker is not None and self.worker.isRunning()

    def refresh(self) -> None:
        """Show the current config in the widgets without triggering a save."""
        c = self.config
        widgets: list[QWidget] = [
            self.ui.thresholdBobberSpinBox,
            self.ui.thresholdCatchSpinBox,
            self.ui.jumpToBobberCheck,
            self.ui.verboseCheck,
        ]
        for w in widgets:
            w.blockSignals(True)
        self.ui.thresholdBobberSpinBox.setValue(c.threshold_bobber)
        self.ui.thresholdCatchSpinBox.setValue(c.threshold_catch)
        self.ui.jumpToBobberCheck.setChecked(c.jump_to_bobber)
        self.ui.verboseCheck.setChecked(c.verbose)
        self.ui.castKeyEdit.setText(c.cast_key)
        for w in widgets:
            w.blockSignals(False)
        self.ui.posStartLabel.setText(f"{c.start_pos.x}, {c.start_pos.y}")
        self.ui.posEndLabel.setText(f"{c.end_pos.x}, {c.end_pos.y}")
        hex_color = QColor(*c.bobber_color).name(QColor.NameFormat.HexRgb)
        self.ui.hexColorLabel.setText(hex_color)
        self.ui.bobberColorLabel.setStyleSheet(f"QLabel {{ background-color: {hex_color}; }}")
        for meter in self.meters:
            meter.set_threshold(c.threshold_catch)

    def save(self) -> None:
        try:
            self.config.validate()
            self.config.save(self.config_path)
        except (ConfigError, OSError) as e:
            self.show_status(f"Could not save settings: {e}")

    def settings_changed(self) -> None:
        self.config.threshold_bobber = self.ui.thresholdBobberSpinBox.value()
        self.config.threshold_catch = self.ui.thresholdCatchSpinBox.value()
        self.config.jump_to_bobber = self.ui.jumpToBobberCheck.isChecked()
        self.config.verbose = self.ui.verboseCheck.isChecked()
        for meter in self.meters:
            meter.set_threshold(self.config.threshold_catch)
        self.save()

    def cast_key_changed(self) -> None:
        key = normalize_key(self.ui.castKeyEdit.text())
        if key == self.config.cast_key:
            self.ui.castKeyEdit.setText(key)
            return
        try:
            replace(self.config, cast_key=key)  # validates
            if not is_known_key(key):
                raise ConfigError(f"Unknown key {key!r} (use names like 0, f, f1, num0)")
        except ConfigError as e:
            self.show_status(str(e))
            self.ui.castKeyEdit.setText(self.config.cast_key)
            return
        self.config.cast_key = key
        self.ui.castKeyEdit.setText(key)
        self.save()

    def set_color(self, color: tuple[int, int, int]) -> None:
        self.config.bobber_color = color
        self.refresh()
        self.save()

    def set_area(self, start: Point, end: Point) -> None:
        self.config.start_pos = start
        self.config.end_pos = end
        self.refresh()
        self.save()

    def show_status(self, text: str) -> None:
        self.ui.statusbar.showMessage(text)

    def set_dark(self, dark: bool) -> None:
        self.dark = dark
        self.settings.setValue("dark", dark)
        app = QApplication.instance()
        assert isinstance(app, QApplication)
        theme.apply(app, dark=dark)
        self.ui.themeButton.setText("Light" if dark else "Dark")
        self.update()

    def set_compact(self, compact: bool) -> None:
        """Switch between the full and the compact view; each keeps its own window geometry."""
        if compact == self.compact:
            return
        self.settings.setValue(self._geometry_key(), self.saveGeometry())
        self.compact = compact
        self.settings.setValue("compact", compact)
        self._show_view()

    def _geometry_key(self) -> str:
        return "compact_geometry" if self.compact else "full_geometry"

    def _show_view(self) -> None:
        current = self.ui.compactPage if self.compact else self.ui.fullPage
        # Ignore the hidden page's size, otherwise the compact window could not shrink.
        for page in (self.ui.fullPage, self.ui.compactPage):
            policy = QSizePolicy.Policy.Preferred if page is current else QSizePolicy.Policy.Ignored
            page.setSizePolicy(policy, policy)
        self.ui.pages.setCurrentWidget(current)
        self.ui.viewButton.setText("Expand" if self.compact else "Compact")
        geometry = self.settings.value(self._geometry_key())
        if not (isinstance(geometry, QByteArray) and self.restoreGeometry(geometry)):
            self.resize(COMPACT_SIZE if self.compact else FULL_SIZE)
        self.update_preview_timer()

    def show_state(self, state: str) -> None:
        """Update the state pill and the start buttons (state: idle, fishing or stopping)."""
        self.ui.stateLabel.setText(state.upper())
        self.ui.stateLabel.setProperty("state", state)
        for w in (self.ui.stateLabel, *self.start_buttons):
            w.setProperty("fishing", state == "fishing")
            w.style().unpolish(w)
            w.style().polish(w)

    def set_start_button(self, text: str, *, enabled: bool = True) -> None:
        for button in self.start_buttons:
            button.setText(text)
            button.setEnabled(enabled)

    def show_stats(self) -> None:
        s = self.stats
        rate = f"{100 * s.catches / s.casts:.0f}%" if s.casts else NO_VALUE
        elapsed = 0.0 if self.started_at is None else time.monotonic() - self.started_at
        # Fish per hour is meaningless (and jumpy) in the first minute.
        per_hour = f"{s.catches / elapsed * 3600:.0f}" if elapsed >= 60 else NO_VALUE
        minutes, seconds = divmod(int(elapsed), 60)
        hours, minutes = divmod(minutes, 60)
        clock = f"{hours}:{minutes:02}:{seconds:02}"
        self.ui.castsValue.setText(str(s.casts))
        self.ui.catchesValue.setText(str(s.catches))
        self.ui.missesValue.setText(str(s.misses))
        self.ui.rateValue.setText(rate)
        self.ui.perHourValue.setText(per_hour)
        self.ui.elapsedValue.setText(clock)
        self.ui.compactStatsLabel.setText(
            f"{s.catches} caught \N{MIDDLE DOT} {s.casts} casts \N{MIDDLE DOT} {rate} "
            f"\N{MIDDLE DOT} {clock}"
        )

    def handle_event(self, event: Event) -> None:
        """Live data from the fishing thread."""
        for meter in self.meters:
            match event:
                case BobberFound():
                    meter.reset()
                case BiteSample(change=change):
                    meter.add_sample(change)
        if isinstance(event, RoundFinished):
            self.stats = event.stats
            self.show_stats()

    def update_preview_timer(self) -> None:
        """The preview is a setup aid: it only runs in the full view and outside a session."""
        if self.compact or self.is_fishing:
            self.preview_timer.stop()
            self.ui.previewView.set_message("Preview pauses while fishing")
        elif self.ui.previewCheck.isChecked():
            self.preview_timer.start()
            self.update_preview()
            return
        else:
            self.preview_timer.stop()
            self.ui.previewView.set_message("Preview off")
        self.ui.previewInfoLabel.clear()

    def update_preview(self) -> None:
        """Grab the search area and highlight the pixels that match the bobber colour."""
        try:
            if self.preview_screen is None:
                self.preview_screen = self.screen_factory()
            image = self.preview_screen.grab(self.config.search_area)
        except Exception as e:
            logger.warning("Preview unavailable: %s", e)
            self.ui.previewCheck.setChecked(False)
            self.ui.previewView.set_message(f"Preview unavailable: {e}")
            return
        mask = color_mask(image, self.config.bobber_color, self.config.threshold_bobber)
        found = locate_cluster(mask)
        self.ui.previewView.set_frame(image, mask, found)
        where = "no bobber" if found is None else f"bobber at {found.x}, {found.y}"
        self.ui.previewInfoLabel.setText(
            f"{int(mask.sum()):,} matching pixels \N{MIDDLE DOT} {where}"
        )

    def covers_search_area(self) -> bool:
        """True if this window hides part of the water or the click that focuses the game."""
        if not self.isVisible():
            return False
        ratio = self.devicePixelRatioF()
        g = self.frameGeometry()
        left, top, right, bottom = self.config.search_area
        return (
            g.left() * ratio < right
            and (g.right() + 1) * ratio > left
            and g.top() * ratio < bottom
            and (g.bottom() + 1) * ratio > top
        )

    def open_config_folder(self) -> None:
        """Open the directory containing config.json and the log file."""
        folder_url = QUrl.fromLocalFile(str(self.config_path.parent.resolve()))
        if not QDesktopServices.openUrl(folder_url):
            self.show_status(f"Could not open folder: {self.config_path.parent}")

    def toggle_fishing(self) -> None:
        if self.is_fishing:
            assert self.worker is not None
            self.worker.stop()
            self.set_start_button("Stopping...", enabled=False)
            self.show_state("stopping")
            return
        self.compact_before_session = self.compact
        self.set_compact(True)
        if self.covers_search_area():
            # The cast click would focus this window instead of the game and nothing happens.
            self.show_status("Move this window beside the game: it covers the fishing area")
            return
        try:
            self.worker = FishingWorker(self.bot_factory, self.config, self)
        except Exception as e:
            QMessageBox.critical(self, "Cannot start", str(e))
            self.set_compact(self.compact_before_session)
            return
        self.worker.status.connect(self.show_status)
        self.worker.live.connect(self.handle_event)
        self.worker.finished.connect(self.fishing_finished)
        self.set_editing_enabled(False)
        self.set_start_button("Stop")
        self.show_state("fishing")
        self.stats = Stats()
        self.started_at = time.monotonic()
        for meter in self.meters:
            meter.reset()
        self.show_stats()
        self.clock_timer.start()
        self.worker.start()
        self.update_preview_timer()

    def fishing_finished(self) -> None:
        self.set_editing_enabled(True)
        self.set_start_button("Start")
        self.show_state("idle")
        self.clock_timer.stop()
        self.set_compact(self.compact_before_session)
        self.update_preview_timer()

    def set_editing_enabled(self, enabled: bool) -> None:
        """Lock what a running session depends on; thresholds stay editable for live tuning."""
        for w in (
            self.ui.areaButton,
            self.ui.colorButton,
            self.ui.jumpToBobberCheck,
            self.ui.castKeyEdit,
        ):
            w.setEnabled(enabled)

    def pick_color(self) -> None:
        picker = ColorPicker()
        picker.color_picked.connect(self.set_color)
        self._show_overlay(picker)

    def select_area(self) -> None:
        selector = AreaSelector()
        selector.area_selected.connect(self.set_area)
        self._show_overlay(selector)

    def _show_overlay(self, overlay: ScreenOverlay) -> None:
        self.overlay = overlay
        overlay.showFullScreen()

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        self.preview_timer.stop()
        self.clock_timer.stop()
        self.settings.setValue(self._geometry_key(), self.saveGeometry())
        self.settings.sync()
        logging.getLogger("getthefish").removeHandler(self.log_handler)
        if self.worker is not None:
            self.worker.stop()
            self.worker.wait(5000)
        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    config_path = default_config_path()
    if log_file := setup_logging(config_path.parent):
        logging.info("Logging to %s", log_file)
    try:
        config = load_or_migrate(config_path)
    except ConfigError as e:
        QMessageBox.critical(None, "Invalid configuration", f"{config_path}:\n{e}")
        return 2
    window = MainWindow(config, config_path)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

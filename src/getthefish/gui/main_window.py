"""Main window: edit settings, pick colour and area, start/stop fishing."""

from __future__ import annotations

import logging
import sys
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from PySide6.QtCore import QObject, QPoint, QRect, QSize, Qt, QThread, QUrl, Signal
from PySide6.QtGui import QCloseEvent, QColor, QDesktopServices, QKeyEvent, QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox, QRubberBand, QWidget

from getthefish.bot import GetTheFish
from getthefish.config import (
    ConfigError,
    FishConfig,
    Point,
    default_config_path,
    load_or_migrate,
    normalize_key,
)
from getthefish.devices import MssScreen, PyAutoGuiInput, is_known_key
from getthefish.gui.ui_main import Ui_MainWindow
from getthefish.logs import setup_logging

logger = logging.getLogger(__name__)

BotFactory = Callable[[FishConfig, Callable[[str], None]], GetTheFish]


def default_bot_factory(config: FishConfig, on_status: Callable[[str], None]) -> GetTheFish:
    return GetTheFish(config, MssScreen(), PyAutoGuiInput(), on_status=on_status)


class FishingWorker(QThread):
    """Runs one :class:`GetTheFish` instance in a background thread."""

    status = Signal(str)

    def __init__(self, factory: BotFactory, config: FishConfig, parent: QObject | None = None):
        super().__init__(parent)
        self.bot = factory(config, self.status.emit)

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
    """Click a pixel to choose the bobber colour. Esc cancels."""

    color_picked = Signal(tuple)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if event is not None and event.button() == Qt.MouseButton.LeftButton:
            self.color_picked.emit(self.color_at(event.position().toPoint()))
            self.close()


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
    ) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = config
        self.config_path = config_path
        self.bot_factory = bot_factory
        self.worker: FishingWorker | None = None
        self.overlay: ScreenOverlay | None = None

        for spin in (self.ui.thresholdBobberSpinBox, self.ui.thresholdCatchSpinBox):
            spin.setRange(0, 255)
        self.refresh()

        self.ui.startButton.clicked.connect(self.toggle_fishing)
        self.ui.areaButton.clicked.connect(self.select_area)
        self.ui.colorButton.clicked.connect(self.pick_color)
        self.ui.openConfigFolderButton.clicked.connect(self.open_config_folder)
        self.ui.thresholdBobberSpinBox.valueChanged.connect(self.settings_changed)
        self.ui.thresholdCatchSpinBox.valueChanged.connect(self.settings_changed)
        self.ui.jumpToBobberCheck.stateChanged.connect(self.settings_changed)
        self.ui.verboseCheck.stateChanged.connect(self.settings_changed)
        self.ui.castKeyEdit.editingFinished.connect(self.cast_key_changed)

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

    def open_config_folder(self) -> None:
        """Open the directory containing config.json and the log file."""
        folder_url = QUrl.fromLocalFile(str(self.config_path.parent.resolve()))
        if not QDesktopServices.openUrl(folder_url):
            self.show_status(f"Could not open folder: {self.config_path.parent}")

    def toggle_fishing(self) -> None:
        if self.is_fishing:
            assert self.worker is not None
            self.worker.stop()
            self.ui.startButton.setEnabled(False)
            self.ui.startButton.setText("Stopping...")
            return
        try:
            self.worker = FishingWorker(self.bot_factory, self.config, self)
        except Exception as e:
            QMessageBox.critical(self, "Cannot start", str(e))
            return
        self.worker.status.connect(self.show_status)
        self.worker.finished.connect(self.fishing_finished)
        self.set_editing_enabled(False)
        self.ui.startButton.setText("Stop")
        self.worker.start()

    def fishing_finished(self) -> None:
        self.set_editing_enabled(True)
        self.ui.startButton.setEnabled(True)
        self.ui.startButton.setText("Start")

    def set_editing_enabled(self, enabled: bool) -> None:
        for w in (
            self.ui.areaButton,
            self.ui.colorButton,
            self.ui.thresholdBobberSpinBox,
            self.ui.thresholdCatchSpinBox,
            self.ui.jumpToBobberCheck,
            self.ui.verboseCheck,
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

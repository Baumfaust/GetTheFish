from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pytestqt")

from PySide6.QtCore import QPoint, Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QFontMetrics, QPixmap
from pytestqt.qtbot import QtBot

from getthefish.bot import (
    BiteSample,
    BobberFound,
    GetTheFish,
    Phase,
    PhaseChanged,
    RoundFinished,
    Stats,
)
from getthefish.config import FishConfig, Point
from getthefish.gui import theme
from getthefish.gui.main_window import AreaSelector, ColorPicker, MainWindow
from helpers import NO_DELAY, FakeMouse, FakeScreen, make_image


def idle_bot_factory(config: FishConfig, on_status: Callable[[str], None]) -> GetTheFish:
    # Nothing to find -> the bot gives up quickly on its own.
    return GetTheFish(config, FakeScreen(make_image(1200, 500)), FakeMouse(), NO_DELAY, on_status)


@pytest.fixture
def window(qtbot: QtBot, tmp_path: Path) -> MainWindow:
    w = MainWindow(FishConfig(), tmp_path / "config.json", idle_bot_factory)
    qtbot.addWidget(w)
    return w


def test_shows_config(window: MainWindow, qtbot: QtBot) -> None:
    window.show()
    qtbot.waitExposed(window)
    assert window.ui.thresholdBobberSpinBox.value() == 18
    assert window.ui.thresholdCatchSpinBox.value() == 60
    for spin in (window.ui.thresholdBobberSpinBox, window.ui.thresholdCatchSpinBox):
        required_text_width = QFontMetrics(spin.lineEdit().font()).horizontalAdvance("255") + 12
        assert spin.width() >= 120
        assert spin.lineEdit().width() >= required_text_width
    assert window.ui.posStartLabel.text() == "200, 50"
    assert window.ui.posEndLabel.text() == "1100, 400"
    assert window.ui.hexColorLabel.text() == "#48290c"


def test_open_config_folder(window: MainWindow, monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[str] = []

    def open_url(url: QUrl) -> bool:
        opened.append(url.toLocalFile())
        return True

    monkeypatch.setattr(QDesktopServices, "openUrl", open_url)
    window.ui.openConfigFolderButton.click()
    assert Path(opened[0]) == window.config_path.parent.resolve()


def enter_cast_key(window: MainWindow, text: str) -> None:
    window.ui.castKeyEdit.setText(text)
    window.ui.castKeyEdit.editingFinished.emit()


@pytest.fixture
def known_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "getthefish.gui.main_window.is_known_key", lambda key: key in {"0", "f", "f1"}
    )


def test_cast_key_shown_and_saved(window: MainWindow, known_keys: None) -> None:
    assert window.ui.castKeyEdit.text() == "0"
    enter_cast_key(window, " F1 ")
    assert window.ui.castKeyEdit.text() == "f1"
    assert FishConfig.load(window.config_path).cast_key == "f1"


@pytest.mark.parametrize("text", ["", "nokey", "page up"])
def test_invalid_cast_key_is_rejected(window: MainWindow, known_keys: None, text: str) -> None:
    enter_cast_key(window, text)
    assert window.config.cast_key == "0"
    assert window.ui.castKeyEdit.text() == "0"
    assert window.ui.statusbar.currentMessage()


def test_changing_settings_saves(window: MainWindow) -> None:
    window.ui.thresholdBobberSpinBox.setValue(25)
    window.ui.verboseCheck.setChecked(True)
    saved = FishConfig.load(window.config_path)
    assert saved.threshold_bobber == 25
    assert saved.verbose is True


def test_set_color_and_area_save(window: MainWindow) -> None:
    window.set_color((1, 2, 3))
    window.set_area(Point(5, 6), Point(50, 60))
    saved = FishConfig.load(window.config_path)
    assert saved.bobber_color == (1, 2, 3)
    assert saved.search_area == (5, 6, 50, 60)
    assert window.ui.hexColorLabel.text() == "#010203"
    assert window.ui.posEndLabel.text() == "50, 60"


def test_start_and_finish(window: MainWindow, qtbot: QtBot) -> None:
    qtbot.mouseClick(window.ui.startButton, Qt.MouseButton.LeftButton)
    assert window.worker is not None
    assert not window.ui.areaButton.isEnabled()
    with qtbot.waitSignal(window.worker.finished, timeout=5000):
        pass
    assert window.ui.startButton.text() == "Start"
    assert window.ui.areaButton.isEnabled()
    assert "Stopped fishing" in window.ui.statusbar.currentMessage()


def test_start_twice_after_finish(window: MainWindow, qtbot: QtBot) -> None:
    for _ in range(2):
        window.toggle_fishing()
        assert window.worker is not None
        with qtbot.waitSignal(window.worker.finished, timeout=5000):
            pass
    assert window.ui.startButton.isEnabled()


def test_stop_while_fishing(qtbot: QtBot, tmp_path: Path) -> None:
    # A bobber that never bites keeps the bot busy until it is stopped.
    def busy_factory(config: FishConfig, on_status: Callable[[str], None]) -> GetTheFish:
        screen = make_image(1200, 500)
        screen[100:110, 300:310] = config.bobber_color
        timing = replace(NO_DELAY, bite_timeout=60, bite_poll_interval=0.01)
        return GetTheFish(config, FakeScreen(screen), FakeMouse(), timing, on_status)

    w = MainWindow(FishConfig(), tmp_path / "config.json", busy_factory)
    qtbot.addWidget(w)
    w.toggle_fishing()
    assert w.is_fishing
    assert w.worker is not None
    with qtbot.waitSignal(w.worker.finished, timeout=5000):
        w.toggle_fishing()
        assert w.ui.startButton.text() == "Stopping..."
    assert w.ui.startButton.text() == "Start"


def test_start_failure_shows_error(
    qtbot: QtBot, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken_factory(config: FishConfig, on_status: Callable[[str], None]) -> GetTheFish:
        raise RuntimeError("no display")

    shown: list[str] = []
    monkeypatch.setattr(
        "getthefish.gui.main_window.QMessageBox.critical", lambda _p, _t, text: shown.append(text)
    )
    w = MainWindow(FishConfig(), tmp_path / "config.json", broken_factory)
    qtbot.addWidget(w)
    w.toggle_fishing()
    assert shown == ["no display"]
    assert w.ui.startButton.text() == "Start"


def test_save_error_is_reported(window: MainWindow, tmp_path: Path) -> None:
    window.config_path = tmp_path  # a directory cannot be written as a file
    window.ui.verboseCheck.setChecked(True)
    assert window.ui.statusbar.currentMessage().startswith("Could not save settings")


def _solid_pixmap(color: QColor) -> QPixmap:
    pm = QPixmap(40, 30)
    pm.fill(color)
    return pm


def test_color_picker(qtbot: QtBot) -> None:
    picker = ColorPicker(_solid_pixmap(QColor(10, 20, 30)))
    qtbot.addWidget(picker)
    with qtbot.waitSignal(picker.color_picked) as blocker:
        qtbot.mouseClick(picker, Qt.MouseButton.LeftButton, pos=QPoint(5, 5))
    assert blocker.args == [(10, 20, 30)]


def test_area_selector(qtbot: QtBot) -> None:
    selector = AreaSelector(_solid_pixmap(QColor("black")))
    qtbot.addWidget(selector)
    selector.show()
    with qtbot.waitSignal(selector.area_selected) as blocker:
        qtbot.mousePress(selector, Qt.MouseButton.LeftButton, pos=QPoint(20, 15))
        qtbot.mouseMove(selector, QPoint(5, 3))
        qtbot.mouseRelease(selector, Qt.MouseButton.LeftButton, pos=QPoint(5, 3))
    start, end = blocker.args
    assert start.x < end.x and start.y < end.y


def test_events_update_meter_and_stats(window: MainWindow) -> None:
    window.handle_event(BobberFound(Point(300, 100), Point(303, 105)))
    window.handle_event(BiteSample(12))
    window.handle_event(BiteSample(80))
    assert list(window.ui.biteMeter.samples) == [12, 80]
    assert window.ui.biteMeter.peak == 80
    window.handle_event(RoundFinished(True, Stats(casts=4, catches=3, misses=1)))
    assert window.ui.castsValue.text() == "4"
    assert window.ui.catchesValue.text() == "3"
    assert window.ui.rateValue.text() == "75%"


def test_meter_drag_sets_threshold_catch(window: MainWindow, qtbot: QtBot) -> None:
    window.resize(1100, 700)
    window.show()
    qtbot.waitExposed(window)
    meter = window.ui.biteMeter
    qtbot.mouseClick(meter, Qt.MouseButton.LeftButton, pos=QPoint(50, meter.height() - 1))
    assert window.config.threshold_catch == 0
    assert meter.threshold == 0
    assert FishConfig.load(window.config_path).threshold_catch == 0


def test_thresholds_stay_editable_while_fishing(qtbot: QtBot, tmp_path: Path) -> None:
    w = MainWindow(FishConfig(), tmp_path / "config.json", idle_bot_factory)
    qtbot.addWidget(w)
    w.toggle_fishing()
    assert w.worker is not None
    assert w.ui.thresholdCatchSpinBox.isEnabled()
    assert not w.ui.castKeyEdit.isEnabled()
    assert w.ui.statusLed.text == "Casting"
    with qtbot.waitSignal(w.worker.finished, timeout=5000):
        pass
    assert w.ui.statusLed.text == "Idle"
    assert not w.ui.statusLed.pulse


def test_status_messages_reach_log_panel(window: MainWindow) -> None:
    logging.getLogger("getthefish.bot").warning("hello log")
    assert "hello log" in window.ui.logView.toPlainText()


def test_color_picker_loupe(qtbot: QtBot) -> None:
    picker = ColorPicker(_solid_pixmap(QColor(10, 20, 30)))
    qtbot.addWidget(picker)
    picker.show()
    qtbot.mouseMove(picker, QPoint(5, 5))
    assert picker.cursor_pos == QPoint(5, 5)
    picker.grab()  # paints the loupe


def test_compact_view_toggle_is_remembered(window: MainWindow, qtbot: QtBot) -> None:
    window.ui.viewButton.click()
    assert window.ui.pages.currentWidget() is window.ui.compactPage
    window.close()
    reopened = MainWindow(FishConfig(), window.config_path, idle_bot_factory)
    qtbot.addWidget(reopened)
    assert reopened.compact
    reopened.ui.viewButton.click()
    assert reopened.ui.pages.currentWidget() is reopened.ui.fullPage


def test_session_uses_compact_view(window: MainWindow, qtbot: QtBot) -> None:
    window.toggle_fishing()
    assert window.worker is not None
    assert window.compact
    assert window.ui.compactStartButton.text() == "Stop"
    with qtbot.waitSignal(window.worker.finished, timeout=5000):
        pass
    assert not window.compact
    assert window.ui.compactStartButton.text() == "Start"


def test_theme_toggle_is_remembered(window: MainWindow, qtbot: QtBot) -> None:
    window.set_dark(True)
    window.ui.themeButton.click()
    assert not window.dark
    assert theme.colors() is theme.LIGHT
    window.close()
    reopened = MainWindow(FishConfig(), window.config_path, idle_bot_factory)
    qtbot.addWidget(reopened)
    assert not reopened.dark


def test_start_refused_when_window_covers_fishing_area(window: MainWindow, qtbot: QtBot) -> None:
    window.show()
    qtbot.waitExposed(window)
    window.config.start_pos, window.config.end_pos = Point(0, 0), Point(4000, 3000)
    window.toggle_fishing()
    assert window.worker is None
    assert "covers the fishing area" in window.ui.statusbar.currentMessage()


def test_statistics_add_up_over_runs_and_restarts(window: MainWindow, qtbot: QtBot) -> None:
    for _ in range(2):
        window.toggle_fishing()
        assert window.worker is not None
        with qtbot.waitSignal(window.worker.finished, timeout=5000):
            pass
    # idle_bot_factory never finds the bobber: 3 casts per run, no catches.
    assert window.ui.castsValue.text() == "6"
    assert window.ui.todayCastsValue.text() == "6"
    assert window.ui.totalCastsValue.text() == "6"
    window.close()

    reopened = MainWindow(FishConfig(), window.config_path, idle_bot_factory)
    qtbot.addWidget(reopened)
    assert reopened.ui.castsValue.text() == "0"
    assert reopened.ui.todayCastsValue.text() == "6"
    assert reopened.ui.totalCastsValue.text() == "6"
    assert reopened.ui.compactTodayCatches.text() == "0"
    assert reopened.ui.compactSessionCatches.text() == "0"


def test_status_led_and_round_history(window: MainWindow) -> None:
    window.handle_event(PhaseChanged(Phase.WAITING))
    assert window.ui.statusLed.text == "Waiting for bite"
    assert window.ui.statusLed.tone == "accent"
    assert window.ui.statusLed.pulse
    window.ui.statusLed.grab()  # paints the glow
    window.handle_event(RoundFinished(True, Stats(casts=1, catches=1)))
    assert window.ui.statusLed.text == "Caught"
    assert not window.ui.statusLed.pulse
    window.handle_event(RoundFinished(False, Stats(casts=2, catches=1, misses=1)))
    window.handle_event(RoundFinished(None, Stats(casts=3, catches=1, misses=1)))
    assert window.ui.statusLed.text == "No bobber"
    assert window.ui.statusLed.tone == "danger"
    window.handle_event(RoundFinished(False, Stats(casts=4, catches=1, misses=1)))  # stopped
    assert list(window.ui.roundHistory.outcomes) == ["caught", "missed", "no_bobber"]
    assert list(window.ui.compactRoundHistory.outcomes) == ["caught", "missed", "no_bobber"]
    window.ui.compactRoundHistory.grab()  # paints the dots

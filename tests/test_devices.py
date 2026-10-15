from __future__ import annotations

import sys
import types
from typing import Any

import numpy as np
import pytest

from getthefish.config import Point
from getthefish.devices import AbortedError, MssScreen, PyAutoGuiInput, is_known_key


class FakeSct:
    def __init__(self) -> None:
        self.monitors: list[dict[str, int]] = []

    def grab(self, monitor: dict[str, int]) -> Any:
        self.monitors.append(monitor)
        bgra = np.zeros((monitor["height"], monitor["width"], 4), dtype=np.uint8)
        bgra[..., 0], bgra[..., 1], bgra[..., 2], bgra[..., 3] = 30, 20, 10, 255
        return bgra


def test_mss_screen_converts_bgra_to_rgb(monkeypatch: pytest.MonkeyPatch) -> None:
    sct = FakeSct()
    monkeypatch.setitem(sys.modules, "mss", types.SimpleNamespace(mss=lambda: sct))

    img = MssScreen().grab((5, 6, 9, 8))

    assert sct.monitors == [{"left": 5, "top": 6, "width": 4, "height": 2}]
    assert img.shape == (2, 4, 3)
    assert img[0, 0].tolist() == [10, 20, 30]


class FakeFailSafeError(Exception):
    pass


@pytest.fixture
def pyautogui(monkeypatch: pytest.MonkeyPatch) -> types.SimpleNamespace:
    calls: list[tuple[str, Any]] = []
    module = types.SimpleNamespace(
        FAILSAFE=False,
        FailSafeException=FakeFailSafeError,
        calls=calls,
        position=lambda: (3, 4),
        moveTo=lambda x, y: calls.append(("move", (x, y))),
        click=lambda button: calls.append(("click", button)),
        press=lambda key: calls.append(("press", key)),
        KEYBOARD_KEYS=["0", "f", "f1"],
    )
    monkeypatch.setitem(sys.modules, "pyautogui", module)
    return module


def test_pyautogui_input(pyautogui: types.SimpleNamespace) -> None:
    mouse = PyAutoGuiInput()
    assert pyautogui.FAILSAFE is True
    assert mouse.position() == Point(3, 4)
    mouse.move_to(Point(7, 8))
    mouse.right_click()
    mouse.left_click()
    mouse.press("0")
    assert pyautogui.calls == [
        ("move", (7, 8)),
        ("click", "right"),
        ("click", "left"),
        ("press", "0"),
    ]


def test_pyautogui_rejects_unknown_key(pyautogui: types.SimpleNamespace) -> None:
    with pytest.raises(ValueError, match="Unknown key"):
        PyAutoGuiInput().press("nokey")
    assert pyautogui.calls == []


def test_is_known_key(pyautogui: types.SimpleNamespace) -> None:
    assert is_known_key("f1")
    assert not is_known_key("nokey")


def test_pyautogui_failsafe_becomes_aborted(pyautogui: types.SimpleNamespace) -> None:
    def fail(*_: object, **__: object) -> None:
        raise FakeFailSafeError

    pyautogui.moveTo = pyautogui.click = pyautogui.press = fail
    mouse = PyAutoGuiInput()
    with pytest.raises(AbortedError):
        mouse.move_to(Point(0, 0))
    with pytest.raises(AbortedError):
        mouse.right_click()
    with pytest.raises(AbortedError):
        mouse.left_click()
    with pytest.raises(AbortedError):
        mouse.press("0")

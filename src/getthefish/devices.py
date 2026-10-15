"""Screen capture and mouse control behind small, replaceable interfaces.

The real implementations import ``mss`` / ``pyautogui`` lazily, because both
need a display at import or construction time. Tests use fakes instead.
"""

from __future__ import annotations

from typing import Any, Protocol

import numpy as np

from getthefish.config import Point
from getthefish.detection import Image


class AbortedError(Exception):
    """Raised by an input controller when the user triggers the fail-safe."""


class ScreenSource(Protocol):
    def grab(self, bbox: tuple[int, int, int, int]) -> Image:
        """Return the RGB pixels of ``(left, top, right, bottom)``."""
        ...


class InputController(Protocol):
    def position(self) -> Point: ...

    def move_to(self, point: Point) -> None: ...

    def right_click(self) -> None: ...

    def left_click(self) -> None: ...

    def press(self, key: str) -> None: ...


def is_known_key(key: str) -> bool:
    """True if pyautogui knows the key name (assumed True when it cannot be imported)."""
    try:
        import pyautogui
    except Exception:  # no display, e.g. headless CI
        return True
    return key in pyautogui.KEYBOARD_KEYS


class MssScreen:
    """Screen capture via ``mss`` (physical pixels, all monitors)."""

    def __init__(self) -> None:
        self._sct: Any = None

    def grab(self, bbox: tuple[int, int, int, int]) -> Image:
        if self._sct is None:
            # mss handles are thread-local, so create it in the worker thread on first use.
            import mss

            self._sct = mss.mss()
        left, top, right, bottom = bbox
        shot = self._sct.grab(
            {"left": left, "top": top, "width": right - left, "height": bottom - top}
        )
        # mss returns BGRA; drop alpha and convert to RGB.
        return np.ascontiguousarray(np.asarray(shot)[:, :, 2::-1])


class PyAutoGuiInput:
    """Mouse control via ``pyautogui`` with its corner fail-safe enabled."""

    def __init__(self) -> None:
        import pyautogui

        pyautogui.FAILSAFE = True
        self._pg = pyautogui

    def position(self) -> Point:
        x, y = self._pg.position()
        return Point(int(x), int(y))

    def move_to(self, point: Point) -> None:
        try:
            self._pg.moveTo(point.x, point.y)
        except self._pg.FailSafeException as e:
            raise AbortedError("Fail-safe triggered (mouse moved to a screen corner)") from e

    def right_click(self) -> None:
        try:
            self._pg.click(button="right")
        except self._pg.FailSafeException as e:
            raise AbortedError("Fail-safe triggered (mouse moved to a screen corner)") from e

    def left_click(self) -> None:
        try:
            self._pg.click(button="left")
        except self._pg.FailSafeException as e:
            raise AbortedError("Fail-safe triggered (mouse moved to a screen corner)") from e

    def press(self, key: str) -> None:
        if key not in self._pg.KEYBOARD_KEYS:
            raise ValueError(f"Unknown key {key!r} (use names like 0, f, f1, num0)")
        try:
            self._pg.press(key)
        except self._pg.FailSafeException as e:
            raise AbortedError("Fail-safe triggered (mouse moved to a screen corner)") from e

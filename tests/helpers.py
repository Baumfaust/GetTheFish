"""Test doubles and image helpers shared by the test modules."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from getthefish.bot import Timing
from getthefish.config import Point
from getthefish.detection import Image

NO_DELAY = Timing(
    after_cast=(0, 0),
    between_search_attempts=(0, 0),
    before_catch=(0, 0),
    after_failure=(0, 0),
    after_round=(0, 0),
    bite_timeout=0.5,
    bite_poll_interval=0,
)

BOBBER = (72, 41, 12)
WATER = (20, 60, 120)


def make_image(width: int, height: int, color: tuple[int, int, int] = WATER) -> Image:
    return np.full((height, width, 3), color, dtype=np.uint8)


class FakeScreen:
    """Screen backed by a full-screen RGB array; ``frames`` can change over time."""

    def __init__(self, frames: Callable[[int], Image] | Image) -> None:
        self._frames = frames
        self.grabs = 0

    def grab(self, bbox: tuple[int, int, int, int]) -> Image:
        left, top, right, bottom = bbox
        frame = self._frames(self.grabs) if callable(self._frames) else self._frames
        self.grabs += 1
        return frame[top:bottom, left:right]


class FakeMouse:
    def __init__(self, start: Point | None = None) -> None:
        self.pos = start or Point(0, 0)
        self.events: list[tuple[str, Point | str]] = []

    def position(self) -> Point:
        return self.pos

    def move_to(self, point: Point) -> None:
        self.pos = point
        self.events.append(("move", point))

    def right_click(self) -> None:
        self.events.append(("click", self.pos))

    def left_click(self) -> None:
        self.events.append(("left_click", self.pos))

    def press(self, key: str) -> None:
        self.events.append(("press", key))

    @property
    def clicks(self) -> list[Point | str]:
        """Right-click positions (the catch clicks)."""
        return [p for kind, p in self.events if kind == "click"]

"""The fishing loop: cast, find the bobber, wait for a bite, reel in."""

from __future__ import annotations

import logging
import random
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, replace

from getthefish.config import FishConfig, Point
from getthefish.detection import find_color
from getthefish.devices import AbortedError, InputController, ScreenSource

logger = logging.getLogger(__name__)

Range = tuple[float, float]


@dataclass(frozen=True)
class Timing:
    """Delays (seconds). Ranges are randomised uniformly between the bounds."""

    after_cast: Range = (2.1, 2.9)
    between_search_attempts: Range = (0.5, 1.5)
    before_catch: Range = (0.2, 0.9)
    after_failure: Range = (3.0, 5.0)
    after_round: Range = (2.0, 2.0)
    bite_timeout: float = 20.0
    bite_poll_interval: float = 0.1


MAX_CONSECUTIVE_FAILURES = 3

BITE_WATCH_OFFSET = Point(3, 5)
"""Watched pixel relative to the bobber's top-most pixel (tuned in the original version)."""


@dataclass
class Stats:
    casts: int = 0
    catches: int = 0
    misses: int = 0


@dataclass(frozen=True)
class BobberFound:
    """The bobber landed at ``position``; ``watch`` is the pixel observed for a bite."""

    position: Point
    watch: Point


@dataclass(frozen=True)
class BiteSample:
    """Largest per-channel change of the watched pixel since the bobber landed."""

    change: int


@dataclass(frozen=True)
class RoundFinished:
    """One round is over: True (caught), False (missed) or None (no bobber / error)."""

    result: bool | None
    stats: Stats


Event = BobberFound | BiteSample | RoundFinished
"""Live data for a UI; sent from the fishing thread."""


class GetTheFish:
    """Runs the fishing loop until :meth:`stop` is called or it gives up.

    Thread-safe to stop from another thread (e.g. the GUI).
    """

    def __init__(
        self,
        config: FishConfig,
        screen: ScreenSource,
        mouse: InputController,
        timing: Timing | None = None,
        on_status: Callable[[str], None] | None = None,
        rng: random.Random | None = None,
        on_event: Callable[[Event], None] | None = None,
    ) -> None:
        self.config = config
        self.screen = screen
        self.mouse = mouse
        self.timing = timing or Timing()
        self.stats = Stats()
        self._on_status = on_status
        self.on_event = on_event
        self._rng = rng or random.Random()  # noqa: S311 - timing jitter, not crypto
        self._stop = threading.Event()

    @property
    def is_running(self) -> bool:
        return not self._stop.is_set()

    def stop(self) -> None:
        self._stop.set()

    def _status(self, text: str, *, verbose_only: bool = False) -> None:
        if verbose_only and not self.config.verbose:
            logger.debug(text)
            return
        logger.info(text)
        if self._on_status is not None:
            self._on_status(text)

    def _emit(self, event: Event) -> None:
        if self.on_event is not None:
            self.on_event(event)

    def _sleep(self, delay: Range | float) -> bool:
        """Interruptible sleep. Returns False if stop was requested."""
        seconds = self._rng.uniform(*delay) if isinstance(delay, tuple) else delay
        return not self._stop.wait(seconds)

    def cast(self) -> None:
        """Focus the game with a left-click on the water, then press the Fishing key.

        The click is needed because key presses go to the focused window, which
        is the GUI right after clicking Start. Left-click on water is harmless in
        the game (right-click could trigger click-to-move).
        """
        self.mouse.move_to(self.config.start_pos)
        self.mouse.left_click()
        self.mouse.press(self.config.cast_key)
        self.stats.casts += 1

    def find_bobber(self) -> Point | None:
        """Search the configured area; returns absolute screen coordinates."""
        left, top, right, bottom = self.config.search_area
        for attempt in range(1, self.config.max_attempts + 1):
            self._status(
                f"Searching for bobber (attempt {attempt}/{self.config.max_attempts})",
                verbose_only=True,
            )
            image = self.screen.grab((left, top, right, bottom))
            found = find_color(image, self.config.bobber_color, self.config.threshold_bobber)
            if found is not None:
                pos = Point(left + found.x, top + found.y)
                self._status(f"Bobber found at {pos.x}, {pos.y}", verbose_only=True)
                return pos
            if attempt < self.config.max_attempts and not self._sleep(
                self.timing.between_search_attempts
            ):
                return None
        return None

    def _pixel(self, pos: Point) -> tuple[int, int, int]:
        px = self.screen.grab((pos.x, pos.y, pos.x + 1, pos.y + 1))[0, 0]
        return (int(px[0]), int(px[1]), int(px[2]))

    def wait_for_bite(self, watch: Point) -> bool:
        """Watch one pixel; returns True once any channel changes by more than threshold_catch."""
        initial = self._pixel(watch)
        self._status(
            f"Watching pixel {watch.x}, {watch.y} with colour {initial}", verbose_only=True
        )
        max_change = 0
        deadline = time.monotonic() + self.timing.bite_timeout
        while time.monotonic() < deadline:
            current = self._pixel(watch)
            change = max(abs(a - b) for a, b in zip(current, initial, strict=True))
            self._emit(BiteSample(change))
            if change > self.config.threshold_catch:
                self._status(
                    f"Bite: colour {initial} -> {current} (change {change} > "
                    f"threshold_catch {self.config.threshold_catch})",
                    verbose_only=True,
                )
                return True
            max_change = max(max_change, change)
            if not self._sleep(self.timing.bite_poll_interval):
                return False
        self._status(
            f"No bite within {self.timing.bite_timeout:.0f}s: largest colour change was "
            f"{max_change}, threshold_catch is {self.config.threshold_catch}",
            verbose_only=True,
        )
        return False

    def reel_in(self, bobber: Point) -> None:
        previous = self.mouse.position()
        self.mouse.move_to(bobber)
        self.mouse.right_click()
        if not self.config.jump_to_bobber:
            self.mouse.move_to(previous)

    def fish_once(self) -> bool | None:
        """One round. Returns True (caught), False (missed) or None (no bobber)."""
        self.cast()
        if not self._sleep(self.timing.after_cast):
            return False
        bobber = self.find_bobber()
        if bobber is None:
            return None
        watch = Point(bobber.x + BITE_WATCH_OFFSET.x, bobber.y + BITE_WATCH_OFFSET.y)
        self._emit(BobberFound(bobber, watch))
        if self.config.jump_to_bobber:
            self.mouse.move_to(watch)
        if not self.wait_for_bite(watch):
            self.stats.misses += 1
            self._status("No bite, recasting", verbose_only=True)
            return False
        if not self._sleep(self.timing.before_catch):
            return False
        self.reel_in(watch)
        self.stats.catches += 1
        self._status(f"Fish caught! ({self.stats.catches} total)")
        return True

    def run(self) -> None:
        """Fish until stopped, aborted via fail-safe, or too many failures.

        An instance runs once; create a new one to start fishing again.
        """
        self._status("Started fishing")
        failures = 0
        try:
            while self.is_running:
                try:
                    result = self.fish_once()
                    problem = "Bobber not found"
                except AbortedError:
                    raise
                except Exception as e:
                    logger.exception("Unexpected error in fishing round")
                    result, problem = None, f"Error: {e}"
                self._emit(RoundFinished(result, replace(self.stats)))
                if result is not None:
                    failures = 0
                    self._sleep(self.timing.after_round)
                    continue
                if not self.is_running:
                    break
                failures += 1
                self._status(f"{problem} ({failures}/{MAX_CONSECUTIVE_FAILURES} failures)")
                if failures >= MAX_CONSECUTIVE_FAILURES:
                    self._status("Too many consecutive failures, stopping")
                    break
                self._sleep(self.timing.after_failure)
        except AbortedError as e:
            self._status(str(e))
        finally:
            self._stop.set()
            self._status(
                f"Stopped fishing (casts: {self.stats.casts}, catches: {self.stats.catches})"
            )

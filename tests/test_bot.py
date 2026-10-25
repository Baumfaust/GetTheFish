from __future__ import annotations

import threading
from dataclasses import replace

import pytest

from getthefish.bot import (
    BITE_WATCH_OFFSET,
    MAX_CONSECUTIVE_FAILURES,
    BiteSample,
    BobberFound,
    Event,
    GetTheFish,
    Phase,
    PhaseChanged,
    RoundFinished,
)
from getthefish.config import FishConfig, Point
from getthefish.detection import Image
from getthefish.devices import AbortedError
from helpers import BOBBER, NO_DELAY, FakeMouse, FakeScreen, make_image

SPLASH = (230, 230, 230)
BOBBER_BOX = (slice(40, 46), slice(60, 66))  # rows 40-45, cols 60-65 -> centre (62/63, 42/43)


def scene(bobber: bool = True, bite: bool = False) -> Image:
    img = make_image(200, 150)
    if bobber:
        img[BOBBER_BOX] = SPLASH if bite else BOBBER
    return img


def make_bot(config: FishConfig, screen: FakeScreen, mouse: FakeMouse | None = None) -> GetTheFish:
    return GetTheFish(config, screen, mouse or FakeMouse(), timing=NO_DELAY)


def test_find_bobber_returns_absolute_position(config: FishConfig) -> None:
    bot = make_bot(config, FakeScreen(scene()))
    pos = bot.find_bobber()
    assert pos is not None
    assert 60 <= pos.x <= 65 and 40 <= pos.y <= 45


def test_find_bobber_respects_search_area(config: FishConfig) -> None:
    config.start_pos, config.end_pos = Point(100, 100), Point(200, 150)
    screen = FakeScreen(scene())
    assert make_bot(config, screen).find_bobber() is None
    assert screen.grabs == config.max_attempts


def test_find_bobber_retries_until_found(config: FishConfig) -> None:
    config.max_attempts = 3
    screen = FakeScreen(lambda n: scene(bobber=n >= 2))
    assert make_bot(config, screen).find_bobber() is not None
    assert screen.grabs == 3


def test_wait_for_bite_detects_colour_change(config: FishConfig) -> None:
    screen = FakeScreen(lambda n: scene(bite=n >= 3))
    assert make_bot(config, screen).wait_for_bite(Point(62, 42)) is True


def test_wait_for_bite_times_out(config: FishConfig) -> None:
    bot = GetTheFish(
        config, FakeScreen(scene()), FakeMouse(), timing=replace(NO_DELAY, bite_timeout=0.05)
    )
    assert bot.wait_for_bite(Point(62, 42)) is False


def test_fish_once_full_round(config: FishConfig) -> None:
    mouse = FakeMouse()
    screen = FakeScreen(lambda n: scene(bite=n >= 3))
    bot = make_bot(config, screen, mouse)

    assert bot.fish_once() is True

    # Cast: focus the game with a left-click on the water, then press the Fishing key.
    assert mouse.events[:3] == [
        ("move", config.start_pos),
        ("left_click", config.start_pos),
        ("press", "0"),
    ]
    assert len(mouse.clicks) == 1
    catch_click = mouse.clicks[0]
    # Bobber's top-most pixel (60, 40) plus the original watch offset (3, 5).
    assert catch_click == Point(60 + BITE_WATCH_OFFSET.x, 40 + BITE_WATCH_OFFSET.y)
    assert bot.stats.casts == 1 and bot.stats.catches == 1


def test_events_are_emitted(config: FishConfig) -> None:
    events: list[Event] = []
    screen = FakeScreen(lambda n: scene(bite=n >= 3))
    bot = GetTheFish(config, screen, FakeMouse(), NO_DELAY, on_event=events.append)
    bot.fish_once()
    found = next(e for e in events if isinstance(e, BobberFound))
    assert found.watch == Point(60 + BITE_WATCH_OFFSET.x, 40 + BITE_WATCH_OFFSET.y)
    changes = [e.change for e in events if isinstance(e, BiteSample)]
    assert changes[0] == 0 and changes[-1] > config.threshold_catch


def test_phases_are_emitted_in_order(config: FishConfig) -> None:
    events: list[Event] = []
    screen = FakeScreen(lambda n: scene(bite=n >= 3))
    GetTheFish(config, screen, FakeMouse(), NO_DELAY, on_event=events.append).fish_once()
    phases = [e.phase for e in events if isinstance(e, PhaseChanged)]
    assert phases == [Phase.CASTING, Phase.SEARCHING, Phase.WAITING, Phase.REELING]


def test_stop_while_waiting_is_not_a_miss(config: FishConfig) -> None:
    bot = make_bot(config, FakeScreen(scene()))
    bot.on_event = lambda e: bot.stop() if isinstance(e, BiteSample) else None
    assert bot.fish_once() is False
    assert bot.stats.misses == 0


def test_run_reports_each_round(config: FishConfig) -> None:
    events: list[Event] = []
    bot = GetTheFish(config, FakeScreen(scene(bobber=False)), FakeMouse(), NO_DELAY)
    bot.on_event = events.append
    bot.run()
    rounds = [e for e in events if isinstance(e, RoundFinished)]
    assert len(rounds) == MAX_CONSECUTIVE_FAILURES
    assert all(r.result is None for r in rounds)
    assert [r.stats.casts for r in rounds] == [1, 2, 3]


def test_bite_diagnostics_are_reported(config: FishConfig) -> None:
    config.verbose = True
    statuses: list[str] = []
    bot = GetTheFish(
        config,
        FakeScreen(lambda n: scene(bite=n >= 3)),
        FakeMouse(),
        timing=NO_DELAY,
        on_status=statuses.append,
    )
    bot.fish_once()
    assert any(s.startswith("Watching pixel 63, 45 with colour (72, 41, 12)") for s in statuses)
    assert any("Bite: colour (72, 41, 12) -> (230, 230, 230)" in s for s in statuses)


def test_no_bite_reports_largest_change(config: FishConfig) -> None:
    config.verbose = True
    statuses: list[str] = []
    bot = GetTheFish(
        config,
        FakeScreen(scene()),
        FakeMouse(),
        timing=replace(NO_DELAY, bite_timeout=0.05),
        on_status=statuses.append,
    )
    assert bot.fish_once() is False
    assert any("largest colour change was 0, threshold_catch is 60" in s for s in statuses)


def test_fish_once_without_jump_restores_mouse(config: FishConfig) -> None:
    config.jump_to_bobber = False
    mouse = FakeMouse()
    bot = make_bot(config, FakeScreen(lambda n: scene(bite=n >= 3)), mouse)

    assert bot.fish_once() is True

    # Mouse stays at the cast position while waiting and returns there after the catch.
    assert mouse.pos == config.start_pos
    assert mouse.events[-2][0] == "click"


def test_cast_uses_configured_key(config: FishConfig) -> None:
    config.cast_key = "f1"
    mouse = FakeMouse()
    make_bot(config, FakeScreen(scene()), mouse).cast()
    assert ("press", "f1") in mouse.events


def test_fish_once_no_bobber(config: FishConfig) -> None:
    bot = make_bot(config, FakeScreen(scene(bobber=False)))
    assert bot.fish_once() is None


def test_run_gives_up_after_consecutive_failures(config: FishConfig) -> None:
    statuses: list[str] = []
    bot = GetTheFish(
        config,
        FakeScreen(scene(bobber=False)),
        FakeMouse(),
        timing=NO_DELAY,
        on_status=statuses.append,
    )
    bot.run()
    assert bot.stats.casts == MAX_CONSECUTIVE_FAILURES
    assert not bot.is_running
    assert any("Too many consecutive failures" in s for s in statuses)


def test_run_survives_unexpected_errors(config: FishConfig) -> None:
    class BrokenScreen:
        def grab(self, bbox: tuple[int, int, int, int]) -> Image:
            raise OSError("display gone")

    statuses: list[str] = []
    bot = GetTheFish(
        config, BrokenScreen(), FakeMouse(), timing=NO_DELAY, on_status=statuses.append
    )
    bot.run()
    assert bot.stats.casts == MAX_CONSECUTIVE_FAILURES
    assert "Error: display gone (1/3 failures)" in statuses


def test_run_stops_on_failsafe(config: FishConfig) -> None:
    class AbortingMouse(FakeMouse):
        def press(self, key: str) -> None:
            raise AbortedError("corner")

    statuses: list[str] = []
    bot = GetTheFish(
        config, FakeScreen(scene()), AbortingMouse(), timing=NO_DELAY, on_status=statuses.append
    )
    bot.run()
    assert "corner" in statuses
    assert not bot.is_running


def test_stop_from_other_thread(config: FishConfig) -> None:
    screen = FakeScreen(lambda n: scene(bite=n % 4 == 3))
    bot = make_bot(config, screen)
    thread = threading.Thread(target=bot.run)
    thread.start()
    while bot.stats.catches < 2:
        assert thread.is_alive()
    bot.stop()
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_stop_before_run_does_nothing(config: FishConfig) -> None:
    mouse = FakeMouse()
    bot = make_bot(config, FakeScreen(scene()), mouse)
    bot.stop()
    bot.run()
    assert mouse.events == []


@pytest.mark.parametrize("verbose", [True, False])
def test_verbose_controls_status_detail(config: FishConfig, verbose: bool) -> None:
    config.verbose = verbose
    statuses: list[str] = []
    bot = GetTheFish(
        config,
        FakeScreen(lambda n: scene(bite=n >= 3)),
        FakeMouse(),
        timing=NO_DELAY,
        on_status=statuses.append,
    )
    bot.fish_once()
    assert any("Fish caught" in s for s in statuses)
    assert any("Searching" in s for s in statuses) is verbose

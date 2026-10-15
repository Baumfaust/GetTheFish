from __future__ import annotations

import os

import pytest

from getthefish.config import FishConfig, Point
from helpers import BOBBER

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture
def config() -> FishConfig:
    return FishConfig(
        bobber_color=BOBBER,
        threshold_bobber=18,
        threshold_catch=60,
        start_pos=Point(10, 10),
        end_pos=Point(110, 90),
        max_attempts=2,
    )

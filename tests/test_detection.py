import numpy as np

from getthefish.config import Point
from getthefish.detection import color_mask, colors_differ, find_color
from helpers import BOBBER, make_image


def test_color_mask_threshold_is_inclusive() -> None:
    img = make_image(3, 1)
    img[0, 0] = (90, 41, 12)  # +18 on red
    img[0, 1] = (91, 41, 12)  # +19 on red
    assert color_mask(img, BOBBER, 18).tolist() == [[True, False, False]]


def test_find_color_none_when_absent() -> None:
    assert find_color(make_image(50, 50), BOBBER, 18) is None


def test_find_color_returns_first_pixel_of_blob() -> None:
    img = make_image(100, 80)
    img[40:45, 60:65] = BOBBER
    assert find_color(img, BOBBER, 18) == Point(60, 40)


def test_find_color_matches_original_first_match_on_irregular_bobber() -> None:
    """Without noise the result equals the original scan-order first match."""
    img = make_image(100, 80)
    img[30, 52:55] = BOBBER  # thin tip
    img[31:40, 45:60] = BOBBER  # wider body
    assert find_color(img, BOBBER, 18) == Point(52, 30)


def test_find_color_ignores_isolated_noise() -> None:
    img = make_image(100, 80)
    img[2, 2] = BOBBER  # single stray pixel, found first in scan order
    img[50:58, 70:78] = BOBBER
    found = find_color(img, BOBBER, 18)
    assert found is not None
    assert 70 <= found.x < 78 and 50 <= found.y < 58


def test_find_color_handles_uint8_without_overflow() -> None:
    img = make_image(4, 4, (250, 250, 250))
    assert find_color(img, (5, 5, 5), 10) is None
    img[1, 1] = (0, 0, 0)
    assert find_color(img, (5, 5, 5), 10) == Point(1, 1)


def test_colors_differ() -> None:
    assert not colors_differ((10, 10, 10), (70, 10, 10), 60)
    assert colors_differ((10, 10, 10), (71, 10, 10), 60)
    assert colors_differ(np.array([255, 0, 0], dtype=np.uint8), (0, 0, 0), 60)

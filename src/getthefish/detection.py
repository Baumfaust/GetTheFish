"""Pure image-processing helpers (no screen or input access)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np
import numpy.typing as npt

from getthefish.config import Point

Image = npt.NDArray[np.uint8]
"""An ``(height, width, 3)`` RGB image."""

ColorLike = Sequence[int] | npt.NDArray[Any]

CLUSTER_CELL_SIZE = 16
"""Grid size in pixels used to group matching pixels into clusters."""


def color_mask(image: Image, color: ColorLike, threshold: int) -> npt.NDArray[np.bool_]:
    """Boolean mask of pixels whose every RGB channel is within ``threshold`` of ``color``."""
    target = np.asarray(color, dtype=np.int16)
    diff = np.abs(image.astype(np.int16) - target)
    return np.all(diff <= threshold, axis=2)


def find_color(
    image: Image,
    color: ColorLike,
    threshold: int,
    cell_size: int = CLUSTER_CELL_SIZE,
) -> Point | None:
    """Locate the first (top-most, then left-most) pixel of the main ``color`` blob.

    Matching pixels are grouped on a ``cell_size`` grid to find the densest
    cluster, which ignores isolated noise pixels elsewhere. Within two cells
    of that cluster the first pixel in scan order is returned (relative to the
    image) - the same anchor the original first-match search used, so the
    bite-watch offset stays valid.
    """
    ys, xs = np.nonzero(color_mask(image, color, threshold))
    if len(xs) == 0:
        return None
    cells = (ys // cell_size) * (image.shape[1] // cell_size + 1) + (xs // cell_size)
    in_cell = cells == int(np.argmax(np.bincount(cells)))
    cx, cy = xs[in_cell].mean(), ys[in_cell].mean()
    near = (np.abs(xs - cx) <= 2 * cell_size) & (np.abs(ys - cy) <= 2 * cell_size)
    # np.nonzero yields pixels in row-major order, so the first one is top-most, left-most.
    first = int(np.argmax(near))
    return Point(int(xs[first]), int(ys[first]))


def colors_differ(color1: ColorLike, color2: ColorLike, threshold: int) -> bool:
    """True if any RGB channel differs by more than ``threshold``."""
    diff = np.abs(np.asarray(color1, dtype=np.int16) - np.asarray(color2, dtype=np.int16))
    return bool(np.any(diff > threshold))

from __future__ import annotations

import struct
from pathlib import Path

import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pytestqt")

from PySide6.QtGui import QColor
from pytestqt.qtbot import QtBot

from getthefish.gui.icon import SIZES, app_icon, main, render


def test_render_draws_on_transparent_corners(qtbot: QtBot) -> None:
    image = render(64)
    assert image.pixelColor(0, 0).alpha() == 0
    assert image.pixelColor(25, 35) == QColor("white")  # fish body
    assert not app_icon().isNull()


def test_writes_multi_size_ico(qtbot: QtBot, tmp_path: Path) -> None:
    out = tmp_path / "icons" / "app.ico"
    assert main(["icon", str(out)]) == 0
    data = out.read_bytes()
    reserved, kind, count = struct.unpack_from("<HHH", data)
    assert (reserved, kind, count) == (0, 1, len(SIZES))
    first_offset = struct.unpack_from("<I", data, 6 + 12)[0]
    assert data[first_offset : first_offset + 8] == b"\x89PNG\r\n\x1a\n"


def test_usage_error() -> None:
    assert main(["icon"]) == 2

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar

import pytest

import getthefish.__main__ as cli
from getthefish.config import FishConfig


class RecordingBot:
    instances: ClassVar[list[RecordingBot]] = []

    def __init__(self, config: FishConfig, *_: object, **__: object) -> None:
        self.config = config
        self.ran = False
        RecordingBot.instances.append(self)

    def run(self) -> None:
        self.ran = True

    def stop(self) -> None:
        pass


@pytest.fixture(autouse=True)
def fake_devices(monkeypatch: pytest.MonkeyPatch) -> None:
    RecordingBot.instances.clear()
    monkeypatch.setattr(cli, "GetTheFish", RecordingBot)
    monkeypatch.setattr(cli, "MssScreen", lambda: None)
    monkeypatch.setattr(cli, "PyAutoGuiInput", lambda: None)
    monkeypatch.setattr("signal.signal", lambda *_: None)


def test_creates_default_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "cfg" / "config.json"
    assert cli.main(["--config", str(path)]) == 0
    assert FishConfig.load(path) == FishConfig()
    assert RecordingBot.instances[0].ran


def test_verbose_flag(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert cli.main(["--config", str(tmp_path / "c.json"), "-v"]) == 0
    assert RecordingBot.instances[0].config.verbose


def test_invalid_config_exits_with_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "c.json"
    path.write_text(json.dumps({"threshold_bobber": 999}))
    assert cli.main(["--config", str(path)]) == 2
    assert RecordingBot.instances == []

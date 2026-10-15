import json
from pathlib import Path

import pytest

from getthefish.config import (
    ConfigError,
    FishConfig,
    Point,
    default_config_path,
    load_or_migrate,
)

LEGACY_JSONPICKLE = {
    "py/object": "getthefish.FishConfig",
    "bobbercolor": {"py/tuple": [72, 41, 12]},
    "endPos": {"py/object": "getthefish.Point", "x": 1100, "y": 400},
    "jumpToBobber": True,
    "startPos": {"py/object": "getthefish.Point", "x": 200, "y": 50},
    "thresholdBobber": 18,
    "thresholdCatch": 60,
    "verbose": False,
}


def test_defaults_are_valid() -> None:
    c = FishConfig()
    assert c.bobber_color == (72, 41, 12)
    assert c.search_area == (200, 50, 1100, 400)


def test_roundtrip(tmp_path: Path) -> None:
    original = FishConfig(
        bobber_color=(1, 2, 3),
        threshold_bobber=5,
        threshold_catch=70,
        jump_to_bobber=False,
        verbose=True,
        start_pos=Point(1, 2),
        end_pos=Point(30, 40),
        max_attempts=7,
        cast_key="f1",
    )
    path = tmp_path / "sub" / "config.json"
    original.save(path)
    assert FishConfig.load(path) == original
    assert json.loads(path.read_text())["start_pos"] == {"x": 1, "y": 2}


def test_load_missing_file_returns_defaults(tmp_path: Path) -> None:
    assert FishConfig.load(tmp_path / "nope.json") == FishConfig()


def test_missing_keys_use_defaults() -> None:
    assert FishConfig.from_dict({"threshold_catch": 42}) == FishConfig(threshold_catch=42)


def test_cast_key_defaults_to_zero_and_is_normalised() -> None:
    assert FishConfig().cast_key == "0"
    assert FishConfig.from_dict({"cast_key": " F1 "}).cast_key == "f1"


def test_legacy_jsonpickle_format_is_migrated() -> None:
    c = FishConfig.from_dict(LEGACY_JSONPICKLE)
    assert c == FishConfig(
        bobber_color=(72, 41, 12),
        start_pos=Point(200, 50),
        end_pos=Point(1100, 400),
    )


def test_load_or_migrate_imports_legacy_file(tmp_path: Path) -> None:
    legacy = tmp_path / "config.json"
    legacy.write_text(json.dumps(LEGACY_JSONPICKLE))
    target = tmp_path / "user" / "config.json"

    c = load_or_migrate(target, legacy_path=legacy)

    assert c.start_pos == Point(200, 50)
    assert "py/object" not in target.read_text()
    assert FishConfig.load(target) == c


def test_load_or_migrate_prefers_existing_target(tmp_path: Path) -> None:
    legacy = tmp_path / "legacy.json"
    legacy.write_text(json.dumps(LEGACY_JSONPICKLE))
    target = tmp_path / "config.json"
    FishConfig(threshold_bobber=3).save(target)

    assert load_or_migrate(target, legacy_path=legacy).threshold_bobber == 3


@pytest.mark.parametrize(
    "content",
    ["{not json", "[1, 2]", '{"bobber_color": [1, 2]}', '{"start_pos": {"x": 1}}'],
)
def test_invalid_file_raises(tmp_path: Path, content: str) -> None:
    path = tmp_path / "config.json"
    path.write_text(content)
    with pytest.raises(ConfigError):
        FishConfig.load(path)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"bobber_color": (256, 0, 0)},
        {"bobber_color": (-1, 0, 0)},
        {"threshold_bobber": -1},
        {"threshold_catch": 300},
        {"max_attempts": 0},
        {"cast_key": ""},
        {"cast_key": "F1"},
        {"cast_key": "page up"},
        {"cast_key": "x" * 21},
        {"start_pos": Point(100, 100), "end_pos": Point(50, 200)},
        {"start_pos": Point(10, 10), "end_pos": Point(10, 20)},
    ],
)
def test_validation(kwargs: dict[str, object]) -> None:
    with pytest.raises(ConfigError):
        FishConfig(**kwargs)  # type: ignore[arg-type]


def test_default_config_path_env_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("GETTHEFISH_CONFIG", str(tmp_path / "x.json"))
    assert default_config_path() == tmp_path / "x.json"


def test_default_config_path_is_per_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GETTHEFISH_CONFIG", raising=False)
    path = default_config_path()
    assert path.name == "config.json"
    assert path.parent.name == "getthefish"
    assert path.is_absolute()

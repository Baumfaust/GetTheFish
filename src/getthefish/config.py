"""Configuration model, validation and persistence."""

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

Color = tuple[int, int, int]

APP_NAME = "getthefish"
CONFIG_FILENAME = "config.json"
CONFIG_ENV_VAR = "GETTHEFISH_CONFIG"
MAX_KEY_LENGTH = 20


def normalize_key(value: object) -> str:
    """Key names are case-insensitive for the user; pyautogui expects lower case."""
    return str(value).strip().lower()


class ConfigError(ValueError):
    """Raised when configuration data is invalid."""


@dataclass(frozen=True)
class Point:
    """A screen coordinate in physical pixels."""

    x: int
    y: int


@dataclass
class FishConfig:
    """User-tunable settings of the fishing bot."""

    bobber_color: Color = (72, 41, 12)
    threshold_bobber: int = 18
    threshold_catch: int = 60
    jump_to_bobber: bool = True
    verbose: bool = False
    start_pos: Point = field(default_factory=lambda: Point(200, 50))
    end_pos: Point = field(default_factory=lambda: Point(1100, 400))
    max_attempts: int = 3
    cast_key: str = "0"
    """Key bound to the Fishing spell in the game (pyautogui key name, e.g. 0, f, f1)."""

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Raise :class:`ConfigError` if any value is out of range."""
        if len(self.bobber_color) != 3 or not all(
            isinstance(c, int) and 0 <= c <= 255 for c in self.bobber_color
        ):
            raise ConfigError(
                f"bobber_color must be three integers 0-255, got {self.bobber_color!r}"
            )
        for name in ("threshold_bobber", "threshold_catch"):
            value = getattr(self, name)
            if not isinstance(value, int) or not 0 <= value <= 255:
                raise ConfigError(f"{name} must be an integer 0-255, got {value!r}")
        if not isinstance(self.max_attempts, int) or self.max_attempts < 1:
            raise ConfigError(f"max_attempts must be a positive integer, got {self.max_attempts!r}")
        if (
            not isinstance(self.cast_key, str)
            or not 0 < len(self.cast_key) <= MAX_KEY_LENGTH
            or self.cast_key != normalize_key(self.cast_key)
            or " " in self.cast_key
        ):
            raise ConfigError(
                f"cast_key must be a lower-case key name like 0, f or f1, got {self.cast_key!r}"
            )
        if self.start_pos.x >= self.end_pos.x or self.start_pos.y >= self.end_pos.y:
            raise ConfigError(
                f"start_pos {self.start_pos} must be above and left of end_pos {self.end_pos}"
            )

    @property
    def search_area(self) -> tuple[int, int, int, int]:
        """Search area as ``(left, top, right, bottom)``."""
        return (self.start_pos.x, self.start_pos.y, self.end_pos.x, self.end_pos.y)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["bobber_color"] = list(self.bobber_color)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FishConfig:
        """Build a config from a dict; missing keys use defaults.

        Both the current snake_case format and the legacy jsonpickle /
        camelCase format written by older versions are accepted.
        """
        data = _migrate_legacy(data)
        defaults = cls()
        try:
            return cls(
                bobber_color=_to_color(data.get("bobber_color", defaults.bobber_color)),
                threshold_bobber=int(data.get("threshold_bobber", defaults.threshold_bobber)),
                threshold_catch=int(data.get("threshold_catch", defaults.threshold_catch)),
                jump_to_bobber=bool(data.get("jump_to_bobber", defaults.jump_to_bobber)),
                verbose=bool(data.get("verbose", defaults.verbose)),
                start_pos=_to_point(data.get("start_pos"), defaults.start_pos),
                end_pos=_to_point(data.get("end_pos"), defaults.end_pos),
                max_attempts=int(data.get("max_attempts", defaults.max_attempts)),
                cast_key=normalize_key(data.get("cast_key", defaults.cast_key)),
            )
        except ConfigError:
            raise
        except (TypeError, ValueError, KeyError) as e:
            raise ConfigError(f"Invalid config data: {e!r}") from e

    def save(self, path: Path) -> None:
        """Write the config as JSON, creating parent directories as needed."""
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(self.to_dict(), indent=4), encoding="utf-8")
        tmp.replace(path)
        logger.debug("Config saved to %s", path)

    @classmethod
    def load(cls, path: Path) -> FishConfig:
        """Load a config file; returns defaults if the file does not exist.

        Raises :class:`ConfigError` if the file exists but is invalid, so a
        broken config is never silently replaced.
        """
        if not path.exists():
            logger.info("No config file at %s, using defaults", path)
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ConfigError(f"{path} is not valid JSON: {e}") from e
        if not isinstance(data, dict):
            raise ConfigError(f"{path} must contain a JSON object")
        logger.info("Config loaded from %s", path)
        return cls.from_dict(data)


def default_config_path() -> Path:
    """Per-user config location (overridable via ``GETTHEFISH_CONFIG``)."""
    if env := os.environ.get(CONFIG_ENV_VAR):
        return Path(env)
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / APP_NAME / CONFIG_FILENAME


def load_or_migrate(path: Path, legacy_path: Path = Path(CONFIG_FILENAME)) -> FishConfig:
    """Load ``path``; if missing, import a legacy ``./config.json`` once."""
    if not path.exists() and legacy_path.exists() and legacy_path.resolve() != path.resolve():
        logger.info("Migrating legacy config %s to %s", legacy_path, path)
        config = FishConfig.load(legacy_path)
        config.save(path)
        return config
    return FishConfig.load(path)


_LEGACY_KEYS = {
    "bobbercolor": "bobber_color",
    "thresholdBobber": "threshold_bobber",
    "thresholdCatch": "threshold_catch",
    "jumpToBobber": "jump_to_bobber",
    "startPos": "start_pos",
    "endPos": "end_pos",
}


def _migrate_legacy(data: dict[str, Any]) -> dict[str, Any]:
    """Translate camelCase keys and jsonpickle wrappers into plain values."""
    migrated: dict[str, Any] = {}
    for key, value in data.items():
        if key == "py/object":
            continue
        migrated[_LEGACY_KEYS.get(key, key)] = _unwrap_jsonpickle(value)
    return migrated


def _unwrap_jsonpickle(value: Any) -> Any:
    if isinstance(value, dict):
        if "py/tuple" in value:
            return list(value["py/tuple"])
        return {k: v for k, v in value.items() if k != "py/object"}
    return value


def _to_color(value: Any) -> Color:
    items = list(value)
    if len(items) != 3:
        raise ConfigError(f"bobber_color must have 3 components, got {value!r}")
    return (int(items[0]), int(items[1]), int(items[2]))


def _to_point(value: Any, default: Point) -> Point:
    if value is None:
        return default
    if isinstance(value, dict):
        return Point(int(value["x"]), int(value["y"]))
    x, y = value
    return Point(int(x), int(y))

"""Catch statistics summed over sessions, and a per-day history on disk."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, fields
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

STATS_FILENAME = "stats.json"


@dataclass
class Tally:
    casts: int = 0
    catches: int = 0
    misses: int = 0
    seconds: float = 0.0
    """Time spent fishing (not idle time between sessions)."""

    def add(self, other: Tally) -> None:
        self.casts += other.casts
        self.catches += other.catches
        self.misses += other.misses
        self.seconds += other.seconds

    @property
    def catch_rate(self) -> float | None:
        """Catches per cast in percent, None before the first cast."""
        return 100 * self.catches / self.casts if self.casts else None

    def per_hour(self, seconds: float | None = None) -> float | None:
        """Catches per hour of fishing, None in the first minute (too jumpy to be useful)."""
        seconds = self.seconds if seconds is None else seconds
        return self.catches / seconds * 3600 if seconds >= 60 else None


class DailyHistory:
    """One :class:`Tally` per calendar day, stored as JSON (``{"YYYY-MM-DD": {...}}``)."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.days: dict[str, Tally] = {}
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            names = {f.name for f in fields(Tally)}
            self.days = {
                day: Tally(**{k: v for k, v in values.items() if k in names})
                for day, values in raw.items()
            }
        except FileNotFoundError:
            pass
        except (OSError, ValueError, TypeError, AttributeError) as e:
            logger.warning("Ignoring unreadable statistics file %s: %s", path, e)

    def today(self, day: date | None = None) -> Tally:
        return self.days.setdefault((day or date.today()).isoformat(), Tally())

    def total(self) -> Tally:
        """All days added up."""
        total = Tally()
        for tally in self.days.values():
            total.add(tally)
        return total

    def save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            data = {day: asdict(t) for day, t in sorted(self.days.items())}
            self.path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        except OSError as e:
            logger.warning("Could not save statistics to %s: %s", self.path, e)

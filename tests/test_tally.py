from __future__ import annotations

from datetime import date
from pathlib import Path

from getthefish.tally import DailyHistory, Tally


def test_rates() -> None:
    assert Tally().catch_rate is None
    assert Tally().per_hour() is None
    t = Tally(casts=4, catches=3, misses=1, seconds=1800)
    assert t.catch_rate == 75
    assert t.per_hour() == 6
    assert t.per_hour(59) is None


def test_history_round_trip_and_total(tmp_path: Path) -> None:
    path = tmp_path / "stats.json"
    history = DailyHistory(path)
    history.today(date(2026, 10, 24)).add(Tally(casts=5, catches=4, seconds=100))
    history.today(date(2026, 10, 25)).add(Tally(casts=2, catches=1, misses=1, seconds=50))
    history.save()

    reloaded = DailyHistory(path)
    assert reloaded.today(date(2026, 10, 25)) == Tally(2, 1, 1, 50)
    assert reloaded.total() == Tally(7, 5, 1, 150)
    assert reloaded.today(date(2026, 10, 26)) == Tally()


def test_unreadable_history_starts_empty(tmp_path: Path) -> None:
    path = tmp_path / "stats.json"
    path.write_text("not json", encoding="utf-8")
    assert DailyHistory(path).total() == Tally()

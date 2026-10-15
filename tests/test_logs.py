import logging
from pathlib import Path

import pytest

from getthefish.logs import LOG_FILENAME, setup_logging


@pytest.fixture(autouse=True)
def restore_logging():  # type: ignore[no-untyped-def]
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    yield
    for h in root.handlers:
        if h not in handlers:
            h.close()
    root.handlers, root.level = handlers, level


def test_writes_log_file(tmp_path: Path) -> None:
    log_file = setup_logging(tmp_path / "logs")
    assert log_file == tmp_path / "logs" / LOG_FILENAME
    logging.getLogger("getthefish.test").info("hello")
    for h in logging.getLogger().handlers:
        h.flush()
    assert "hello" in log_file.read_text(encoding="utf-8")


def test_unwritable_dir_falls_back_to_console(tmp_path: Path) -> None:
    blocker = tmp_path / "file"
    blocker.write_text("")
    assert setup_logging(blocker / "sub") is None

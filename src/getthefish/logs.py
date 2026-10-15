"""Logging setup shared by the CLI and the GUI."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FILENAME = "getthefish.log"
FORMAT = "%(asctime)s %(levelname)s %(message)s"


def setup_logging(log_dir: Path) -> Path | None:
    """Log to stderr and to a small rotating file in ``log_dir``.

    Returns the log file path, or None if the file could not be opened.
    The windowed exe has no console, so the file is the only place to see
    diagnostics there.
    """
    handlers: list[logging.Handler] = []
    if sys.stderr is not None:  # None in the windowed exe
        handlers.append(logging.StreamHandler())
    log_file = log_dir / LOG_FILENAME
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        handlers.append(
            RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=2, encoding="utf-8")
        )
    except OSError:
        logging.basicConfig(level=logging.INFO, format=FORMAT, handlers=handlers, force=True)
        return None
    logging.basicConfig(level=logging.INFO, format=FORMAT, handlers=handlers, force=True)
    return log_file

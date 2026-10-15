"""Command-line entry point: ``getthefish`` / ``python -m getthefish``."""

from __future__ import annotations

import argparse
import logging
import signal
import sys
from pathlib import Path

from getthefish import __version__
from getthefish.bot import GetTheFish
from getthefish.config import ConfigError, default_config_path, load_or_migrate
from getthefish.devices import MssScreen, PyAutoGuiInput
from getthefish.logs import setup_logging


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="getthefish", description="Run the fishing bot headless with the saved config."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help=f"config file (default: {default_config_path()})",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="log every step")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    config_path = args.config or default_config_path()
    if log_file := setup_logging(config_path.parent):
        logging.info("Logging to %s", log_file)
    try:
        config = load_or_migrate(config_path)
    except ConfigError as e:
        logging.error("Invalid configuration: %s", e)
        return 2
    if args.verbose:
        config.verbose = True
    if not config_path.exists():
        config.save(config_path)
        logging.info("Wrote default config to %s - adjust it or use getthefish-gui", config_path)

    bot = GetTheFish(config, MssScreen(), PyAutoGuiInput())
    signal.signal(signal.SIGINT, lambda *_: bot.stop())
    logging.info("Press Ctrl+C or move the mouse to a screen corner to stop")
    bot.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())

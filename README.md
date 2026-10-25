# Get The Fish

[![CI](../../actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)

An automated fishing tool. It casts the line, finds the bobber by its colour,
watches it for a bite and reels the fish in. A PySide6 GUI lets you pick the
bobber colour and the search area directly on screen, shows each round live and
keeps statistics. A compact view fits beside the game in windowed mode.

> **Note:** The tool moves the mouse and reads the screen. Only use it where
> automation is allowed by the game's terms of service.

## Requirements

- Python 3.12 or newer (Python 3.15 is the current project default)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for installation and dependency management
- Windows (primary target). Linux/macOS work for development; on macOS the
  terminal needs *Screen Recording* and *Accessibility* permissions.

## Installation

### Windows (PowerShell)

```powershell
git clone <repository-url> GetTheFish
cd GetTheFish
uv sync --locked
uv run getthefish-gui
```

### Linux / macOS

```bash
git clone <repository-url> GetTheFish
cd GetTheFish
uv sync --locked
uv run getthefish-gui
```

`uv` creates the project environment and installs the pinned Python version and
locked dependencies. To run the application later, use `uv run getthefish-gui`.

Prebuilt Windows executables are attached to each
[GitHub release](../../releases).

## Usage

```bash
getthefish-gui      # GUI (recommended)
getthefish          # headless, uses the saved config
getthefish --help   # options: --config PATH, --verbose
```

In the GUI:

- **Set Area** – drag a rectangle over the water where the bobber lands. Esc or right-click cancels.
- **Pick Color** – click on the bobber in the frozen screenshot; a magnifier next to the cursor
  shows the exact pixel and its value. Esc cancels.
- **Cast Key** – the key the *Fishing* spell is on in your action bar (default `0`).
  Names follow pyautogui: `0`–`9`, `a`–`z`, `f1`–`f12`, `num0`–`num9`, …
- **Threshold Bobber / Threshold Catch** – per-channel RGB tolerance for finding the bobber and for detecting a bite.
- **Jump to Bobber** – keep the cursor on the bobber while waiting; otherwise it returns to where it was after reeling in.
- **Start / Stop** – run the fishing loop in the background.
- **Status LED** – next to the title: Casting, Searching bobber, Waiting for bite, Bite! Reeling
  in, then the result of the round (Caught, Missed, No bobber).
- **Last rounds** – the last 30 rounds as dots: green caught, orange missed, red no bobber.
  Many orange dots usually mean *Threshold Catch* is too high, many red ones that the colour,
  *Threshold Bobber* or the area does not fit.
- **Bite Meter** – live graph of how much the watched pixel changes. The dashed line is
  *Threshold Catch*; click or drag in the graph to move it. Thresholds stay editable while
  fishing so you can tune them live.
- **Statistics** – casts, catches, misses, catch rate, fish per hour and fishing time for the
  *Session* (since the program started, over all Start/Stop runs), *Today* and *Total*.
  Daily numbers are kept in `stats.json` next to `config.json`.
- **Log** – the latest messages; enable *Verbose Log* for every search and bite detail.
- **Compact / Expand** – a small view with Start/Stop, stats and the bite meter, meant to sit
  beside the game in windowed mode. Start switches to it automatically and the previous view
  returns when the session ends. Each view remembers its own window position.
- **Dark / Light** – switches the colour theme (the first start follows the system setting).

Keep this window out of the fishing area: the cast clicks into the area to focus the game, so
a window covering it swallows the click. Start refuses to run while the window overlaps it.

To stop the headless version press **Ctrl+C**. In both modes moving the mouse
into a screen corner triggers the emergency stop.

## Configuration

Settings are saved automatically to a per-user file:

| OS | Location |
| --- | --- |
| Windows | `%APPDATA%\getthefish\config.json` |
| macOS | `~/Library/Application Support/getthefish/config.json` |
| Linux | `$XDG_CONFIG_HOME/getthefish/config.json` (default `~/.config/...`) |

The same folder holds `getthefish.log`, the daily statistics (`stats.json`) and
the window preferences (`window.ini`: theme, view, window positions). The
*Open Config/Logs Folder* button opens it.

Set `GETTHEFISH_CONFIG` or pass `--config` to use another file. A
`config.json` from older versions in the current directory is imported
automatically on first start. See [`config.example.json`](config.example.json).

| Setting | Default | Description |
| --- | --- | --- |
| `bobber_color` | `[72, 41, 12]` | RGB colour of the bobber |
| `threshold_bobber` | `18` | Tolerance (0–255) for finding the bobber |
| `threshold_catch` | `60` | Tolerance (0–255) for detecting a bite |
| `jump_to_bobber` | `true` | Keep the cursor on the bobber while waiting |
| `verbose` | `false` | Log every step |
| `start_pos` | `{"x": 200, "y": 50}` | Top-left corner of the search area (physical pixels) |
| `end_pos` | `{"x": 1100, "y": 400}` | Bottom-right corner of the search area |
| `max_attempts` | `3` | Screenshots taken per cast while looking for the bobber |
| `cast_key` | `"0"` | Key bound to the Fishing spell |

### How a round works

1. **Cast** – left-click on the water (top-left corner of the area) to give the
   game focus, then press `cast_key`. No addon is needed.
2. Wait ~2.5 s, then search the area for the bobber colour.
3. With *Jump to Bobber* the cursor moves onto the bobber (no click).
4. Watch one bobber pixel for up to 20 s. When it changes by more than
   `threshold_catch`, right-click the bobber to reel in.
5. Wait 2 s and cast again. After 3 rounds in a row without a bobber the bot stops.

In the game, enable **Auto Loot** (Interface → Controls) so the catch is looted
by the right-click.

## Troubleshooting

Enable **Verbose Log** in the GUI (or run `getthefish -v`) and check the log file
`getthefish.log` in the same folder as `config.json`. Each cast logs, for example:

```
Bobber found at 640, 212
Watching pixel 643, 217 with colour (74, 40, 13)
No bite within 20s: largest colour change was 41, threshold_catch is 60
```

- **Nothing is cast, then "Bobber not found" three times** – something covers
  the top-left corner of the area, where the cast clicks to focus the game
  (often this window). Move it beside the game; Start checks this for its own
  window.
- **Set the area over water only.** Dark wood (boat), the character and UI
  bars contain the same dark red/brown as the bobber; if they are inside the
  area the bot locks onto them and never sees a bite.
- **`threshold_catch` must be lower than the real change.** On a dark bobber
  colour the pixel changes only ~45–50 when the bobber dips into the water,
  so values of 60+ never fire. Around 30 works for the dark red feather.
- **"Bobber not found"** – the colour or area is off. Pick the colour again on
  the darkest part of the bobber, or raise `threshold_bobber`.
- **"No bite ... largest colour change was X"** although a fish bit – `X` is
  how much the pixel changed. Set `threshold_catch` a bit below that value
  (but above the change you see when nothing happens, to avoid false catches).
- **Cursor never moves (macOS)** – grant *Accessibility* and *Screen Recording*
  permissions to your terminal.

## Project structure

```
src/getthefish/
├── __main__.py        # CLI entry point
├── bot.py             # fishing loop (cast → find → wait → reel in)
├── config.py          # config model, validation, persistence, migration
├── detection.py       # pure numpy colour detection
├── devices.py         # screen capture (mss) and mouse (pyautogui) adapters
├── logs.py            # console + log file setup
├── tally.py           # statistics and the per-day history (stats.json)
└── gui/
    ├── main_window.py # main window, colour picker and area selector
    ├── widgets.py     # status LED, bite meter, round history, log bridge
    ├── theme.py       # light and dark theme
    ├── icon.py        # application icon (also writes the .ico for the exe)
    ├── main.ui        # Qt Designer source
    └── ui_main.py     # generated from main.ui
tests/                 # pytest suite (no real screen or mouse needed)
```

## Development

Run the same checks as CI:

```bash
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy
uv run --locked pytest
```

CI runs them on Windows for every push and pull request. Pushing a tag like
`v1.2.0` builds `getthefish-gui.exe` and attaches it to a GitHub release.

`uv.lock` is the committed, cross-platform dependency lockfile.

After editing `main.ui` in Qt Designer, regenerate the Python code:

```bash
uv run pyside6-uic src/getthefish/gui/main.ui -o src/getthefish/gui/ui_main.py
```

## License

MIT – see [LICENSE](LICENSE).

# Get The Fish

An automated fishing tool written in Python. It automates the fishing process: it casts a line, searches for the bobber using color detection, detects when a fish bites, and automatically reels it in.

The project consists of:
- **`getthefish.py`** — core tool logic: cast, find bobber by color, wait for a bite, and catch the fish.
- **`ui.py`** — PyQt5 graphical user interface (built from `main.ui` via `ui_main.py`) for configuring the tool.
- **`colorcompare.py`** — color-difference utility using `numpy` and `scikit-image` (CIE76 delta-E).

## Features

- Automatic fishing loop (cast → bobber detection → bite detection → catch)
- Color-based bobber detection (default bobber color: `(72, 41, 12)`, threshold: `18`)
- Customizable fishing area, thresholds, and logging
- GUI to pick the bobber color and set the fishing area

## Prerequisites

- Python 3.x
- A Windows-based display (screen capture and mouse automation are used)

## Project Structure

```
GetTheFish/
├── getthefish.py    # Core fishing tool logic
├── ui.py            # PyQt5 GUI wrapper
├── ui_main.py       # Auto-generated UI from main.ui
├── main.ui          # Qt Designer UI file
├── colorcompare.py  # Color comparison utility
├── config.json      # tool configuration
├── test.png         # Sample screenshot (bobber snapshot)
└── README.md        # This file
```

## Running with a Virtual Environment (Windows)

### 1. Open Command Prompt

- Press `Win + R`, type `cmd`, and press **Enter**.
- Navigate to the project directory:

```cmd
cd C:\path\to\GetTheFish
```

### 2. Create a Virtual Environment

```cmd
python -m venv venv
```

### 3. Activate the Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` appear in your prompt.

### 4. Install Dependencies

```cmd
pip install pyscreenshot pyautogui jsonpickle PyQt5 numpy scikit-image
```

### 5. Run the Tool

Start the GUI (recommended, for configuration):

```cmd
python ui.py
```

Or run the core tool directly:

```cmd
python getthefish.py
```

### 6. Deactivate the Virtual Environment

When finished:

```cmd
deactivate
```

## Running Without a Virtual Environment

If you prefer not to use a virtual environment, install the dependencies globally:

```cmd
pip install pyscreenshot pyautogui jsonpickle PyQt5 numpy scikit-image
python ui.py
```

## Configuration

All settings are saved in `config.json` (auto-created on first run):

| Setting | Default | Description |
| --- | --- | --- |
| `bobbercolor` | `[72, 41, 12]` | RGB color of the bobber |
| `thresholdBobber` | `18` | Color tolerance for bobber detection |
| `thresholdCatch` | `60` | Color tolerance for bite detection |
| `jumpToBobber` | `true` | Move the cursor directly to the bobber |
| `verbose` | `false` | Enable detailed logging |
| `startPos` | `(200, 50)` | Top-left corner of the fishing area |
| `endPos` | `(1100, 400)` | Bottom-right corner of the fishing area |

Use the GUI (in `ui.py`) to adjust the bobber color and fishing area interactively:

- **Set Area** — left-click to start and drag to define the fishing area; right-click to finish.
- **Select Color** — click on the bobber in the screenshot to pick its color.
- **Threshold Bobber / Threshold Catch** — adjust detection sensitivity.
- **Start** — toggle the fishing loop on/off.

## Notes

- The script uses screen capture and mouse control, so run it only on a trusted/authorized game session.
- Adjust the bobber color and thresholds in the GUI to match your game's colors for optimal performance.

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file included in the repository.
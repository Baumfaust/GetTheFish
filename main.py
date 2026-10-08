#!/usr/bin/env python
"""Get The Fish - Main entry point for the fishing automation tool.

This script provides a clean entry point for running the fishing bot.
It handles command-line arguments for different modes of operation.
"""

import sys
from pathlib import Path

# Add the current directory to Python path to ensure imports work correctly
sys.path.insert(0, str(Path(__file__).parent))

from getthefish import GetTheFish, FishConfig


def main():
    """Main function to run the fishing bot."""
    print("Get The Fish - Automated Fishing Tool")
    print("=" * 50)

    # Check if a config file exists, and if not, create one with defaults
    if not Path("config.json").exists():
        print("No config file found. Creating default config...")
        config = FishConfig()
        config.save()

    # Initialize and run the fishing bot
    try:
        fish = GetTheFish()
        print("Starting fishing bot... Press Ctrl+C to stop.")
        fish.fishing()
    except KeyboardInterrupt:
        print("\nFishing stopped by user.")
        if 'fish' in locals():
            fish.stop()
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
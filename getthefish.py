"""Get The Fish - Automated fishing tool for the browser game Get The Fish."""
import time
import random
import json
import logging
from pathlib import Path
from typing import Optional, Tuple

import mss
import numpy as np
import pyautogui

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Point:
    """Simple 2D point class."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class FishConfig:
    """Configuration for the fishing tool."""

    CONFIG_FILE = Path("config.json")

    def __init__(
        self,
        jumpToBobber: bool = True,
        verbose: bool = False,
        thresholdBobber: int = 18,
        thresholdCatch: int = 60,
        bobbercolor: Tuple[int, int, int] = (72, 41, 12),
        startPos: Optional[Point] = None,
        endPos: Optional[Point] = None,
        max_attempts: int = 50,
    ):
        self.jumpToBobber = jumpToBobber
        self.verbose = verbose
        self.thresholdBobber = thresholdBobber
        self.thresholdCatch = thresholdCatch
        self.bobbercolor = bobbercolor
        self.startPos = startPos or Point(200, 50)
        self.endPos = endPos or Point(1100, 400)
        self.max_attempts = max_attempts

    def to_dict(self) -> dict:
        """Convert config to dictionary for JSON serialization."""
        return {
            "jumpToBobber": self.jumpToBobber,
            "verbose": self.verbose,
            "thresholdBobber": self.thresholdBobber,
            "thresholdCatch": self.thresholdCatch,
            "bobbercolor": list(self.bobbercolor),
            "startPos": {"x": self.startPos.x, "y": self.startPos.y},
            "endPos": {"x": self.endPos.x, "y": self.endPos.y},
            "max_attempts": self.max_attempts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FishConfig":
        """Create FishConfig from dictionary."""
        start_pos = Point(data["startPos"]["x"], data["startPos"]["y"])
        end_pos = Point(data["endPos"]["x"], data["endPos"]["y"])
        return cls(
            jumpToBobber=data.get("jumpToBobber", True),
            verbose=data.get("verbose", False),
            thresholdBobber=data.get("thresholdBobber", 18),
            thresholdCatch=data.get("thresholdCatch", 60),
            bobbercolor=tuple(data.get("bobbercolor", (72, 41, 12))),
            startPos=start_pos,
            endPos=end_pos,
            max_attempts=data.get("max_attempts", 50),
        )

    def save(self, path: Optional[Path] = None) -> None:
        """Save config to JSON file."""
        path = path or self.CONFIG_FILE
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
        logger.debug(f"Config saved to {path}")

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "FishConfig":
        """Load config from JSON file."""
        path = path or cls.CONFIG_FILE
        if not path.exists():
            logger.info(f"No config file found at {path}, using defaults")
            return cls()

        try:
            with open(path, 'r') as f:
                data = json.load(f)
            logger.info(f"Config loaded from {path}")
            return cls.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to load config from {path}: {e}. Using defaults.")
            return cls()


def check_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], delta: int) -> bool:
    """Check if two RGB colors are within delta of each other."""
    return all(
        color2[i] - delta <= color1[i] <= color2[i] + delta
        for i in range(3)
    )


class GetTheFish:
    """Main fishing automation class."""

    def __init__(self, config: Optional[FishConfig] = None):
        # Re-enable failsafe for safety (Ctrl+Alt+Del or move mouse to corner)
        pyautogui.FAILSAFE = True

        self.run = True
        self.gui = False
        self.fishConfig = config or FishConfig()
        self.sct = mss.mss()

        logger.info("GetTheFish initialized")
        logger.debug(f"Config: {self.fishConfig.__dict__}")

        self.fishConfig.save()

    def log(self, text: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.fishConfig.verbose:
            logger.info(text)

    def stop(self) -> None:
        """Stop the fishing loop."""
        self.run = False
        logger.info("Stop signal received")

    def grab_screen(self, bbox: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """Capture screen region using mss."""
        if bbox:
            monitor = {"left": bbox[0], "top": bbox[1], "width": bbox[2] - bbox[0], "height": bbox[3] - bbox[1]}
        else:
            monitor = self.sct.monitors[1]  # Primary monitor
        screenshot = self.sct.grab(monitor)
        return np.array(screenshot)[:, :, :3]  # Drop alpha channel

    def find_bobber(self, max_attempts: int = 3) -> Optional[Point]:
        """
        Find the bobber using vectorized numpy color comparison.
        """
        x1, y1 = self.fishConfig.startPos.x, self.fishConfig.startPos.y
        x2, y2 = self.fishConfig.endPos.x, self.fishConfig.endPos.y
        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            logger.error("Invalid search area: width and height must be positive")
            return None

        bobber_color = np.array(self.fishConfig.bobbercolor, dtype=np.uint8)
        threshold = self.fishConfig.thresholdBobber

        for attempt in range(max_attempts):
            self.log(f"Searching for bobber (attempt {attempt + 1}/{max_attempts})")

            try:
                image = self.grab_screen(bbox=(x1, y1, x2, y2))
                image_rgb = image[:, :, ::-1]  # Convert BGR to RGB

                # Vectorized color difference calculation
                diff = np.abs(image_rgb.astype(np.int16) - bobber_color.astype(np.int16))
                match_mask = np.all(diff <= threshold, axis=2)

                matches = np.argwhere(match_mask)
                if len(matches) > 0:
                    y, x = matches[0]  # First match
                    screen_x = x1 + x
                    screen_y = y1 + y
                    self.log(f"Bobber found at position: {screen_x}, {screen_y}")
                    return Point(screen_x, screen_y)

            except Exception as e:
                logger.warning(f"Error during bobber search (attempt {attempt + 1}): {e}")

            if attempt < max_attempts - 1:
                wait_time = random.uniform(0.5, 1.5)
                time.sleep(wait_time)

        self.log("Bobber not found after all attempts")
        return None

    def wait_for_fish(self, bobber_pos: Point, timeout: float = 20.0) -> bool:
        """Wait for fish to bite by detecting color change at bobber position."""
        start_time = time.time()
        old_x, old_y = pyautogui.position()

        try:
            image = self.grab_screen(bbox=(bobber_pos.x, bobber_pos.y, bobber_pos.x + 1, bobber_pos.y + 1))
            initial_color = image[0, 0, ::-1]  # BGR to RGB
        except Exception as e:
            logger.error(f"Failed to capture initial bobber color: {e}")
            return False

        self.log("Waiting for fish...")

        while (time.time() - start_time) < timeout and self.run:
            try:
                image = self.grab_screen(bbox=(bobber_pos.x, bobber_pos.y, bobber_pos.x + 1, bobber_pos.y + 1))
                current_color = image[0, 0, ::-1]

                if not check_color(current_color, initial_color, self.fishConfig.thresholdCatch):
                    self.log("Fish detected! Catching...")
                    time.sleep(random.uniform(0.2, 0.9))
                    pyautogui.moveTo(old_x, old_y)
                    pyautogui.moveTo(bobber_pos.x, bobber_pos.y)
                    pyautogui.click(button='right')
                    pyautogui.moveTo(old_x, old_y)
                    return True
            except Exception as e:
                logger.warning(f"Error during fish detection: {e}")

            time.sleep(0.1)

        self.log("Fish timeout - no bite detected")
        return False

    def fishing(self) -> None:
        """Main fishing loop with error handling and retry logic."""
        logger.info("Starting fishing loop")
        max_consecutive_failures = 3
        consecutive_failures = 0

        while self.run:
            try:
                self.fishConfig.save()
                pyautogui.moveTo(self.fishConfig.startPos.x, self.fishConfig.startPos.y)
                pyautogui.click(button='right')
                pyautogui.click(button='right')

                wait_time = random.uniform(2.1, 2.9)
                self.log(f"Start fishing in {wait_time:.1f} seconds")
                time.sleep(wait_time)

                bobber_pos = self.find_bobber(max_attempts=self.fishConfig.max_attempts)

                if bobber_pos is None:
                    consecutive_failures += 1
                    logger.warning(f"Failed to find bobber (consecutive failures: {consecutive_failures})")
                    if consecutive_failures >= max_consecutive_failures:
                        logger.error("Too many consecutive failures, stopping")
                        break
                    time.sleep(random.uniform(3, 5))
                    continue

                consecutive_failures = 0
                bobber_pos.x += 3
                bobber_pos.y += 5
                pyautogui.moveTo(bobber_pos.x, bobber_pos.y)
                self.log("Wait for Fish")

                caught = self.wait_for_fish(bobber_pos)
                if caught:
                    self.log("Fish caught!")
                else:
                    self.log("Fish gone or timeout!")

                time.sleep(2)

            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                break
            except pyautogui.FailSafeException:
                logger.info("Fail-safe triggered (mouse moved to corner)")
                break
            except Exception as e:
                logger.error(f"Unexpected error in fishing loop: {e}")
                consecutive_failures += 1
                if consecutive_failures >= max_consecutive_failures:
                    logger.error("Too many errors, stopping")
                    break
                time.sleep(random.uniform(3, 5))

        logger.info("Stopped fishing")


if __name__ == '__main__':
    fish = GetTheFish()
    try:
        fish.fishing()
    except KeyboardInterrupt:
        fish.stop()
        logger.info("Shutting down...")

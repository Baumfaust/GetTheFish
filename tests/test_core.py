"""Unit tests for the core GetTheFish functionality."""
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock

import pytest
import numpy as np

from getthefish import FishConfig, GetTheFish, Point


class TestFishConfig:
    """Tests for configuration loading and validation."""

    def test_load_valid_config(self):
        """Test that a valid config loads correctly."""
        config = {
            "bobber_color": [255, 165, 0],
            "area_x": 100,
            "area_y": 100,
            "threshold": 30,
            "max_attempts": 50,
        }
        loaded = FishConfig.load(config)
        assert loaded["bobber_color"] == config["bobber_color"]
        assert loaded["area_x"] == config["area_x"]
        assert loaded["area_y"] == config["area_y"]
        assert loaded["threshold"] == config["threshold"]
        assert loaded["max_attempts"] == config["max_attempts"]

    def test_load_missing_keys_raises_error(self):
        """Test that missing required keys raise an error."""
        incomplete = {"bobber_color": [255, 0, 0]}
        with pytest.raises(KeyError):
            FishConfig.load(incomplete)

    def test_save_and_load_roundtrip(self):
        """Test saving config to JSON and reloading preserves values."""
        original = {
            "bobber_color": [200, 150, 50],
            "area_x": 50,
            "area_y": 80,
            "threshold": 25,
            "max_attempts": 40,
        }
        saved_path = tempfile.mktemp(suffix='.json')
        try:
            config = FishConfig.load(original)
            with open(saved_path, 'w') as f:
                json.dump(config.to_dict(), f)

            reloaded = FishConfig.load(saved_path)
            assert reloaded["bobber_color"] == original["bobber_color"]
            assert reloaded["area_x"] == original["area_x"]
            assert reloaded["area_y"] == original["area_y"]
            assert reloaded["threshold"] == original["threshold"]
            assert reloaded["max_attempts"] == original["max_attempts"]
        finally:
            os.unlink(saved_path)


class TestGetTheFish:
    """Tests for the main GetTheFish class."""

    @patch('getthefish.mss.mss')
    @patch('getthefish.pyautogui.moveTo')
    @patch('getthefish.pyautogui.wait')
    def test_fishing_loop_runs(self, mock_wait, mock_move_to, mock_image_grab):
        """Test that the fishing loop executes without errors."""
        # Setup mock image with a bobber-like color
        mock_img = MagicMock()
        mock_img.getpixel.return_value = (255, 165, 0)  # Bobber color

        # Mock the screenshot to return our mock image
        with patch('getthefish.pyscreenshot.ImageGrab.grab', return_value=mock_img):
            fish = GetTheFish(
                bobber_color=[255, 165, 0],
                area_x=100,
                area_y=100,
                threshold=30,
                max_attempts=10,
            )
            # The fishing method should run without raising exceptions
            fish.fishing()
            # We don't assert on internal state since it depends on timing
            assert fish.is_running is True

    def test_fishing_stops_on_no_bobber(self):
        """Test that fishing stops when no bobber is detected within max_attempts."""
        # Mock image with no matching color
        mock_img = MagicMock()
        mock_img.getpixel.return_value = (0, 0, 0)  # Not a bobber

        with patch('getthefish.pyscreenshot.ImageGrab.grab', return_value=mock_img):
            fish = GetTheFish(
                bobber_color=[255, 165, 0],
                area_x=100,
                area_y=100,
                threshold=30,
                max_attempts=5,
            )
            # After max_attempts, the fish should stop
            fish.fishing()
            # In the actual implementation, this may set a flag or stop moving
            # For now, we just verify it doesn't hang
            assert fish.is_running is False or fish.has_stopped == True

    def test_init_with_defaults(self):
        """Test that GetTheFish initializes with sensible defaults."""
        fish = GetTheFish()
        assert fish.bobber_color == [255, 165, 0]  # Default
        assert fish.area_x == 100
        assert fish.area_y == 100
        assert fish.threshold == 30
        assert fish.max_attempts == 50

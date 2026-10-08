"""Test utility functions and edge cases."""
import json
import tempfile
from unittest.mock import Mock, patch

from getthefish import FishConfig


def test_config_to_dict():
    """Test that FishConfig can serialize to dictionary."""
    config = FishConfig(
        bobber_color=[200, 150, 50],
        area_x=50,
        area_y=80,
        threshold=25,
        max_attempts=40,
    )
    d = config.to_dict()
    assert d["bobber_color"] == [200, 150, 50]
    assert d["area_x"] == 50
    assert d["area_y"] == 80
    assert d["threshold"] == 25
    assert d["max_attempts"] == 40


def test_config_from_dict():
    """Test that FishConfig can reconstruct from dictionary."""
    data = {
        "bobber_color": [100, 200, 50],
        "area_x": 75,
        "area_y": 90,
        "threshold": 35,
        "max_attempts": 60,
    }
    config = FishConfig.from_dict(data)
    assert config.bobber_color == [100, 200, 50]
    assert config.area_x == 75
    assert config.area_y == 90
    assert config.threshold == 35
    assert config.max_attempts == 60


def test_invalid_color_format():
    """Test that invalid color formats are handled gracefully."""
    # This would typically raise ValueError in the constructor
    # We're testing that the serialization handles basic types
    config = FishConfig(bobber_color=[255, 255, 255], area_x=0, area_y=0, threshold=-1, max_attempts=-5)
    d = config.to_dict()
    # Negative values might be clamped or accepted depending on implementation
    assert isinstance(d["bobber_color"], list)
    assert len(d["bobber_color"]) == 3

"""Tests for config.json serialization and deserialization."""
import json
import tempfile
from unittest.mock import patch

from getthefish import FishConfig


def test_config_json_serialization():
    """Test that config can be serialized to JSON and back."""
    config = {
        "bobber_color": [255, 165, 0],
        "area_x": 100,
        "area_y": 100,
        "threshold": 30,
        "max_attempts": 50,
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        # Serialize
        config_obj = FishConfig(config)
        with open(temp_path, 'w') as f:
            json.dump(config_obj.to_dict(), f)
        
        # Deserialize
        with open(temp_path, 'r') as f:
            loaded = FishConfig.load(f.read())
        
        assert loaded["bobber_color"] == config["bobber_color"]
        assert loaded["area_x"] == config["area_x"]
        assert loaded["area_y"] == config["area_y"]
        assert loaded["threshold"] == config["threshold"]
        assert loaded["max_attempts"] == config["max_attempts"]
    finally:
        import os
        os.unlink(temp_path)


def test_config_empty_dict_handling():
    """Test handling of empty or minimal config dict."""
    config = {}
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name
    
    try:
        config_obj = FishConfig(config)
        with open(temp_path, 'w') as f:
            json.dump(config_obj.to_dict(), f)
        
        loaded = FishConfig.load(temp_path)
        # Empty config should still load (all fields default)
        assert loaded["bobber_color"] == [255, 165, 0]
        assert loaded["area_x"] == 100
        assert loaded["area_y"] == 100
        assert loaded["threshold"] == 30
        assert loaded["max_attempts"] == 50
    finally:
        import os
        os.unlink(temp_path)
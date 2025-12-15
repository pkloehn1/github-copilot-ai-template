"""Tests for config loading functionality."""

import tempfile
from pathlib import Path

import pytest


def test_load_config_returns_dict():
    """load_config should return a dictionary."""
    from scripts.context_validator.config import load_config

    # Use the actual config file
    config_path = Path(__file__).parent.parent / "scripts" / "copilot-context-health.conf"
    result = load_config(config_path)

    assert isinstance(result, dict)


def test_load_config_parses_required_keys():
    """load_config should parse all required keys from config."""
    from scripts.context_validator.config import load_config

    config_path = Path(__file__).parent.parent / "scripts" / "copilot-context-health.conf"
    result = load_config(config_path)

    # Verify required keys exist and are positive integers
    # Note: LLM provider limits are now in LLM_PROVIDERS dict, not config file
    required_keys = [
        "CHARS_PER_TOKEN",
        "INFO_THRESHOLD_PERCENT",
        "WARN_THRESHOLD_PERCENT",
    ]
    for key in required_keys:
        assert key in result, f"Missing required key: {key}"
        assert isinstance(result[key], int), f"{key} should be an integer"
        assert result[key] > 0, f"{key} should be positive"


def test_load_config_ignores_comments():
    """load_config should ignore lines starting with #."""
    from scripts.context_validator.config import load_config

    with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
        f.write("# This is a comment\n")
        f.write("KEY=100\n")
        f.write("  # Indented comment\n")
        f.flush()
        config_path = Path(f.name)

    result = load_config(config_path)
    assert result == {"KEY": 100}


def test_load_config_ignores_empty_lines():
    """load_config should ignore empty lines."""
    from scripts.context_validator.config import load_config

    with tempfile.NamedTemporaryFile(mode="w", suffix=".conf", delete=False) as f:
        f.write("KEY1=100\n")
        f.write("\n")
        f.write("KEY2=200\n")
        f.flush()
        config_path = Path(f.name)

    result = load_config(config_path)
    assert result == {"KEY1": 100, "KEY2": 200}


def test_load_config_missing_file_exits():
    """load_config should exit with error if file not found."""
    from scripts.context_validator.config import load_config

    with pytest.raises(SystemExit):
        load_config(Path("/nonexistent/path/config.conf"))

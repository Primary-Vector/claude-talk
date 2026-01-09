"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def tmp_config_dir():
    """Create a temporary config directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config(tmp_config_dir):
    """Create a mock config file."""
    config_path = tmp_config_dir / "config.toml"
    config_path.write_text('''enabled = true
voice = "v2/en_speaker_6"
model_size = "small"
max_chars = 500
''')
    return config_path

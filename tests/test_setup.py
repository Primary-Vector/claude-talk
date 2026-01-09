import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from claude_talk.setup import install_hook, run_setup


def test_install_hook_creates_settings_file(tmp_path):
    settings_path = tmp_path / "settings.json"

    install_hook(settings_path)

    assert settings_path.exists()
    settings = json.loads(settings_path.read_text())
    assert "hooks" in settings
    assert "AssistantResponse" in settings["hooks"]


def test_install_hook_preserves_existing_settings(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text('{"existingKey": "value"}')

    install_hook(settings_path)

    settings = json.loads(settings_path.read_text())
    assert settings["existingKey"] == "value"
    assert "hooks" in settings


def test_install_hook_preserves_existing_hooks(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text('{"hooks": {"Stop": [{"type": "command", "command": "other"}]}}')

    install_hook(settings_path)

    settings = json.loads(settings_path.read_text())
    assert "Stop" in settings["hooks"]
    assert "AssistantResponse" in settings["hooks"]

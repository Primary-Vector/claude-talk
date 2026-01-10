import tempfile
from pathlib import Path

from claude_talk.config import Config, load_config, save_config


def test_default_config():
    config = Config()
    assert config.enabled is True
    assert config.voice == "af_heart"
    assert config.max_chars == 500


def test_save_and_load_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.toml"

        config = Config(enabled=False, voice="af_bella", max_chars=1000)
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert loaded.enabled is False
        assert loaded.voice == "af_bella"
        assert loaded.max_chars == 1000


def test_load_missing_config_returns_default():
    config = load_config(Path("/nonexistent/path/config.toml"))
    assert config.enabled is True

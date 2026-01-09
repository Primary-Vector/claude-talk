import tempfile
from pathlib import Path

from claude_talk.config import Config, load_config, save_config


def test_default_config():
    config = Config()
    assert config.enabled is True
    assert config.voice == "v2/en_speaker_6"
    assert config.model_size == "small"
    assert config.max_chars == 500


def test_save_and_load_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.toml"

        config = Config(enabled=False, voice="v2/en_speaker_3", model_size="large", max_chars=1000)
        save_config(config, config_path)

        loaded = load_config(config_path)
        assert loaded.enabled is False
        assert loaded.voice == "v2/en_speaker_3"
        assert loaded.model_size == "large"
        assert loaded.max_chars == 1000


def test_load_missing_config_returns_default():
    config = load_config(Path("/nonexistent/path/config.toml"))
    assert config.enabled is True

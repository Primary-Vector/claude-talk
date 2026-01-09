"""Integration tests for Claude Talk."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

from claude_talk.cli import main
from claude_talk.config import save_config, Config


def test_full_speak_flow(tmp_path):
    """Test the full flow from stdin to TTS."""
    config_path = tmp_path / "config.toml"
    config = Config(enabled=True, voice="v2/en_speaker_6", model_size="small", max_chars=500)
    save_config(config, config_path)

    input_text = """Here's my response!

```python
def example():
    pass
```

Hope that helps!"""

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.BarkTTS") as mock_tts_class:
            mock_tts = MagicMock()
            mock_tts_class.return_value = mock_tts

            with patch("sys.stdin", StringIO(input_text)):
                with patch("sys.argv", ["claude-talk", "speak"]):
                    main()

            mock_tts.speak.assert_called_once()
            spoken_text = mock_tts.speak.call_args[0][0]

            # Should include conversational parts
            assert "response" in spoken_text or "Hope" in spoken_text
            # Should not include code
            assert "def example" not in spoken_text


def test_disabled_skips_tts(tmp_path):
    """Test that disabled config skips TTS entirely."""
    config_path = tmp_path / "config.toml"
    config = Config(enabled=False, voice="v2/en_speaker_6", model_size="small", max_chars=500)
    save_config(config, config_path)

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.BarkTTS") as mock_tts_class:
            with patch("sys.stdin", StringIO("Hello world")):
                with patch("sys.argv", ["claude-talk", "speak"]):
                    main()

            mock_tts_class.assert_not_called()

"""Integration tests for Claude Talk."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

from claude_talk.cli import main, speak_command
from claude_talk.config import save_config, Config


def test_full_speak_flow(tmp_path):
    """Test the full flow from hook input to TTS."""
    config_path = tmp_path / "config.toml"
    config = Config(enabled=True, voice="af_heart", max_chars=500)
    save_config(config, config_path)

    # Create a transcript with conversational text and code
    transcript_path = tmp_path / "transcript.jsonl"
    transcript_path.write_text(
        json.dumps({"type": "user", "message": {"content": "Help me"}}) + "\n" +
        json.dumps({
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": "Here's my response!\n\n```python\ndef example():\n    pass\n```\n\nHope that helps!"}]}
        })
    )

    hook_input = json.dumps({
        "hook_event_name": "Stop",
        "session_id": "test123",
        "transcript_path": str(transcript_path)
    })

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.speak_async") as mock_speak:
            with patch("claude_talk.cli.get_spoken_hash", return_value=None):
                with patch("claude_talk.cli.set_spoken_hash"):
                    with patch("sys.stdin", StringIO(hook_input)):
                        speak_command()

            mock_speak.assert_called_once()
            spoken_text = mock_speak.call_args[0][0]

            # Should include conversational parts
            assert "response" in spoken_text or "Hope" in spoken_text
            # Should not include code
            assert "def example" not in spoken_text


def test_disabled_skips_tts(tmp_path):
    """Test that disabled config skips TTS entirely."""
    config_path = tmp_path / "config.toml"
    config = Config(enabled=False, voice="af_heart", max_chars=500)
    save_config(config, config_path)

    transcript_path = tmp_path / "transcript.jsonl"
    transcript_path.write_text(
        json.dumps({"type": "user", "message": {"content": "Hi"}}) + "\n" +
        json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "Hello!"}]}})
    )

    hook_input = json.dumps({
        "hook_event_name": "Stop",
        "session_id": "test",
        "transcript_path": str(transcript_path)
    })

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.speak_async") as mock_speak:
            with patch("sys.stdin", StringIO(hook_input)):
                speak_command()

            mock_speak.assert_not_called()

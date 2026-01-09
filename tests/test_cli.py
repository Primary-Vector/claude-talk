import sys
import tempfile
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock

from claude_talk.cli import speak_command, main


def test_speak_command_exits_if_disabled(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('enabled = false\nvoice = "v2/en_speaker_6"\nmodel_size = "small"\nmax_chars = 500')

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.BarkTTS") as mock_tts:
            speak_command("Hello world")
            mock_tts.assert_not_called()


def test_speak_command_filters_and_speaks(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('enabled = true\nvoice = "v2/en_speaker_6"\nmodel_size = "small"\nmax_chars = 500')

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.BarkTTS") as mock_tts_class:
            mock_tts = MagicMock()
            mock_tts_class.return_value = mock_tts

            speak_command("Hello! ```python\ncode\n``` How are you?")

            mock_tts.speak.assert_called_once()
            call_args = mock_tts.speak.call_args[0][0]
            assert "code" not in call_args
            assert "Hello" in call_args


def test_speak_command_skips_empty_after_filter(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('enabled = true\nvoice = "v2/en_speaker_6"\nmodel_size = "small"\nmax_chars = 500')

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.BarkTTS") as mock_tts:
            speak_command("```python\nprint('hello')\n```")
            mock_tts.assert_not_called()


def test_main_speak_reads_stdin():
    with patch("claude_talk.cli.speak_command") as mock_speak:
        with patch("sys.stdin", StringIO("Hello from stdin")):
            with patch("sys.argv", ["claude-talk", "speak"]):
                main()
                mock_speak.assert_called_once_with("Hello from stdin")

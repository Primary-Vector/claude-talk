import sys
import json
import tempfile
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock

from claude_talk.cli import speak_command, main, get_assistant_text_from_transcript


def test_speak_command_exits_if_disabled(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('enabled = false\nvoice = "af_heart"\nmax_chars = 500')

    hook_input = json.dumps({
        "hook_event_name": "Stop",
        "session_id": "test",
        "transcript_path": "/nonexistent/path.jsonl"
    })

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.speak_async") as mock_speak:
            with patch("sys.stdin", StringIO(hook_input)):
                speak_command()
                mock_speak.assert_not_called()


def test_speak_command_calls_speak_async(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('enabled = true\nvoice = "af_heart"\nmax_chars = 500')

    # Create a mock transcript
    transcript_path = tmp_path / "transcript.jsonl"
    transcript_path.write_text(json.dumps({
        "type": "user",
        "message": {"content": "Hello"}
    }) + "\n" + json.dumps({
        "type": "assistant",
        "message": {"content": [{"type": "text", "text": "Hi there!"}]}
    }))

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


def test_speak_command_skips_empty_after_filter(tmp_path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('enabled = true\nvoice = "af_heart"\nmax_chars = 500')

    # Create a transcript with only code (should be filtered out)
    transcript_path = tmp_path / "transcript.jsonl"
    transcript_path.write_text(json.dumps({
        "type": "user",
        "message": {"content": "Hello"}
    }) + "\n" + json.dumps({
        "type": "assistant",
        "message": {"content": [{"type": "text", "text": "```python\nprint('hello')\n```"}]}
    }))

    hook_input = json.dumps({
        "hook_event_name": "Stop",
        "session_id": "test123",
        "transcript_path": str(transcript_path)
    })

    with patch("claude_talk.cli.DEFAULT_CONFIG_PATH", config_path):
        with patch("claude_talk.cli.speak_async") as mock_speak:
            with patch("claude_talk.cli.get_spoken_hash", return_value=None):
                with patch("sys.stdin", StringIO(hook_input)):
                    speak_command()
                    mock_speak.assert_not_called()


def test_main_speak_reads_stdin():
    hook_input = json.dumps({
        "hook_event_name": "Stop",
        "session_id": "test",
        "transcript_path": "/some/path.jsonl"
    })

    with patch("claude_talk.cli.speak_command") as mock_speak:
        with patch("sys.stdin", StringIO(hook_input)):
            with patch("sys.argv", ["claude-talk", "speak"]):
                main()
                mock_speak.assert_called_once()


def test_get_assistant_text_from_transcript(tmp_path):
    transcript_path = tmp_path / "transcript.jsonl"
    transcript_path.write_text(
        json.dumps({"type": "user", "message": {"content": "Hi"}}) + "\n" +
        json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "Hello!"}]}}) + "\n" +
        json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "How can I help?"}]}})
    )

    result = get_assistant_text_from_transcript(str(transcript_path))
    assert "Hello!" in result
    assert "How can I help?" in result

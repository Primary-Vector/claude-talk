# Claude Talk TTS Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Claude Code plugin that speaks assistant responses aloud using Bark TTS.

**Architecture:** Hook-based TTS triggered by `AssistantResponse` hook. Text is filtered (remove code/tables), truncated, then spoken via Bark. Configuration stored in TOML. Slash commands for setup/enable/disable/voice.

**Tech Stack:** Python 3.11+, Bark TTS (`git+https://github.com/suno-ai/bark.git`), scipy, tomli/tomllib, uv for packaging

---

## Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `src/claude_talk/__init__.py`

**Step 1: Create pyproject.toml**

```toml
[project]
name = "claude-talk"
version = "0.1.0"
description = "TTS plugin for Claude Code using Bark"
requires-python = ">=3.11"
dependencies = [
    "bark @ git+https://github.com/suno-ai/bark.git",
    "scipy>=1.11.0",
    "sounddevice>=0.4.6",
]

[project.scripts]
claude-talk = "claude_talk.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/claude_talk"]
```

**Step 2: Create package init**

```python
"""Claude Talk - TTS plugin for Claude Code using Bark."""

__version__ = "0.1.0"
```

**Step 3: Commit**

```bash
git add pyproject.toml src/claude_talk/__init__.py
git commit -m "feat: add project scaffolding"
```

---

## Task 2: Configuration Module

**Files:**
- Create: `src/claude_talk/config.py`
- Test: `tests/test_config.py`

**Step 1: Write the failing test**

```python
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
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_config.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'claude_talk.config'"

**Step 3: Write implementation**

```python
"""Configuration management for Claude Talk."""

from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "claude-talk" / "config.toml"


@dataclass
class Config:
    """Claude Talk configuration."""

    enabled: bool = True
    voice: str = "v2/en_speaker_6"
    model_size: str = "small"
    max_chars: int = 500


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Config:
    """Load config from TOML file, returning defaults if not found."""
    if not path.exists():
        return Config()

    with open(path, "rb") as f:
        data = tomllib.load(f)

    return Config(
        enabled=data.get("enabled", True),
        voice=data.get("voice", "v2/en_speaker_6"),
        model_size=data.get("model_size", "small"),
        max_chars=data.get("max_chars", 500),
    )


def save_config(config: Config, path: Path = DEFAULT_CONFIG_PATH) -> None:
    """Save config to TOML file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    content = f'''enabled = {str(config.enabled).lower()}
voice = "{config.voice}"
model_size = "{config.model_size}"
max_chars = {config.max_chars}
'''
    path.write_text(content)
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_config.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/claude_talk/config.py tests/test_config.py
git commit -m "feat: add configuration module"
```

---

## Task 3: Text Filtering Module

**Files:**
- Create: `src/claude_talk/filter.py`
- Test: `tests/test_filter.py`

**Step 1: Write the failing test**

```python
from claude_talk.filter import filter_text


def test_removes_fenced_code_blocks():
    text = """Here's the code:

```python
def hello():
    print("world")
```

That should work."""
    result = filter_text(text)
    assert "def hello" not in result
    assert "Here's the code:" in result
    assert "That should work." in result


def test_removes_inline_code():
    text = "Use the `print()` function to output text."
    result = filter_text(text)
    assert "`print()`" not in result
    assert "print()" not in result
    assert "Use the" in result


def test_removes_markdown_tables():
    text = """Here's a table:

| Name | Age |
|------|-----|
| Bob  | 30  |

And some more text."""
    result = filter_text(text)
    assert "| Name |" not in result
    assert "Here's a table:" in result
    assert "And some more text." in result


def test_removes_file_paths():
    text = "Check the file at /Users/pv/git/project/src/main.py for details."
    result = filter_text(text)
    assert "/Users/pv/git" not in result


def test_removes_urls():
    text = "Visit https://example.com/page for more info."
    result = filter_text(text)
    assert "https://example.com" not in result


def test_truncates_to_max_chars():
    text = "Hello world. " * 100  # ~1300 chars
    result = filter_text(text, max_chars=100)
    assert len(result) <= 100


def test_preserves_conversational_text():
    text = "I'd be happy to help you with that! Let me explain how it works."
    result = filter_text(text)
    assert result.strip() == text


def test_empty_after_filtering_returns_empty():
    text = "```python\nprint('hello')\n```"
    result = filter_text(text)
    assert result.strip() == ""
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_filter.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'claude_talk.filter'"

**Step 3: Write implementation**

```python
"""Text filtering for Claude Talk - removes code, tables, and other non-conversational content."""

import re


def filter_text(text: str, max_chars: int = 500) -> str:
    """Filter out non-conversational content and truncate."""
    result = text

    # Remove fenced code blocks (``` ... ```)
    result = re.sub(r"```[\s\S]*?```", "", result)

    # Remove inline code (`...`)
    result = re.sub(r"`[^`]+`", "", result)

    # Remove markdown tables (lines starting with |)
    result = re.sub(r"^\|.*\|$", "", result, flags=re.MULTILINE)

    # Remove file paths (Unix and Windows style)
    result = re.sub(r"(?:/[\w.-]+)+/?", "", result)
    result = re.sub(r"(?:[A-Za-z]:\\[\w\\.-]+)+", "", result)

    # Remove URLs
    result = re.sub(r"https?://[^\s]+", "", result)

    # Clean up multiple spaces/newlines
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r" {2,}", " ", result)
    result = result.strip()

    # Truncate to max_chars
    if len(result) > max_chars:
        # Try to break at sentence boundary
        truncated = result[:max_chars]
        last_period = truncated.rfind(". ")
        if last_period > max_chars // 2:
            result = truncated[:last_period + 1]
        else:
            result = truncated.rsplit(" ", 1)[0] + "..."

    return result
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_filter.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/claude_talk/filter.py tests/test_filter.py
git commit -m "feat: add text filtering module"
```

---

## Task 4: TTS Module (Bark Wrapper)

**Files:**
- Create: `src/claude_talk/tts.py`
- Test: `tests/test_tts.py`

**Step 1: Write the failing test**

```python
import numpy as np
from unittest.mock import patch, MagicMock

from claude_talk.tts import BarkTTS, setup_models


def test_bark_tts_init():
    with patch("claude_talk.tts.preload_models"):
        tts = BarkTTS(model_size="small")
        assert tts.model_size == "small"


def test_bark_tts_synthesize_returns_audio():
    with patch("claude_talk.tts.generate_audio") as mock_gen:
        mock_gen.return_value = np.zeros(24000, dtype=np.float32)
        with patch("claude_talk.tts.preload_models"):
            tts = BarkTTS(model_size="small")
            audio = tts.synthesize("Hello world", voice="v2/en_speaker_6")
            assert isinstance(audio, np.ndarray)
            mock_gen.assert_called_once()


def test_setup_models_sets_env_for_small():
    with patch("claude_talk.tts.preload_models") as mock_preload:
        with patch.dict("os.environ", {}, clear=True):
            import os
            setup_models("small")
            assert os.environ.get("SUNO_USE_SMALL_MODELS") == "True"
            mock_preload.assert_called_once()


def test_setup_models_unsets_env_for_large():
    with patch("claude_talk.tts.preload_models") as mock_preload:
        with patch.dict("os.environ", {"SUNO_USE_SMALL_MODELS": "True"}):
            import os
            setup_models("large")
            assert os.environ.get("SUNO_USE_SMALL_MODELS") != "True"
            mock_preload.assert_called_once()
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_tts.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'claude_talk.tts'"

**Step 3: Write implementation**

```python
"""Bark TTS wrapper for Claude Talk."""

import os
import numpy as np
import sounddevice as sd

from bark import SAMPLE_RATE, generate_audio, preload_models


def setup_models(model_size: str = "small") -> None:
    """Download and load Bark models."""
    if model_size == "small":
        os.environ["SUNO_USE_SMALL_MODELS"] = "True"
    else:
        os.environ.pop("SUNO_USE_SMALL_MODELS", None)

    preload_models()


class BarkTTS:
    """Bark TTS synthesizer."""

    def __init__(self, model_size: str = "small"):
        self.model_size = model_size
        setup_models(model_size)

    def synthesize(self, text: str, voice: str = "v2/en_speaker_6") -> np.ndarray:
        """Synthesize text to audio array."""
        audio = generate_audio(text, history_prompt=voice)
        return audio

    def speak(self, text: str, voice: str = "v2/en_speaker_6") -> None:
        """Synthesize and play audio."""
        audio = self.synthesize(text, voice)
        sd.play(audio, samplerate=SAMPLE_RATE)
        sd.wait()
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_tts.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/claude_talk/tts.py tests/test_tts.py
git commit -m "feat: add Bark TTS wrapper"
```

---

## Task 5: Voice Samples Module

**Files:**
- Create: `src/claude_talk/voices.py`
- Test: `tests/test_voices.py`

**Step 1: Write the failing test**

```python
from claude_talk.voices import VOICES, get_voice_sample


def test_voices_has_entries():
    assert len(VOICES) >= 3


def test_each_voice_has_required_fields():
    for voice_id, voice in VOICES.items():
        assert "name" in voice
        assert "joke" in voice
        assert voice_id.startswith("v2/")


def test_get_voice_sample():
    voice_id, voice = get_voice_sample(0)
    assert voice_id.startswith("v2/")
    assert "joke" in voice
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_voices.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'claude_talk.voices'"

**Step 3: Write implementation**

```python
"""Voice presets and sample jokes for Claude Talk."""

VOICES = {
    "v2/en_speaker_6": {
        "name": "Speaker 6 (Neutral)",
        "joke": "Why do programmers prefer dark mode? Because light attracts bugs.",
    },
    "v2/en_speaker_3": {
        "name": "Speaker 3 (Warm)",
        "joke": "There are only 10 kinds of people. Those who understand binary, and those who don't.",
    },
    "v2/en_speaker_9": {
        "name": "Speaker 9 (Clear)",
        "joke": "A SQL query walks into a bar, sees two tables, and asks... can I join you?",
    },
    "v2/en_speaker_0": {
        "name": "Speaker 0 (Calm)",
        "joke": "Why do Java developers wear glasses? Because they can't C sharp.",
    },
}


def get_voice_sample(index: int) -> tuple[str, dict]:
    """Get voice by index for selection UI."""
    voice_ids = list(VOICES.keys())
    voice_id = voice_ids[index % len(voice_ids)]
    return voice_id, VOICES[voice_id]


def list_voices() -> list[tuple[str, dict]]:
    """List all available voices."""
    return list(VOICES.items())
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_voices.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/claude_talk/voices.py tests/test_voices.py
git commit -m "feat: add voice presets with programming jokes"
```

---

## Task 6: CLI Module - Speak Command

**Files:**
- Create: `src/claude_talk/cli.py`
- Test: `tests/test_cli.py`

**Step 1: Write the failing test**

```python
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
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'claude_talk.cli'"

**Step 3: Write implementation**

```python
"""CLI for Claude Talk."""

import sys

from claude_talk.config import load_config, DEFAULT_CONFIG_PATH
from claude_talk.filter import filter_text
from claude_talk.tts import BarkTTS


def speak_command(text: str) -> None:
    """Filter and speak text if enabled."""
    config = load_config(DEFAULT_CONFIG_PATH)

    if not config.enabled:
        return

    filtered = filter_text(text, max_chars=config.max_chars)

    if not filtered.strip():
        return

    tts = BarkTTS(model_size=config.model_size)
    tts.speak(filtered, voice=config.voice)


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: claude-talk <command>", file=sys.stderr)
        print("Commands: speak, setup", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "speak":
        text = sys.stdin.read()
        speak_command(text)
    elif command == "setup":
        from claude_talk.setup import run_setup
        run_setup()
    elif command == "enable":
        from claude_talk.config import load_config, save_config
        config = load_config()
        config.enabled = True
        save_config(config)
        print("Claude Talk enabled.")
    elif command == "disable":
        from claude_talk.config import load_config, save_config
        config = load_config()
        config.enabled = False
        save_config(config)
        print("Claude Talk disabled.")
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_cli.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/claude_talk/cli.py tests/test_cli.py
git commit -m "feat: add CLI with speak command"
```

---

## Task 7: Setup Module

**Files:**
- Create: `src/claude_talk/setup.py`
- Test: `tests/test_setup.py`

**Step 1: Write the failing test**

```python
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
```

**Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_setup.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'claude_talk.setup'"

**Step 3: Write implementation**

```python
"""Setup flow for Claude Talk."""

import json
from pathlib import Path

from claude_talk.config import Config, save_config, DEFAULT_CONFIG_PATH
from claude_talk.voices import list_voices
from claude_talk.tts import setup_models, BarkTTS


CLAUDE_SETTINGS_PATH = Path.home() / ".claude" / "settings.json"


def install_hook(settings_path: Path = CLAUDE_SETTINGS_PATH) -> None:
    """Install the AssistantResponse hook in Claude settings."""
    settings = {}
    if settings_path.exists():
        settings = json.loads(settings_path.read_text())

    if "hooks" not in settings:
        settings["hooks"] = {}

    settings["hooks"]["AssistantResponse"] = [
        {
            "type": "command",
            "command": "uvx claude-talk speak"
        }
    ]

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2))


def run_setup() -> None:
    """Interactive setup flow."""
    print("Claude Talk Setup")
    print("=" * 40)
    print()

    # Step 1: Choose model size
    print("Step 1: Choose model size")
    print("  1. Small (faster, ~2-4GB VRAM)")
    print("  2. Large (better quality, ~8-12GB VRAM)")
    print()

    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice in ("1", "2"):
            break
        print("Please enter 1 or 2.")

    model_size = "small" if choice == "1" else "large"

    # Step 2: Download models
    print()
    print(f"Step 2: Downloading {model_size} models...")
    print("(This may take a few minutes)")
    print()
    setup_models(model_size)
    print("Models downloaded!")
    print()

    # Step 3: Voice selection
    print("Step 3: Choose your voice")
    print("Listen to each sample and pick your favorite.")
    print()

    tts = BarkTTS(model_size=model_size)
    voices = list_voices()

    for i, (voice_id, voice_info) in enumerate(voices, 1):
        print(f"  {i}. {voice_info['name']}")
        print(f"     Playing sample...")
        tts.speak(voice_info["joke"], voice=voice_id)
        print()

    while True:
        choice = input(f"Enter choice (1-{len(voices)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(voices):
            break
        print(f"Please enter a number between 1 and {len(voices)}.")

    selected_voice_id = voices[int(choice) - 1][0]

    # Step 4: Save config
    print()
    print("Step 4: Saving configuration...")
    config = Config(
        enabled=True,
        voice=selected_voice_id,
        model_size=model_size,
        max_chars=500,
    )
    save_config(config, DEFAULT_CONFIG_PATH)
    print(f"Config saved to {DEFAULT_CONFIG_PATH}")

    # Step 5: Install hook
    print()
    print("Step 5: Installing Claude Code hook...")
    install_hook()
    print(f"Hook installed in {CLAUDE_SETTINGS_PATH}")

    # Done!
    print()
    print("=" * 40)
    print("Setup complete! Claude will now speak responses aloud.")
    print()
    print("Quick commands:")
    print("  /claude-talk:disable  - Turn off speech")
    print("  /claude-talk:enable   - Turn on speech")
    print("  /claude-talk:voice    - Change voice")
    print()
```

**Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_setup.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/claude_talk/setup.py tests/test_setup.py
git commit -m "feat: add setup flow with voice selection"
```

---

## Task 8: Slash Commands (Claude Code Skills)

**Files:**
- Create: `.claude/skills/claude-talk/setup.md`
- Create: `.claude/skills/claude-talk/enable.md`
- Create: `.claude/skills/claude-talk/disable.md`
- Create: `.claude/skills/claude-talk/voice.md`

**Step 1: Create setup skill**

```markdown
---
name: setup
description: Set up Claude Talk TTS - download models, choose voice, install hook
user_invocable: true
---

# Claude Talk Setup

Run the interactive setup flow for Claude Talk TTS.

Execute this command:

```bash
uvx claude-talk setup
```

This will:
1. Ask which model size to download (small/large)
2. Download Bark TTS models
3. Play voice samples with programming jokes
4. Let the user pick their favorite voice
5. Save configuration
6. Install the AssistantResponse hook
```

**Step 2: Create enable skill**

```markdown
---
name: enable
description: Enable Claude Talk TTS
user_invocable: true
---

# Enable Claude Talk

Enable text-to-speech for Claude responses.

```bash
uvx claude-talk enable
```

After running, Claude's responses will be spoken aloud.
```

**Step 3: Create disable skill**

```markdown
---
name: disable
description: Disable Claude Talk TTS
user_invocable: true
---

# Disable Claude Talk

Disable text-to-speech for Claude responses.

```bash
uvx claude-talk disable
```

After running, Claude's responses will be silent.
```

**Step 4: Create voice skill**

```markdown
---
name: voice
description: Change Claude Talk voice
user_invocable: true
---

# Change Claude Talk Voice

Change the voice used for text-to-speech.

Run this Python script to play samples and select a new voice:

```python
from claude_talk.config import load_config, save_config
from claude_talk.voices import list_voices
from claude_talk.tts import BarkTTS

config = load_config()
tts = BarkTTS(model_size=config.model_size)
voices = list_voices()

print("Available voices:")
for i, (voice_id, info) in enumerate(voices, 1):
    print(f"\n{i}. {info['name']}")
    print("   Playing sample...")
    tts.speak(info["joke"], voice=voice_id)

choice = int(input(f"\nEnter choice (1-{len(voices)}): "))
selected = voices[choice - 1][0]

config.voice = selected
save_config(config)
print(f"\nVoice changed to {selected}")
```
```

**Step 5: Commit**

```bash
git add .claude/skills/claude-talk/
git commit -m "feat: add Claude Code slash commands"
```

---

## Task 9: Create pytest configuration

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

**Step 1: Create test package init**

```python
"""Tests for Claude Talk."""
```

**Step 2: Create conftest with fixtures**

```python
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
```

**Step 3: Commit**

```bash
git add tests/__init__.py tests/conftest.py
git commit -m "feat: add pytest configuration"
```

---

## Task 10: Final Integration Test

**Files:**
- Create: `tests/test_integration.py`

**Step 1: Write integration test**

```python
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
```

**Step 2: Run all tests**

Run: `uv run pytest tests/ -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add tests/test_integration.py
git commit -m "feat: add integration tests"
```

---

## Task 11: Final Verification

**Step 1: Run full test suite**

Run: `uv run pytest tests/ -v --tb=short`
Expected: All tests PASS

**Step 2: Test manual installation**

Run: `uv tool install . --force`
Expected: Installs successfully

**Step 3: Verify CLI works**

Run: `claude-talk --help` or `uvx claude-talk`
Expected: Shows usage info

**Step 4: Final commit**

```bash
git add -A
git commit -m "chore: final cleanup and verification"
```

---

## Summary

After completing all tasks, the plugin will:
- Speak Claude responses aloud using Bark TTS
- Filter out code blocks, tables, URLs, file paths
- Truncate long responses to 500 chars (configurable)
- Support small/large model selection
- Provide `/claude-talk:setup`, `/claude-talk:enable`, `/claude-talk:disable`, `/claude-talk:voice` commands
- Store config in `~/.config/claude-talk/config.toml`
- Use `AssistantResponse` hook in `~/.claude/settings.json`

# Claude Talk TTS Plugin Design

A Claude Code plugin that reads assistant responses aloud using Bark TTS.

## Overview

Uses Claude Code's `AssistantResponse` hook to automatically speak Claude's responses. Filters out code blocks, tables, and other non-conversational content. Uses Bark by Suno for high-quality TTS.

## Project Structure

```
claude-talk/
├── pyproject.toml              # Package config, dependencies, CLI entry point
├── src/
│   └── claude_talk/
│       ├── __init__.py
│       ├── cli.py              # CLI commands: setup, speak
│       ├── tts.py              # Bark TTS wrapper
│       ├── filter.py           # Regex filtering (strip code, tables, etc.)
│       ├── config.py           # Load/save user config
│       └── voices.py           # Voice presets + programming jokes for demos
```

## Configuration

**User config:** `~/.config/claude-talk/config.toml`

```toml
enabled = true
voice = "v2/en_speaker_6"
model_size = "small"
max_chars = 500
```

**Models location:** Bark's default cache (`~/.cache/suno/bark_v0/`)

## Hook Configuration

Added to `~/.claude/settings.json` by setup:

```json
{
  "hooks": {
    "AssistantResponse": [
      {
        "type": "command",
        "command": "uvx claude-talk speak"
      }
    ]
  }
}
```

## Commands

### CLI Commands (via `uvx claude-talk`)

- `setup` - Download models, pick voice, configure hook
- `speak` - Called by hook, reads stdin, filters, speaks

### Slash Commands (Claude Code skills)

- `/claude-talk:setup` - Full setup flow
- `/claude-talk:enable` - Turn TTS on
- `/claude-talk:disable` - Turn TTS off
- `/claude-talk:voice` - Change voice (plays samples)

## Text Filtering

Regex-based filtering removes:
- Fenced code blocks (``` ... ```)
- Inline code (`...`)
- Markdown tables
- File paths and URLs
- Tool call artifacts

After filtering, truncate to `max_chars` (default 500).

## Setup Flow

1. Check dependencies (Python, uv)
2. Choose model size: Small (~2-4GB VRAM) or Large (~8-12GB)
3. Download Bark models with progress indication
4. Voice selection - play 3-4 samples with programming jokes:
   - "Why do programmers prefer dark mode? Because light attracts bugs."
   - "There are only 10 kinds of people - those who understand binary and those who don't."
   - "A SQL query walks into a bar, sees two tables and asks... can I join you?"
5. User picks favorite voice
6. Write config to `~/.config/claude-talk/config.toml`
7. Install hook in `~/.claude/settings.json`
8. Show completion message with quick command reference

## Post-Setup Message

```
Setup complete! Claude will now speak responses aloud.

Quick commands:
  /claude-talk:disable  - Turn off speech
  /claude-talk:enable   - Turn on speech
  /claude-talk:voice    - Change voice
```

## Speak Command Flow

1. Read assistant response from stdin
2. Check if enabled in config - exit silently if not
3. Filter text (remove code, tables, etc.)
4. Truncate to max_chars
5. If text remains, send to Bark TTS
6. Play audio, exit silently

## Dependencies

- `bark` - Suno's Bark TTS
- `torch` - Required by Bark
- `scipy` - Audio output
- `tomli` / `tomllib` - Config parsing

## Key Decisions

- **Hook-based** (not MCP) - TTS happens automatically, Claude doesn't need to call a tool
- **Regex filtering** - Simple, fast, handles common cases
- **uv-based packaging** - Clean CLI execution via `uvx`, no environment management
- **User choice for model size** - Accommodates different hardware
- **Voice samples with jokes** - Fun setup experience
- **Truncation** - Keeps speech reasonable length, avoids long waits

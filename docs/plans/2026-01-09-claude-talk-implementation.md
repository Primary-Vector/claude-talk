# Claude Talk TTS Implementation Plan

**Goal:** Build a Claude Code plugin that speaks assistant responses aloud using Kokoro ONNX TTS.

**Architecture:** Hook-based TTS triggered by `PreToolUse` and `Stop` hooks. Text is filtered (remove code/tables), truncated, then spoken via Kokoro ONNX. Configuration stored in TOML. Slash commands for setup/enable/disable/voice.

**Tech Stack:** Python 3.11+, Kokoro ONNX (`kokoro-onnx`), soundfile, sounddevice, espeak-ng (for phoneme generation)

---

## Features

- Speaks Claude's responses automatically via hooks
- Fast, near real-time TTS using Kokoro ONNX (~340MB model)
- Filters out code blocks, URLs, and file paths - only speaks conversational content
- 10 diverse voice options (American and British, male and female)
- Async playback - doesn't block Claude while speaking
- New messages interrupt existing playback

## Architecture

### Hooks
- **PreToolUse**: Speaks Claude's intro text before running tools
- **Stop**: Speaks Claude's final response

### Text Filtering
Content is filtered to remove:
- Code blocks (fenced and inline)
- Markdown tables
- URLs and file paths
- Markdown formatting (bold, italic, headers)

### Voice Options

**American Female:**
- `af_heart` - Warm
- `af_bella` - Expressive
- `af_nicole` - Clear
- `af_sky` - Bright

**American Male:**
- `am_michael` - Professional
- `am_adam` - Friendly

**British Female:**
- `bf_emma` - Elegant
- `bf_isabella` - Refined

**British Male:**
- `bm_george` - Distinguished
- `bm_lewis` - Thoughtful

## Configuration

Config stored at `~/.config/claude-talk/config.toml`:

```toml
enabled = true
voice = "af_heart"
max_chars = 500
```

## Commands

- `/talk:setup` - Interactive setup wizard
- `/talk:enable` - Enable TTS
- `/talk:disable` - Disable TTS
- `/talk:voice` - Change voice

## Installation

Via marketplace:
```
/plugin marketplace add primary-vector/claude-marketplace
/plugin install talk@primary-vector-marketplace
/talk:setup
```

## Dependencies

- `kokoro-onnx>=0.4.0` - ONNX runtime for TTS synthesis
- `soundfile>=0.12.0` - Audio file I/O
- `sounddevice>=0.4.6` - Audio playback
- `espeak-ng` - Phoneme generation (installed via Homebrew)

## Models

Downloaded during setup to `<plugin>/models/`:
- `kokoro-v1.0.onnx` (~310MB) - Main TTS model
- `voices-v1.0.bin` (~27MB) - Voice data

## Requirements

- Python 3.11+
- macOS (Apple Silicon recommended)
- Homebrew (for espeak-ng)

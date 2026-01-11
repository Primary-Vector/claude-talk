# claude-talk

TTS plugin for Claude Code that speaks Claude's responses aloud using [Kokoro](https://github.com/thewh1teagle/kokoro-onnx).

## Features

- Speaks Claude's responses automatically via hooks
- Fast, near real-time TTS using Kokoro ONNX (~300MB model)
- Filters out code blocks, URLs, and file paths - only speaks conversational content
- Multiple voice options (female/male)
- Async playback - doesn't block Claude while speaking
- New messages interrupt existing playback

## Installation

### Via Marketplace (Recommended)

In Claude Code, register the marketplace:

```
/plugin marketplace add primary-vector/claude-marketplace
```

Then install the plugin:

```
/plugin install talk@primary-vector-marketplace
```

Run setup:

```
/talk:setup
```

Restart Claude Code.

### Manual Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/primary-vector/claude-talk.git
   ```

2. Run setup in Claude Code:
   ```
   /talk:setup
   ```

   This will:
   - Install Python dependencies
   - Download the Kokoro TTS models (~340MB)
   - Let you choose from available voices
   - Configure the Claude Code hooks

3. Restart Claude Code

## Commands

Use these as slash commands in Claude Code:

- `/talk:setup` - Interactive setup wizard
- `/talk:enable` - Enable TTS
- `/talk:disable` - Disable TTS
- `/talk:voice` - Change voice

## Available Voices

**American:**
- `af_heart` - Female, warm
- `af_bella` - Female, expressive
- `af_nicole` - Female, clear
- `af_sky` - Female, bright
- `am_michael` - Male, professional
- `am_adam` - Male, friendly

**British:**
- `bf_emma` - Female, elegant
- `bf_isabella` - Female, refined
- `bm_george` - Male, distinguished
- `bm_lewis` - Male, thoughtful

## Configuration

Config is stored at `~/.config/claude-talk/config.toml`:

```toml
enabled = true
voice = "af_bella"
max_chars = 500
```

## How It Works

The plugin installs two Claude Code hooks:

1. **PreToolUse** - Speaks Claude's intro text before running tools
2. **Stop** - Speaks Claude's final response

Content is filtered to remove:
- Code blocks (fenced and inline)
- Markdown tables
- URLs and file paths
- Markdown formatting (bold, italic, headers)

The TTS runs in a background subprocess so it doesn't block Claude. New messages automatically stop any existing playback.

## Requirements

- Python 3.11+
- macOS (uses ONNX runtime, works great on Apple Silicon)
- espeak-ng: `brew install espeak-ng`

## License

MIT

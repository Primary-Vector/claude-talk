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

1. Clone this repo:
   ```bash
   git clone https://github.com/primary-vector/claude-talk.git
   ```

2. Install dependencies:
   ```bash
   cd claude-talk
   uv sync
   ```

3. Download the Kokoro models (~340MB):
   ```bash
   mkdir -p models
   curl -L -o models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
   curl -L -o models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
   ```

4. Run setup in Claude Code:
   ```
   /claude-talk:setup
   ```

   Or manually install the hooks by running:
   ```bash
   uv run python -c "
   import sys
   sys.path.insert(0, 'src')
   from claude_talk.setup import install_hook
   install_hook()
   "
   ```

5. Restart Claude Code

## Commands

Use these as slash commands in Claude Code:

- `/claude-talk:setup` - Interactive setup wizard
- `/claude-talk:enable` - Enable TTS
- `/claude-talk:disable` - Disable TTS
- `/claude-talk:voice` - Change voice

## Available Voices

- `af_heart` - Female, warm
- `am_michael` - Male, professional
- `af_bella` - Female, expressive
- `am_fenrir` - Male, deep

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

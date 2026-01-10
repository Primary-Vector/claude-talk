---
description: Set up Claude Talk TTS - download models, choose voice, install hook
---

# Claude Talk Setup

Run the complete setup for Claude Talk TTS. This will install dependencies, download models, let the user choose a voice, and configure the hooks.

## Step 1: Install Dependencies

```bash
cd /Users/pv/git/claude-talk && uv sync
```

## Step 2: Download Models

Download the Kokoro ONNX models (~340MB total):

```bash
mkdir -p /Users/pv/git/claude-talk/models
curl -L -o /Users/pv/git/claude-talk/models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o /Users/pv/git/claude-talk/models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

Verify the models downloaded:

```bash
ls -la /Users/pv/git/claude-talk/models/
```

## Step 3: Voice Selection

Play voice samples for the user to choose from. For each voice, run the command and let them hear it:

**Voice 1 - Heart (Female, Warm):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak('Why do programmers prefer dark mode? Because light attracts bugs.', voice='af_heart')
"
```

**Voice 2 - Michael (Male, Professional):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak('Why do Java developers wear glasses? Because they cant C sharp.', voice='am_michael')
"
```

**Voice 3 - Bella (Female, Expressive):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak('There are only 10 kinds of people. Those who understand binary, and those who dont.', voice='af_bella')
"
```

**Voice 4 - Fenrir (Male, Deep):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak('A SQL query walks into a bar, sees two tables, and asks... can I join you?', voice='am_fenrir')
"
```

Ask which voice they prefer after playing the samples.

## Step 4: Save Configuration

Once they choose a voice, save the config (replace VOICE_ID with the chosen voice, e.g., 'af_heart'):

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.config import Config, save_config
config = Config(
    enabled=True,
    voice='VOICE_ID',
    max_chars=500
)
save_config(config)
print('Configuration saved!')
"
```

## Step 5: Install Hook

Install the Claude Code hooks:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.setup import install_hook
install_hook()
print('Hook installed!')
"
```

## Done!

Tell the user setup is complete and remind them of the commands:
- `/claude-talk:disable` - Turn off speech
- `/claude-talk:enable` - Turn on speech
- `/claude-talk:voice` - Change voice

Note: They'll need to restart Claude Code for the hook to take effect.

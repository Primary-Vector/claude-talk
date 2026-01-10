---
description: Set up Claude Talk TTS - download models, choose voice, install hook
---

# Claude Talk Setup

Guide the user through setting up Claude Talk TTS interactively.

## Step 1: Download Models

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

## Step 2: Voice Selection

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

**Voice 2 - Bella (Female, Expressive):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak('There are only 10 kinds of people. Those who understand binary, and those who dont.', voice='af_bella')
"
```

**Voice 3 - Nicole (Female, Clear):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak('A SQL query walks into a bar, sees two tables, and asks... can I join you?', voice='af_nicole')
"
```

**Voice 4 - Michael (Male, Professional):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak('Why do Java developers wear glasses? Because they cant C sharp.', voice='am_michael')
"
```

Ask which voice they prefer after playing the samples.

## Step 3: Save Configuration

Once they choose a voice, save the config:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.config import Config, save_config
config = Config(
    enabled=True,
    voice='VOICE_ID',  # e.g., 'af_heart'
    max_chars=500
)
save_config(config)
print('Configuration saved!')
"
```

## Step 4: Install Hook

Install the AssistantResponse hook:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.setup import install_hook
install_hook()
print('Hook installed!')
"
```

## Step 5: Done!

Tell the user setup is complete and remind them of the commands:
- `/claude-talk:disable` - Turn off speech
- `/claude-talk:enable` - Turn on speech
- `/claude-talk:voice` - Change voice

Note: They'll need to restart Claude Code for the hook to take effect.

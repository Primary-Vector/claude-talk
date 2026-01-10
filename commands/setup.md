---
description: Set up Claude Talk TTS - download models, choose voice, install hook
---

# Claude Talk Setup

Guide the user through setting up Claude Talk TTS interactively.

## Step 1: Choose Model Size

Ask the user which model size they want:
- **Small** (faster, ~2-4GB VRAM) - Good for quick responses
- **Large** (better quality, ~8-12GB VRAM) - More natural sounding

## Step 2: Download Models

Once they choose, download the Bark models by running:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import setup_models
print('Downloading models... this may take a few minutes.')
setup_models('MODEL_SIZE')  # Replace with 'small' or 'large'
print('Models downloaded!')
"
```

Replace `MODEL_SIZE` with their choice.

## Step 3: Voice Selection

Play voice samples for the user to choose from. For each voice, run the command and let them hear it:

**Voice 1 - Speaker 6 (Neutral):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import BarkTTS
tts = BarkTTS(model_size='MODEL_SIZE')
tts.speak('Why do programmers prefer dark mode? Because light attracts bugs.', voice='v2/en_speaker_6')
"
```

**Voice 2 - Speaker 3 (Warm):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import BarkTTS
tts = BarkTTS(model_size='MODEL_SIZE')
tts.speak('There are only 10 kinds of people. Those who understand binary, and those who dont.', voice='v2/en_speaker_3')
"
```

**Voice 3 - Speaker 9 (Clear):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import BarkTTS
tts = BarkTTS(model_size='MODEL_SIZE')
tts.speak('A SQL query walks into a bar, sees two tables, and asks... can I join you?', voice='v2/en_speaker_9')
"
```

**Voice 4 - Speaker 0 (Calm):**
```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.tts import BarkTTS
tts = BarkTTS(model_size='MODEL_SIZE')
tts.speak('Why do Java developers wear glasses? Because they cant C sharp.', voice='v2/en_speaker_0')
"
```

Ask which voice they prefer after playing the samples.

## Step 4: Save Configuration

Once they choose a voice, save the config:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.config import Config, save_config
config = Config(
    enabled=True,
    voice='VOICE_ID',  # e.g., 'v2/en_speaker_6'
    model_size='MODEL_SIZE',
    max_chars=500
)
save_config(config)
print('Configuration saved!')
"
```

## Step 5: Install Hook

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

## Step 6: Done!

Tell the user setup is complete and remind them of the commands:
- `/claude-talk:disable` - Turn off speech
- `/claude-talk:enable` - Turn on speech
- `/claude-talk:voice` - Change voice

Note: They'll need to restart Claude Code for the hook to take effect.

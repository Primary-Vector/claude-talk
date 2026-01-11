---
description: Set up Claude Talk TTS - download models, choose voice, install hook
---

# Claude Talk Setup

Run the complete setup for Claude Talk TTS. This will install dependencies, download models, let the user choose a voice, and configure the hooks.

## Step 1: Install Dependencies

```bash
python3 -m pip install -q -r /Users/pv/git/claude-talk/requirements.txt
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

Present the list of available voices to the user. **Do not play samples upfront** - only play when they pick one.

**Available voices:**

| # | Voice ID | Description |
|---|----------|-------------|
| 1 | af_heart | Heart (American Female, Warm) |
| 2 | af_bella | Bella (American Female, Expressive) |
| 3 | af_nicole | Nicole (American Female, Clear) |
| 4 | af_sky | Sky (American Female, Bright) |
| 5 | am_michael | Michael (American Male, Professional) |
| 6 | am_adam | Adam (American Male, Friendly) |
| 7 | bf_emma | Emma (British Female, Elegant) |
| 8 | bf_isabella | Isabella (British Female, Refined) |
| 9 | bm_george | George (British Male, Distinguished) |
| 10 | bm_lewis | Lewis (British Male, Thoughtful) |

Ask the user which voice they'd like to hear. When they pick one, play the sample:

```bash
python3 -c "
import sys
sys.path.insert(0, '/Users/pv/git/claude-talk/src')
from claude_talk.tts import KokoroTTS
from claude_talk.voices import VOICES
tts = KokoroTTS()
voice_id = 'VOICE_ID'  # Replace with chosen voice
tts.speak(VOICES[voice_id]['joke'], voice=voice_id)
"
```

After playing the sample, ask: "Would you like to use this voice, or pick another?"

- If they confirm, proceed to Step 4 with that voice
- If they want another, show the list again and repeat

## Step 4: Save Configuration

Once they choose a voice, save the config (replace VOICE_ID with the chosen voice, e.g., 'af_heart'):

```bash
python3 -c "
import sys
sys.path.insert(0, '/Users/pv/git/claude-talk/src')
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
python3 -c "
import sys
sys.path.insert(0, '/Users/pv/git/claude-talk/src')
from claude_talk.setup import install_hook
install_hook()
print('Hook installed!')
"
```

## Done!

Tell the user setup is complete and remind them of the commands:
- `/talk:disable` - Turn off speech
- `/talk:enable` - Turn on speech
- `/talk:voice` - Change voice

Note: They'll need to restart Claude Code for the hook to take effect.

---
description: Change Claude Talk voice
---

# Change Claude Talk Voice

Guide the user through changing their Claude Talk voice interactively.

First, check their current config to get the model size:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.config import load_config
config = load_config()
print(f'Current voice: {config.voice}')
print(f'Model size: {config.model_size}')
"
```

Then play each voice sample (use their model_size from above):

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

After playing samples, ask which voice they prefer, then save their choice:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.config import load_config, save_config
config = load_config()
config.voice = 'VOICE_ID'  # Replace with chosen voice
save_config(config)
print(f'Voice changed to VOICE_ID')
"
```

Replace `VOICE_ID` with their choice (e.g., `v2/en_speaker_6`).

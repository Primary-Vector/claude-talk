---
description: Change Claude Talk voice
---

# Change Claude Talk Voice

Guide the user through changing their Claude Talk voice interactively.

First, check their current config:

```bash
uv run --directory /Users/pv/git/claude-talk python -c "
import sys
sys.path.insert(0, 'src')
from claude_talk.config import load_config
config = load_config()
print(f'Current voice: {config.voice}')
"
```

Then play each voice sample:

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

Replace `VOICE_ID` with their choice (e.g., `af_heart`).

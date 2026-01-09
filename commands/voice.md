---
description: Change Claude Talk voice
---

# Change Claude Talk Voice

Change the voice used for text-to-speech.

Run this Python script to play samples and select a new voice:

```python
from claude_talk.config import load_config, save_config
from claude_talk.voices import list_voices
from claude_talk.tts import BarkTTS

config = load_config()
tts = BarkTTS(model_size=config.model_size)
voices = list_voices()

print("Available voices:")
for i, (voice_id, info) in enumerate(voices, 1):
    print(f"\n{i}. {info['name']}")
    print("   Playing sample...")
    tts.speak(info["joke"], voice=voice_id)

choice = int(input(f"\nEnter choice (1-{len(voices)}): "))
selected = voices[choice - 1][0]

config.voice = selected
save_config(config)
print(f"\nVoice changed to {selected}")
```

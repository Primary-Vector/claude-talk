---
name: setup
description: Set up Claude Talk TTS - download models, choose voice, install hook
user_invocable: true
---

# Claude Talk Setup

Run the interactive setup flow for Claude Talk TTS.

Execute this command:

```bash
uvx claude-talk setup
```

This will:
1. Ask which model size to download (small/large)
2. Download Bark TTS models
3. Play voice samples with programming jokes
4. Let the user pick their favorite voice
5. Save configuration
6. Install the AssistantResponse hook

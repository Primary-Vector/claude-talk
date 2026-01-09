---
description: Set up Claude Talk TTS - download models, choose voice, install hook
---

# Claude Talk Setup

Run the interactive setup flow for Claude Talk TTS by executing:

```bash
uv run --directory /Users/pv/git/claude-talk python run.py setup
```

This will:
1. Ask which model size to download (small/large)
2. Download Bark TTS models
3. Play voice samples with programming jokes
4. Let the user pick their favorite voice
5. Save configuration
6. Install the AssistantResponse hook

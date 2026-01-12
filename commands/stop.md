---
description: Stop Claude Talk TTS playback
---

# Stop Claude Talk

Stop any currently playing text-to-speech audio.

First, determine the plugin directory by finding where this command file is located. The plugin root is the parent of the `commands` directory.

```bash
python3 <PLUGIN_ROOT>/run.py stop
```

Replace `<PLUGIN_ROOT>` with the actual plugin directory path.

This will immediately silence any speech in progress.

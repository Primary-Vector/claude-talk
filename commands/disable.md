---
description: Disable Claude Talk TTS
---

# Disable Claude Talk

Disable text-to-speech for Claude responses.

First, determine the plugin directory by finding where this command file is located. The plugin root is the parent of the `commands` directory.

```bash
python3 <PLUGIN_ROOT>/run.py disable
```

Replace `<PLUGIN_ROOT>` with the actual plugin directory path.

After running, Claude's responses will be silent.

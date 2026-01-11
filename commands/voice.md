---
description: Change Claude Talk voice
---

# Change Claude Talk Voice

Guide the user through changing their Claude Talk voice interactively.

First, determine the plugin directory by finding where this command file is located. The plugin root is the parent of the `commands` directory.

Check their current config:

```bash
python3 <PLUGIN_ROOT>/run.py current-voice
```

Present the list of available voices. **Do not play samples upfront** - only play when they pick one.

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
python3 <PLUGIN_ROOT>/run.py sample <VOICE_ID>
```

Replace `<VOICE_ID>` with the chosen voice (e.g., `af_heart`).

After playing the sample, ask: "Would you like to use this voice, or pick another?"

- If they confirm, save the config
- If they want another, show the list again and repeat

Save their choice:

```bash
python3 <PLUGIN_ROOT>/run.py set-voice <VOICE_ID>
```

Replace `<PLUGIN_ROOT>` with the actual plugin directory path.

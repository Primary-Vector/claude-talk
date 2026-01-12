---
description: Set up Claude Talk TTS - download models, choose voice, install hook
---

# Claude Talk Setup

Run the complete setup for Claude Talk TTS. This will install dependencies, download models, let the user choose a voice, and configure the hooks.

First, determine the plugin directory by finding where this command file is located. The plugin root is the parent of the `commands` directory.

## Step 1: Install System Dependencies

Check if espeak-ng is installed (required for phoneme generation):

```bash
which espeak-ng || echo "NOT_INSTALLED"
```

If espeak-ng is not installed, install it via Homebrew:

```bash
brew install espeak-ng
```

## Step 2: Install Python Dependencies

Install the required Python packages:

```bash
python3 -m pip install -q kokoro-onnx soundfile sounddevice
```

## Step 3: Download Models

Download the Kokoro ONNX models (~340MB total) to the plugin's models directory:

```bash
mkdir -p <PLUGIN_ROOT>/models
curl -L -o <PLUGIN_ROOT>/models/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o <PLUGIN_ROOT>/models/voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

Replace `<PLUGIN_ROOT>` with the actual plugin directory path.

Verify the models downloaded:

```bash
ls -la <PLUGIN_ROOT>/models/
```

## Step 4: Voice Selection

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

Ask the user which voice they'd like to hear. When they pick one, play the sample using the plugin's run.py:

```bash
python3 <PLUGIN_ROOT>/run.py sample <VOICE_ID>
```

Replace `<VOICE_ID>` with the chosen voice (e.g., `af_heart`).

After playing the sample, ask: "Would you like to use this voice, or pick another?"

- If they confirm, proceed to Step 4 with that voice
- If they want another, show the list again and repeat

## Step 5: Save Configuration

Once they choose a voice, save the config:

```bash
python3 <PLUGIN_ROOT>/run.py set-voice <VOICE_ID>
```

## Step 6: Install Hook

Install the Claude Code hooks:

```bash
python3 <PLUGIN_ROOT>/run.py install-hook
```

## Done!

Tell the user setup is complete and remind them of the commands:
- `/talk:disable` - Turn off speech
- `/talk:enable` - Turn on speech
- `/talk:voice` - Change voice

Note: They'll need to restart Claude Code for the hook to take effect.

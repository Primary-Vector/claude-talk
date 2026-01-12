"""Setup flow for Claude Talk."""

import json
import subprocess
import sys
from pathlib import Path

from claude_talk.config import Config, save_config, DEFAULT_CONFIG_PATH
from claude_talk.voices import list_voices
from claude_talk.tts import setup_models, KokoroTTS, PLUGIN_ROOT


CLAUDE_SETTINGS_PATH = Path.home() / ".claude" / "settings.json"


def install_hook(settings_path: Path = CLAUDE_SETTINGS_PATH, plugin_root: Path = PLUGIN_ROOT) -> None:
    """Install the AssistantResponse hook in Claude settings."""
    settings = {}
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text())
        except json.JSONDecodeError:
            print(f"Warning: Could not parse {settings_path}, creating new settings")
            settings = {}

    if "hooks" not in settings:
        settings["hooks"] = {}

    # Use the local run.py script
    run_script = plugin_root / "run.py"
    command = f"{sys.executable} {run_script} speak"

    # Helper to add hook if not already present
    def add_hook_if_missing(hook_name: str) -> None:
        if hook_name not in settings["hooks"]:
            settings["hooks"][hook_name] = []

        hook_exists = any(
            any(h.get("command", "").endswith("run.py speak") for h in entry.get("hooks", []))
            for entry in settings["hooks"][hook_name]
        )

        if not hook_exists:
            settings["hooks"][hook_name].append({
                "hooks": [
                    {
                        "type": "command",
                        "command": command
                    }
                ]
            })

    # Add hooks for assistant responses
    add_hook_if_missing("PreToolUse")        # Speak intro before tools
    add_hook_if_missing("Stop")              # Speak final response

    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2))


def run_setup() -> None:
    """Interactive setup flow."""
    print("Claude Talk Setup")
    print("=" * 40)
    print()

    # Step 1: Install dependencies
    print("Step 1: Installing dependencies...")
    requirements_file = PLUGIN_ROOT / "requirements.txt"
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(requirements_file)],
            check=True
        )
        print("Dependencies installed!")
    except subprocess.CalledProcessError:
        print("Error: Failed to install dependencies. Please run:")
        print(f"  pip install -r {requirements_file}")
        return
    print()

    # Step 2: Download models
    print("Step 2: Downloading Kokoro TTS models...")
    print("(This may take a moment on first run)")
    print()
    setup_models()
    print("Models ready!")
    print()

    # Step 3: Voice selection
    print("Step 3: Choose your voice")
    print()

    tts = KokoroTTS()
    voices = list_voices()

    selected_voice_id = None
    while selected_voice_id is None:
        # Show all voices
        print("Available voices:")
        print()
        for i, (voice_id, voice_info) in enumerate(voices, 1):
            print(f"  {i}. {voice_info['name']}")
        print()

        # Get user choice
        while True:
            choice = input(f"Enter choice (1-{len(voices)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(voices):
                break
            print(f"Please enter a number between 1 and {len(voices)}.")

        choice_idx = int(choice) - 1
        voice_id, voice_info = voices[choice_idx]

        # Play sample
        print()
        print(f"Playing sample for {voice_info['name']}...")
        tts.speak(voice_info["joke"], voice=voice_id)
        print()

        # Confirm or pick another
        confirm = input("Use this voice? (y/n): ").strip().lower()
        if confirm in ("y", "yes"):
            selected_voice_id = voice_id
        else:
            print()
            print("Let's pick another voice.")
            print()

    # Step 4: Save config
    print()
    print("Step 4: Saving configuration...")
    config = Config(
        enabled=True,
        voice=selected_voice_id,
        max_chars=500,
    )
    save_config(config, DEFAULT_CONFIG_PATH)
    print(f"Config saved to {DEFAULT_CONFIG_PATH}")

    # Step 5: Install hook
    print()
    print("Step 5: Installing Claude Code hook...")
    install_hook()
    print(f"Hook installed in {CLAUDE_SETTINGS_PATH}")

    # Done!
    print()
    print("=" * 40)
    print("Setup complete! Claude will now speak responses aloud.")
    print()
    print("Quick commands:")
    print("  /talk:disable  - Turn off speech")
    print("  /talk:enable   - Turn on speech")
    print("  /talk:voice    - Change voice")
    print()

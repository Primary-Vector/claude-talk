"""CLI for Claude Talk."""

import sys

from claude_talk.config import load_config, DEFAULT_CONFIG_PATH
from claude_talk.filter import filter_text
from claude_talk.tts import BarkTTS


def speak_command(text: str) -> None:
    """Filter and speak text if enabled."""
    config = load_config(DEFAULT_CONFIG_PATH)

    if not config.enabled:
        return

    filtered = filter_text(text, max_chars=config.max_chars)

    if not filtered.strip():
        return

    tts = BarkTTS(model_size=config.model_size)
    tts.speak(filtered, voice=config.voice)


def voice_command() -> None:
    """Interactive voice selection."""
    from claude_talk.config import load_config, save_config
    from claude_talk.voices import list_voices

    config = load_config()
    tts = BarkTTS(model_size=config.model_size)
    voices = list_voices()

    print("Available voices:")
    for i, (voice_id, info) in enumerate(voices, 1):
        print(f"\n{i}. {info['name']}")
        print("   Playing sample...")
        tts.speak(info["joke"], voice=voice_id)

    while True:
        choice = input(f"\nEnter choice (1-{len(voices)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(voices):
            break
        print(f"Please enter a number between 1 and {len(voices)}.")

    selected = voices[int(choice) - 1][0]
    config.voice = selected
    save_config(config)
    print(f"\nVoice changed to {selected}")


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: claude-talk <command>", file=sys.stderr)
        print("Commands: speak, setup, enable, disable, voice", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "speak":
        text = sys.stdin.read()
        speak_command(text)
    elif command == "setup":
        from claude_talk.setup import run_setup
        run_setup()
    elif command == "enable":
        from claude_talk.config import load_config, save_config
        config = load_config()
        config.enabled = True
        save_config(config)
        print("Claude Talk enabled.")
    elif command == "disable":
        from claude_talk.config import load_config, save_config
        config = load_config()
        config.enabled = False
        save_config(config)
        print("Claude Talk disabled.")
    elif command == "voice":
        voice_command()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

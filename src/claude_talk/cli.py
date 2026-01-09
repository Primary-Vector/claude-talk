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


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: claude-talk <command>", file=sys.stderr)
        print("Commands: speak, setup", file=sys.stderr)
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
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

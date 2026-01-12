"""CLI for Claude Talk."""

import json
import hashlib
import os
import sys
from pathlib import Path

from claude_talk.config import load_config, DEFAULT_CONFIG_PATH
from claude_talk.filter import filter_text
from claude_talk.tts import KokoroTTS

# State directory for tracking spoken content and PIDs
STATE_DIR = Path.home() / ".cache" / "claude-talk"
PID_FILE = STATE_DIR / "tts.pid"
LAST_SPEAK_FILE = STATE_DIR / "last_speak.timestamp"
DEBOUNCE_SECONDS = 0.5  # Ignore speak requests within this window


def get_state_file(session_id: str) -> Path:
    """Get the state file path for a session."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR / f"{session_id}.spoken"


def get_spoken_hash(session_id: str) -> str | None:
    """Get the hash of last spoken content for this session."""
    state_file = get_state_file(session_id)
    if state_file.exists():
        return state_file.read_text().strip()
    return None


def set_spoken_hash(session_id: str, content_hash: str) -> None:
    """Record what we've spoken."""
    state_file = get_state_file(session_id)
    state_file.write_text(content_hash)


def should_debounce() -> bool:
    """Check if we should skip this speak request due to recent activity."""
    import time

    STATE_DIR.mkdir(parents=True, exist_ok=True)

    if LAST_SPEAK_FILE.exists():
        try:
            last_timestamp = float(LAST_SPEAK_FILE.read_text().strip())
            time_since_last = time.time() - last_timestamp
            return time_since_last < DEBOUNCE_SECONDS
        except (ValueError, OSError):
            pass

    return False


def update_speak_timestamp() -> None:
    """Record the current time as the last speak attempt."""
    import time

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LAST_SPEAK_FILE.write_text(str(time.time()))


def get_assistant_text_from_transcript(transcript_path: str) -> str | None:
    """Read all assistant text from the current response in transcript."""
    path = Path(transcript_path).expanduser()
    if not path.exists():
        return None

    # Find text from the last assistant message(s) after the last user message
    all_text = []
    in_current_response = False

    with open(path, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                msg_type = entry.get("type")

                if msg_type == "user":
                    # New user message, reset
                    all_text = []
                    in_current_response = True
                elif msg_type == "assistant" and in_current_response:
                    # Extract text blocks from assistant message
                    message = entry.get("message", {})
                    content = message.get("content", [])
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text", "").strip()
                            if text:
                                all_text.append(text)
                        elif isinstance(block, str):
                            if block.strip():
                                all_text.append(block.strip())
            except json.JSONDecodeError:
                continue

    return " ".join(all_text) if all_text else None


def kill_existing_playback() -> None:
    """Kill any existing TTS playback."""
    import signal

    STATE_DIR.mkdir(parents=True, exist_ok=True)

    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            os.kill(old_pid, signal.SIGTERM)
        except (ValueError, ProcessLookupError, PermissionError):
            pass  # Process already gone or invalid PID
        PID_FILE.unlink(missing_ok=True)


def speak_async(text: str, voice: str) -> None:
    """Speak text in a background subprocess (fire and forget)."""
    import subprocess

    # Debounce rapid requests to prevent overlapping playback
    if should_debounce():
        return

    # Kill any existing playback first
    kill_existing_playback()

    # Update timestamp to prevent rapid subsequent calls
    update_speak_timestamp()

    # Get the path to this module's directory
    module_dir = Path(__file__).parent.parent.parent

    # Spawn a detached subprocess to do the speaking
    proc = subprocess.Popen(
        [
            sys.executable,
            "-c",
            f'''
import sys
sys.path.insert(0, "{module_dir / 'src'}")
from claude_talk.tts import KokoroTTS
tts = KokoroTTS()
tts.speak({repr(text)}, voice={repr(voice)})
'''
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    # Save PID so we can kill it later if needed
    PID_FILE.write_text(str(proc.pid))


def speak_new_content(transcript_path: str, session_id: str, config) -> None:
    """Speak any new content that hasn't been spoken yet."""
    text = get_assistant_text_from_transcript(transcript_path)
    if not text:
        return

    # Check if we've already spoken this exact content
    content_hash = hashlib.md5(text.encode()).hexdigest()
    if get_spoken_hash(session_id) == content_hash:
        return  # Already spoken this

    filtered = filter_text(text, max_chars=config.max_chars)
    if not filtered.strip():
        return

    # Record that we spoke this (before speaking, to avoid race conditions)
    set_spoken_hash(session_id, content_hash)

    # Speak it async
    speak_async(filtered, config.voice)


def speak_command() -> None:
    """Read hook input and speak assistant response."""
    config = load_config(DEFAULT_CONFIG_PATH)

    if not config.enabled:
        return

    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    hook_event = hook_input.get("hook_event_name", "")
    session_id = hook_input.get("session_id", "default")

    # Handle UserPromptSubmit - speak the user's prompt
    if hook_event == "UserPromptSubmit":
        prompt = hook_input.get("prompt", "")
        if prompt:
            filtered = filter_text(prompt, max_chars=config.max_chars)
            if filtered.strip():
                speak_async(filtered, config.voice)
        return

    # Handle PreToolUse and Stop - speak from transcript
    transcript_path = hook_input.get("transcript_path")
    if not transcript_path:
        return

    speak_new_content(transcript_path, session_id, config)


def voice_command() -> None:
    """Interactive voice selection."""
    from claude_talk.config import load_config, save_config
    from claude_talk.voices import list_voices

    config = load_config()
    tts = KokoroTTS()
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
        print("Commands: speak, stop, setup, enable, disable, voice, sample, set-voice, current-voice, install-hook", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "speak":
        speak_command()
    elif command == "stop":
        kill_existing_playback()
        print("Stopped.")
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
    elif command == "sample":
        # Play a sample for a specific voice
        if len(sys.argv) < 3:
            print("Usage: claude-talk sample <voice_id>", file=sys.stderr)
            sys.exit(1)
        voice_id = sys.argv[2]
        from claude_talk.voices import VOICES
        if voice_id not in VOICES:
            print(f"Unknown voice: {voice_id}", file=sys.stderr)
            sys.exit(1)
        tts = KokoroTTS()
        tts.speak(VOICES[voice_id]["joke"], voice=voice_id)
    elif command == "set-voice":
        # Set the voice in config
        if len(sys.argv) < 3:
            print("Usage: claude-talk set-voice <voice_id>", file=sys.stderr)
            sys.exit(1)
        voice_id = sys.argv[2]
        from claude_talk.voices import VOICES
        from claude_talk.config import load_config, save_config, Config
        if voice_id not in VOICES:
            print(f"Unknown voice: {voice_id}", file=sys.stderr)
            sys.exit(1)
        try:
            config = load_config()
        except FileNotFoundError:
            config = Config(enabled=True, voice=voice_id, max_chars=500)
        config.voice = voice_id
        save_config(config)
        print(f"Voice set to {voice_id}")
    elif command == "current-voice":
        # Print current voice
        from claude_talk.config import load_config
        try:
            config = load_config()
            print(f"Current voice: {config.voice}")
        except FileNotFoundError:
            print("No voice configured yet. Run /talk:setup first.")
    elif command == "install-hook":
        # Install the Claude Code hooks
        from claude_talk.setup import install_hook
        install_hook()
        print("Hooks installed.")
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

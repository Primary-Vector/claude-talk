"""Voice presets and sample jokes for Claude Talk."""

VOICES = {
    "v2/en_speaker_6": {
        "name": "Speaker 6 (Neutral)",
        "joke": "Why do programmers prefer dark mode? Because light attracts bugs.",
    },
    "v2/en_speaker_3": {
        "name": "Speaker 3 (Warm)",
        "joke": "There are only 10 kinds of people. Those who understand binary, and those who don't.",
    },
    "v2/en_speaker_9": {
        "name": "Speaker 9 (Clear)",
        "joke": "A SQL query walks into a bar, sees two tables, and asks... can I join you?",
    },
    "v2/en_speaker_0": {
        "name": "Speaker 0 (Calm)",
        "joke": "Why do Java developers wear glasses? Because they can't C sharp.",
    },
}


def get_voice_sample(index: int) -> tuple[str, dict]:
    """Get voice by index for selection UI."""
    voice_ids = list(VOICES.keys())
    voice_id = voice_ids[index % len(voice_ids)]
    return voice_id, VOICES[voice_id]


def list_voices() -> list[tuple[str, dict]]:
    """List all available voices."""
    return list(VOICES.items())

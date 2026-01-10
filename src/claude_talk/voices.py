"""Voice presets and sample jokes for Claude Talk."""

# Ordered: Female, Male, Female, Male
VOICES = {
    "af_heart": {
        "name": "Heart (Female, Warm)",
        "joke": "Why do programmers prefer dark mode? Because light attracts bugs.",
    },
    "am_michael": {
        "name": "Michael (Male, Professional)",
        "joke": "There are only 10 kinds of people. Those who understand binary, and those who don't.",
    },
    "af_bella": {
        "name": "Bella (Female, Expressive)",
        "joke": "A SQL query walks into a bar, sees two tables, and asks... can I join you?",
    },
    "am_fenrir": {
        "name": "Fenrir (Male, Deep)",
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

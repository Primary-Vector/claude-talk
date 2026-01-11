"""Voice presets and sample jokes for Claude Talk."""

# Diverse selection: American and British, Female and Male
VOICES = {
    # American Female
    "af_heart": {
        "name": "Heart (American Female, Warm)",
        "joke": "Why do programmers prefer dark mode? Because light attracts bugs.",
    },
    "af_bella": {
        "name": "Bella (American Female, Expressive)",
        "joke": "A SQL query walks into a bar, sees two tables, and asks... can I join you?",
    },
    "af_nicole": {
        "name": "Nicole (American Female, Clear)",
        "joke": "Why did the developer go broke? Because he used up all his cache.",
    },
    "af_sky": {
        "name": "Sky (American Female, Bright)",
        "joke": "I told my computer I needed a break. Now it won't stop sending me vacation ads.",
    },
    # American Male
    "am_michael": {
        "name": "Michael (American Male, Professional)",
        "joke": "There are only 10 kinds of people. Those who understand binary, and those who don't.",
    },
    "am_adam": {
        "name": "Adam (American Male, Friendly)",
        "joke": "Why do Java developers wear glasses? Because they can't C sharp.",
    },
    # British Female
    "bf_emma": {
        "name": "Emma (British Female, Elegant)",
        "joke": "Programming is like cooking. Sometimes you follow the recipe, sometimes you just throw things together and hope for the best.",
    },
    "bf_isabella": {
        "name": "Isabella (British Female, Refined)",
        "joke": "A programmer's wife tells him: Go to the store and buy a loaf of bread. If they have eggs, buy a dozen. He comes home with twelve loaves.",
    },
    # British Male
    "bm_george": {
        "name": "George (British Male, Distinguished)",
        "joke": "There's no place like 127.0.0.1.",
    },
    "bm_lewis": {
        "name": "Lewis (British Male, Thoughtful)",
        "joke": "The best thing about a Boolean is that even if you're wrong, you're only off by a bit.",
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

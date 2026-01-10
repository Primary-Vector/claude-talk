from claude_talk.voices import VOICES, get_voice_sample


def test_voices_has_entries():
    assert len(VOICES) >= 3


def test_each_voice_has_required_fields():
    for voice_id, voice in VOICES.items():
        assert "name" in voice
        assert "joke" in voice
        # Kokoro voice IDs like "af_heart", "am_michael"
        assert "_" in voice_id


def test_get_voice_sample():
    voice_id, voice = get_voice_sample(0)
    assert "_" in voice_id  # Kokoro voice ID format
    assert "joke" in voice

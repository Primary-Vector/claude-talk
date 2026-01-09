from claude_talk.voices import VOICES, get_voice_sample


def test_voices_has_entries():
    assert len(VOICES) >= 3


def test_each_voice_has_required_fields():
    for voice_id, voice in VOICES.items():
        assert "name" in voice
        assert "joke" in voice
        assert voice_id.startswith("v2/")


def test_get_voice_sample():
    voice_id, voice = get_voice_sample(0)
    assert voice_id.startswith("v2/")
    assert "joke" in voice

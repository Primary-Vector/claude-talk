import numpy as np
from unittest.mock import patch, MagicMock

from claude_talk.tts import BarkTTS, setup_models


def test_bark_tts_init():
    with patch("claude_talk.tts.preload_models"):
        tts = BarkTTS(model_size="small")
        assert tts.model_size == "small"


def test_bark_tts_synthesize_returns_audio():
    with patch("claude_talk.tts.generate_audio") as mock_gen:
        mock_gen.return_value = np.zeros(24000, dtype=np.float32)
        with patch("claude_talk.tts.preload_models"):
            tts = BarkTTS(model_size="small")
            audio = tts.synthesize("Hello world", voice="v2/en_speaker_6")
            assert isinstance(audio, np.ndarray)
            mock_gen.assert_called_once()


def test_setup_models_sets_env_for_small():
    with patch("claude_talk.tts.preload_models") as mock_preload:
        with patch.dict("os.environ", {}, clear=True):
            import os
            setup_models("small")
            assert os.environ.get("SUNO_USE_SMALL_MODELS") == "True"
            mock_preload.assert_called_once()


def test_setup_models_unsets_env_for_large():
    with patch("claude_talk.tts.preload_models") as mock_preload:
        with patch.dict("os.environ", {"SUNO_USE_SMALL_MODELS": "True"}):
            import os
            setup_models("large")
            assert os.environ.get("SUNO_USE_SMALL_MODELS") != "True"
            mock_preload.assert_called_once()


def test_bark_tts_speak_plays_audio():
    with patch("claude_talk.tts.generate_audio") as mock_gen:
        with patch("claude_talk.tts.sd") as mock_sd:
            with patch("claude_talk.tts.preload_models"):
                mock_gen.return_value = np.zeros(24000, dtype=np.float32)
                tts = BarkTTS(model_size="small")
                tts.speak("Hello", voice="v2/en_speaker_6")
                mock_sd.play.assert_called_once()
                mock_sd.wait.assert_called_once()

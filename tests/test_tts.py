import numpy as np
from unittest.mock import patch, MagicMock
from pathlib import Path

from claude_talk.tts import KokoroTTS, setup_models, download_models, MODEL_PATH, VOICES_PATH


def test_kokoro_tts_init():
    tts = KokoroTTS()
    assert tts._kokoro is None  # Lazy loading


def test_kokoro_tts_synthesize_returns_audio():
    mock_kokoro = MagicMock()
    mock_kokoro.create.return_value = (np.zeros(24000, dtype=np.float32), 24000)

    with patch("claude_talk.tts.Kokoro", return_value=mock_kokoro):
        tts = KokoroTTS()
        samples, rate = tts.synthesize("Hello world", voice="af_heart")
        assert isinstance(samples, np.ndarray)
        assert rate == 24000
        mock_kokoro.create.assert_called_once()


def test_kokoro_tts_speak_plays_audio():
    mock_kokoro = MagicMock()
    mock_kokoro.create.return_value = (np.zeros(24000, dtype=np.float32), 24000)

    with patch("claude_talk.tts.Kokoro", return_value=mock_kokoro):
        with patch("claude_talk.tts.sd") as mock_sd:
            tts = KokoroTTS()
            tts.speak("Hello", voice="af_heart")
            mock_sd.play.assert_called_once()
            mock_sd.wait.assert_called_once()


def test_setup_models_verifies_files_exist(tmp_path):
    # Create fake model files
    model_file = tmp_path / "kokoro-v1.0.onnx"
    voices_file = tmp_path / "voices-v1.0.bin"
    model_file.write_text("fake model")
    voices_file.write_text("fake voices")

    mock_kokoro = MagicMock()
    mock_kokoro.create.return_value = (np.zeros(100), 24000)

    with patch("claude_talk.tts.MODEL_PATH", model_file):
        with patch("claude_talk.tts.VOICES_PATH", voices_file):
            with patch("claude_talk.tts.Kokoro", return_value=mock_kokoro):
                # Should not raise
                setup_models()


def test_download_models_calls_curl_when_missing(tmp_path):
    """Test that download_models calls curl when models are missing."""
    missing_model = tmp_path / "models" / "kokoro-v1.0.onnx"
    missing_voices = tmp_path / "models" / "voices-v1.0.bin"
    models_dir = tmp_path / "models"

    with patch("claude_talk.tts.MODEL_PATH", missing_model):
        with patch("claude_talk.tts.VOICES_PATH", missing_voices):
            with patch("claude_talk.tts.MODELS_DIR", models_dir):
                with patch("claude_talk.tts.subprocess.run") as mock_run:
                    download_models()
                    # Should call curl twice (model and voices)
                    assert mock_run.call_count == 2


def test_download_models_skips_if_exists(tmp_path):
    """Test that download_models skips download if models exist."""
    model_file = tmp_path / "kokoro-v1.0.onnx"
    voices_file = tmp_path / "voices-v1.0.bin"
    model_file.write_text("fake model")
    voices_file.write_text("fake voices")

    with patch("claude_talk.tts.MODEL_PATH", model_file):
        with patch("claude_talk.tts.VOICES_PATH", voices_file):
            with patch("claude_talk.tts.subprocess.run") as mock_run:
                download_models()
                # Should not call curl if files exist
                mock_run.assert_not_called()

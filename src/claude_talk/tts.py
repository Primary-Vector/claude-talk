"""Kokoro ONNX TTS wrapper for Claude Talk."""

from pathlib import Path
import sounddevice as sd
from kokoro_onnx import Kokoro

# Models directory relative to plugin root
PLUGIN_ROOT = Path(__file__).parent.parent.parent
MODELS_DIR = PLUGIN_ROOT / "models"
MODEL_PATH = MODELS_DIR / "kokoro-v1.0.onnx"
VOICES_PATH = MODELS_DIR / "voices-v1.0.bin"

SAMPLE_RATE = 24000


class KokoroTTS:
    """Kokoro ONNX TTS synthesizer."""

    def __init__(self):
        """Initialize Kokoro TTS."""
        self._kokoro = None

    @property
    def kokoro(self) -> Kokoro:
        """Lazy-load the Kokoro model."""
        if self._kokoro is None:
            self._kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))
        return self._kokoro

    def synthesize(self, text: str, voice: str = "af_heart") -> tuple:
        """Synthesize text to audio array."""
        samples, sample_rate = self.kokoro.create(
            text,
            voice=voice,
            speed=1.0,
            lang="en-us"
        )
        return samples, sample_rate

    def speak(self, text: str, voice: str = "af_heart") -> None:
        """Synthesize and play audio."""
        samples, sample_rate = self.synthesize(text, voice)
        sd.play(samples, samplerate=sample_rate)
        sd.wait()


def setup_models() -> None:
    """Verify models are downloaded."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run /claude-talk:setup to download models."
        )
    if not VOICES_PATH.exists():
        raise FileNotFoundError(
            f"Voices file not found at {VOICES_PATH}. "
            "Run /claude-talk:setup to download models."
        )
    # Quick test to verify models load
    kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))
    # Generate tiny sample to verify
    kokoro.create("test", voice="af_heart", speed=1.0, lang="en-us")

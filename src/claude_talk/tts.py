"""Kokoro ONNX TTS wrapper for Claude Talk."""

from pathlib import Path
import subprocess
import sys
import sounddevice as sd
from kokoro_onnx import Kokoro

# Models directory relative to plugin root
PLUGIN_ROOT = Path(__file__).parent.parent.parent
MODELS_DIR = PLUGIN_ROOT / "models"
MODEL_PATH = MODELS_DIR / "kokoro-v1.0.onnx"
VOICES_PATH = MODELS_DIR / "voices-v1.0.bin"

MODEL_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"

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


def download_models() -> None:
    """Download Kokoro ONNX models if not present."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if not MODEL_PATH.exists():
        print(f"Downloading kokoro-v1.0.onnx (~310MB)...")
        subprocess.run(
            ["curl", "-L", "-o", str(MODEL_PATH), MODEL_URL],
            check=True
        )
        print("Model downloaded.")

    if not VOICES_PATH.exists():
        print(f"Downloading voices-v1.0.bin (~27MB)...")
        subprocess.run(
            ["curl", "-L", "-o", str(VOICES_PATH), VOICES_URL],
            check=True
        )
        print("Voices downloaded.")


def setup_models() -> None:
    """Download and verify models."""
    download_models()

    # Quick test to verify models load
    print("Verifying models...")
    kokoro = Kokoro(str(MODEL_PATH), str(VOICES_PATH))
    kokoro.create("test", voice="af_heart", speed=1.0, lang="en-us")
    print("Models verified!")

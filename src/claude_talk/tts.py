"""Bark TTS wrapper for Claude Talk."""

import os
import numpy as np
import sounddevice as sd

from bark import SAMPLE_RATE, generate_audio, preload_models


def setup_models(model_size: str = "small") -> None:
    """Download and load Bark models."""
    if model_size == "small":
        os.environ["SUNO_USE_SMALL_MODELS"] = "True"
    else:
        os.environ.pop("SUNO_USE_SMALL_MODELS", None)

    preload_models()


class BarkTTS:
    """Bark TTS synthesizer."""

    def __init__(self, model_size: str = "small"):
        self.model_size = model_size
        setup_models(model_size)

    def synthesize(self, text: str, voice: str = "v2/en_speaker_6") -> np.ndarray:
        """Synthesize text to audio array."""
        audio = generate_audio(text, history_prompt=voice)
        return audio

    def speak(self, text: str, voice: str = "v2/en_speaker_6") -> None:
        """Synthesize and play audio."""
        audio = self.synthesize(text, voice)
        sd.play(audio, samplerate=SAMPLE_RATE)
        sd.wait()

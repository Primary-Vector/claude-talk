"""Configuration management for Claude Talk."""

from dataclasses import dataclass
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "claude-talk" / "config.toml"


@dataclass
class Config:
    """Claude Talk configuration."""

    enabled: bool = True
    voice: str = "af_heart"
    max_chars: int = 500


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Config:
    """Load config from TOML file, returning defaults if not found."""
    if not path.exists():
        return Config()

    with open(path, "rb") as f:
        data = tomllib.load(f)

    return Config(
        enabled=data.get("enabled", True),
        voice=data.get("voice", "af_heart"),
        max_chars=data.get("max_chars", 500),
    )


def save_config(config: Config, path: Path = DEFAULT_CONFIG_PATH) -> None:
    """Save config to TOML file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    content = f'''enabled = {str(config.enabled).lower()}
voice = "{config.voice}"
max_chars = {config.max_chars}
'''
    path.write_text(content)

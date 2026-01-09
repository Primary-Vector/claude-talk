#!/usr/bin/env python3
"""Entry point for Claude Talk - runs from plugin directory."""

import sys
from pathlib import Path

# Add src to path so we can import claude_talk
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from claude_talk.cli import main

if __name__ == "__main__":
    main()

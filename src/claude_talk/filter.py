"""Text filtering for Claude Talk - removes code, tables, and other non-conversational content."""

import re


def filter_text(text: str, max_chars: int = 500) -> str:
    """Filter out non-conversational content and truncate."""
    result = text

    # Remove fenced code blocks (``` ... ```)
    result = re.sub(r"```[\s\S]*?```", "", result)

    # Remove inline code (`...`)
    result = re.sub(r"`[^`]+`", "", result)

    # Remove markdown tables (lines starting with |)
    result = re.sub(r"^\|.*\|$", "", result, flags=re.MULTILINE)

    # Remove URLs (BEFORE file paths, since URLs contain paths)
    result = re.sub(r"https?://[^\s]+", "", result)

    # Remove file paths (Unix and Windows style)
    result = re.sub(r"(?:/[\w.-]+)+/?", "", result)
    result = re.sub(r"(?:[A-Za-z]:\\[\w\\.-]+)+", "", result)

    # Clean up multiple spaces/newlines
    result = re.sub(r"\n{3,}", "\n\n", result)
    result = re.sub(r" {2,}", " ", result)
    result = result.strip()

    # Truncate to max_chars
    if len(result) > max_chars:
        # Try to break at sentence boundary
        truncated = result[:max_chars]
        last_period = truncated.rfind(". ")
        if last_period > max_chars // 2:
            result = truncated[:last_period + 1]
        else:
            result = truncated.rsplit(" ", 1)[0] + "..."

    return result

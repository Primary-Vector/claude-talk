"""Text filtering for Claude Talk - removes code, tables, and other non-conversational content."""

import re


def filter_text(text: str, max_chars: int = 500) -> str:
    """Filter out non-conversational content and truncate."""
    result = text

    # Remove fenced code blocks (``` ... ```)
    result = re.sub(r"```[\s\S]*?```", "", result)

    # Remove backticks but keep the content inside
    result = re.sub(r"`([^`]+)`", r"\1", result)

    # Remove markdown tables (lines starting with |)
    result = re.sub(r"^\|.*\|$", "", result, flags=re.MULTILINE)

    # Convert periods without surrounding whitespace to " dot " (for filenames, code identifiers)
    # e.g., "SignupView.swift" -> "SignupView dot swift"
    result = re.sub(r"(\S)\.(\S)", r"\1 dot \2", result)

    # Remove URLs (BEFORE file paths, since URLs contain paths)
    result = re.sub(r"https?://[^\s]+", "", result)

    # Remove file paths (Unix and Windows style)
    result = re.sub(r"(?:/[\w.-]+)+/?", "", result)
    result = re.sub(r"(?:[A-Za-z]:\\[\w\\.-]+)+", "", result)

    # Remove markdown formatting
    result = re.sub(r"\*\*([^*]+)\*\*", r"\1", result)  # **bold**
    result = re.sub(r"__([^_]+)__", r"\1", result)      # __bold__
    result = re.sub(r"\*([^*]+)\*", r"\1", result)      # *italic*
    result = re.sub(r"_([^_]+)_", r"\1", result)        # _italic_
    result = re.sub(r"^#{1,6}\s*", "", result, flags=re.MULTILINE)  # # headers
    result = re.sub(r"^\s*[-*]\s+", "", result, flags=re.MULTILINE)  # - bullets (keep numbered lists)

    # Add pause for dashes (replace " - " with comma pause)
    result = re.sub(r" - ", ", ", result)

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

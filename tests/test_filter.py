from claude_talk.filter import filter_text


def test_removes_fenced_code_blocks():
    text = """Here's the code:

```python
def hello():
    print("world")
```

That should work."""
    result = filter_text(text)
    assert "def hello" not in result
    assert "Here's the code:" in result
    assert "That should work." in result


def test_removes_inline_code_backticks():
    text = "Use the `print()` function to output text."
    result = filter_text(text)
    assert "`" not in result  # Backticks removed
    assert "print()" in result  # Content kept
    assert "Use the" in result


def test_removes_markdown_tables():
    text = """Here's a table:

| Name | Age |
|------|-----|
| Bob  | 30  |

And some more text."""
    result = filter_text(text)
    assert "| Name |" not in result
    assert "Here's a table:" in result
    assert "And some more text." in result


def test_removes_file_paths():
    text = "Check the file at /Users/pv/git/project/src/main.py for details."
    result = filter_text(text)
    assert "/Users/pv/git" not in result


def test_removes_urls():
    text = "Visit https://example.com/page for more info."
    result = filter_text(text)
    assert "https://example.com" not in result


def test_truncates_to_max_chars():
    text = "Hello world. " * 100  # ~1300 chars
    result = filter_text(text, max_chars=100)
    assert len(result) <= 100


def test_preserves_conversational_text():
    text = "I'd be happy to help you with that! Let me explain how it works."
    result = filter_text(text)
    assert result.strip() == text


def test_empty_after_filtering_returns_empty():
    text = "```python\nprint('hello')\n```"
    result = filter_text(text)
    assert result.strip() == ""

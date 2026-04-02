"""Encoding related utilities."""

def CEscape(text: bytes, as_utf8: bool) -> str:
    """
    Escape a bytes string for use in an text protocol buffer.

    Args:
      text: A byte string to be escaped.
      as_utf8: Specifies if result may contain non-ASCII characters.
          In Python 3 this allows unescaped non-ASCII Unicode characters.
          In Python 2 the return value will be valid UTF-8 rather than only ASCII.
    Returns:
      Escaped string (str).
    """
    ...
def CUnescape(text: str) -> bytes:
    """
    Unescape a text string with C-style escape sequences to UTF-8 bytes.

    Args:
      text: The data to parse in a str.
    Returns:
      A byte string.
    """
    ...

"""
Deprecated fastText language detection module.

This module is deprecated as the fastText library is archived and unmaintained.
Please use langdetect instead.
"""

def detect_languages(text: str, confidence_threshold: float) -> list[str]:
    """
    Deprecated function. FastText support has been removed.

    Args:
        text: The text to detect languages from (unused)
        confidence_threshold: Minimum confidence threshold (unused)

    Raises:
        ImportError: Always, as fastText is no longer supported.
    """
    ...

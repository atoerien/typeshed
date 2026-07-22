"""
Convert a NT pathname to a file URL and vice versa.

This module only exists to provide OS-specific code
for urllib.requests, thus do not use directly.
"""

from typing_extensions import deprecated

@deprecated("Deprecated; use `urllib.request` file-URL helpers instead.")
def url2pathname(url: str) -> str: ...
@deprecated("Deprecated; use `urllib.request` file-URL helpers instead.")
def pathname2url(p: str) -> str: ...

"""
pygments.modeline
~~~~~~~~~~~~~~~~~

A simple modeline parser (based on pymodeline).

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

__all__ = ["get_filetype_from_buffer"]

def get_filetype_from_buffer(buf: str, max_lines: int = 5) -> str | None:
    """Scan the buffer for modelines and return filetype if one is found."""
    ...

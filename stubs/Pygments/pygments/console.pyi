"""
pygments.console
~~~~~~~~~~~~~~~~

Format colored console output.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from typing import Final

esc: Final = "\x1b["
codes: Final[dict[str, str]]
dark_colors: Final[list[str]]
light_colors: Final[list[str]]

def reset_color() -> str: ...
def colorize(color_key: str, text: str) -> str: ...
def ansiformat(attr: str, text: str) -> str:
    """
    Format ``text`` with a color and/or some attributes::

        color       normal color
        *color*     bold color
        _color_     underlined color
        +color+     blinking color
    """
    ...

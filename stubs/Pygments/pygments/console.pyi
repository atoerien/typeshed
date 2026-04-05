"""
pygments.console
~~~~~~~~~~~~~~~~

Format colored console output.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete

esc: str
codes: Incomplete
dark_colors: Incomplete
light_colors: Incomplete

def reset_color(): ...
def colorize(color_key, text): ...
def ansiformat(attr, text):
    """
    Format ``text`` with a color and/or some attributes::

        color       normal color
        *color*     bold color
        _color_     underlined color
        +color+     blinking color
    """
    ...

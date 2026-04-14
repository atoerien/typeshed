from collections.abc import Iterable
from re import Pattern

from .ast import Node

def parse_nth(input: str | Iterable[Node]) -> tuple[int, int] | None:
    """
    Parse `<An+B> <https://drafts.csswg.org/css-syntax-3/#anb>`_,
    as found in `:nth-child()
    <https://drafts.csswg.org/selectors/#nth-child-pseudo>`_
    and related Selector pseudo-classes.

    Although tinycss2 does not include a full Selector parser,
    this bit of syntax is included as it is particularly tricky to define
    on top of a CSS tokenizer.

    :type input: :obj:`str` or :term:`iterable`
    :param input: A string or an iterable of :term:`component values`.
    :returns:
        A ``(a, b)`` tuple of integers, or :obj:`None` if the input is invalid.
    """
    ...
def parse_b(tokens: Iterable[Node], a: int) -> tuple[int, int] | None: ...
def parse_signless_b(tokens: Iterable[Node], a: int, b_sign: int) -> tuple[int, int] | None: ...
def parse_end(tokens: Iterable[Node], a: int, b: int) -> tuple[int, int] | None: ...

N_DASH_DIGITS_RE: Pattern[str]

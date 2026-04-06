"""
pygments.lexer
~~~~~~~~~~~~~~

Base lexer classes.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete
from collections.abc import Iterable, Iterator, Sequence
from re import Pattern, RegexFlag
from typing import ClassVar, Final

from pygments.token import _TokenType
from pygments.util import Future

__all__ = [
    "Lexer",
    "RegexLexer",
    "ExtendedRegexLexer",
    "DelegatingLexer",
    "LexerContext",
    "include",
    "inherit",
    "bygroups",
    "using",
    "this",
    "default",
    "words",
    "line_re",
]

line_re: Final[Pattern[str]]

class LexerMeta(type):
    """
    This metaclass automagically converts ``analyse_text`` methods into
    static methods which always return float values.
    """
    def __new__(cls, name, bases, d): ...

class Lexer(metaclass=LexerMeta):
    name: ClassVar[str]  # Set to None, but always overridden with a non-None value in subclasses.
    aliases: ClassVar[Sequence[str]]  # not intended to be mutable
    filenames: ClassVar[Sequence[str]]
    alias_filenames: ClassVar[Sequence[str]]
    mimetypes: ClassVar[Sequence[str]]
    priority: ClassVar[float]
    url: ClassVar[str]  # Set to None, but always overridden with a non-None value in subclasses.
    version_added: ClassVar[str]  # Set to None, but always overridden with a non-None value in subclasses.
    options: Incomplete
    stripnl: Incomplete
    stripall: Incomplete
    ensurenl: Incomplete
    tabsize: Incomplete
    encoding: Incomplete
    filters: Incomplete
    def __init__(self, **options) -> None: ...
    def add_filter(self, filter_, **options) -> None: ...
    @staticmethod  # @staticmethod added by special handling in metaclass
    def analyse_text(text: str) -> float: ...
    def get_tokens(self, text: str, unfiltered: bool = False) -> Iterator[tuple[_TokenType, str]]: ...
    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...

class DelegatingLexer(Lexer):
    """
    This lexer takes two lexer as arguments. A root lexer and
    a language lexer. First everything is scanned using the language
    lexer, afterwards all ``Other`` tokens are lexed using the root
    lexer.

    The lexers from the ``template`` lexer package use this base lexer.
    """
    root_lexer: Incomplete
    language_lexer: Incomplete
    needle: Incomplete
    def __init__(self, _root_lexer, _language_lexer, _needle=..., **options) -> None: ...
    def get_tokens_unprocessed(self, text: str) -> Iterator[tuple[int, _TokenType, str]]: ...

class include(str):
    """Indicates that a state should include rules from another state."""
    ...
class _inherit:
    """Indicates the a state should inherit from its superclass."""
    ...

inherit: Incomplete

class combined(tuple[Incomplete, ...]):
    """Indicates a state combined from multiple states."""
    def __new__(cls, *args): ...
    def __init__(self, *args) -> None: ...

class _PseudoMatch:
    """A pseudo match object constructed from a string."""
    def __init__(self, start, text) -> None: ...
    def start(self, arg=None): ...
    def end(self, arg=None): ...
    def group(self, arg=None): ...
    def groups(self): ...
    def groupdict(self): ...

def bygroups(*args):
    """Callback that yields multiple actions for each group in the match."""
    ...

class _This:
    """
    Special singleton used for indicating the caller class.
    Used by ``using``.
    """
    ...

this: Incomplete

def using(_other, **kwargs):
    """
    Callback that processes the match with a different lexer.

    The keyword arguments are forwarded to the lexer, except `state` which
    is handled separately.

    `state` specifies the state that the new lexer will start in, and can
    be an enumerable such as ('root', 'inline', 'string') or a simple
    string which is assumed to be on top of the root state.

    Note: For that to work, `_other` must not be an `ExtendedRegexLexer`.
    """
    ...

class default:
    """
    Indicates a state or state action (e.g. #pop) to apply.
    For example default('#pop') is equivalent to ('', Token, '#pop')
    Note that state tuples may be used as well.

    .. versionadded:: 2.0
    """
    state: Incomplete
    def __init__(self, state) -> None: ...

class words(Future):
    """
    Indicates a list of literal words that is transformed into an optimized
    regex that matches any of the words.

    .. versionadded:: 2.0
    """
    words: Incomplete
    prefix: Incomplete
    suffix: Incomplete
    def __init__(self, words, prefix: str = "", suffix: str = "") -> None: ...
    def get(self): ...

class RegexLexerMeta(LexerMeta):
    """
    Metaclass for RegexLexer, creates the self._tokens attribute from
    self.tokens on the first instantiation.
    """
    def process_tokendef(cls, name, tokendefs=None):
        """Preprocess a dictionary of token definitions."""
        ...
    def get_tokendefs(cls):
        """
        Merge tokens from superclasses in MRO order, returning a single tokendef
        dictionary.

        Any state that is not defined by a subclass will be inherited
        automatically.  States that *are* defined by subclasses will, by
        default, override that state in the superclass.  If a subclass wishes to
        inherit definitions from a superclass, it can use the special value
        "inherit", which will cause the superclass' state definition to be
        included at that point in the state.
        """
        ...
    def __call__(cls, *args, **kwds):
        """Instantiate cls after preprocessing its token definitions."""
        ...

class RegexLexer(Lexer, metaclass=RegexLexerMeta):
    """
    Base for simple stateful regular expression-based lexers.
    Simplifies the lexing process so that you need only
    provide a list of states and regular expressions.
    """
    flags: ClassVar[RegexFlag]
    tokens: ClassVar[dict[str, list[Incomplete]]]
    def get_tokens_unprocessed(self, text: str, stack: Iterable[str] = ("root",)) -> Iterator[tuple[int, _TokenType, str]]:
        """
        Split ``text`` into (tokentype, text) pairs.

        ``stack`` is the initial stack (default: ``['root']``)
        """
        ...

class LexerContext:
    """A helper object that holds lexer position data."""
    text: Incomplete
    pos: Incomplete
    end: Incomplete
    stack: Incomplete
    def __init__(self, text, pos, stack=None, end=None) -> None: ...

class ExtendedRegexLexer(RegexLexer):
    """A RegexLexer that uses a context object to store its state."""
    def get_tokens_unprocessed(  # type: ignore[override]
        self, text: str | None = None, context: LexerContext | None = None
    ) -> Iterator[tuple[int, _TokenType, str]]:
        """
        Split ``text`` into (tokentype, text) pairs.
        If ``context`` is given, use this lexer context instead.
        """
        ...

class ProfilingRegexLexerMeta(RegexLexerMeta):
    """Metaclass for ProfilingRegexLexer, collects regex timing info."""
    ...

class ProfilingRegexLexer(RegexLexer, metaclass=ProfilingRegexLexerMeta):
    """Drop-in replacement for RegexLexer that does profiling of its regexes."""
    def get_tokens_unprocessed(self, text: str, stack: Iterable[str] = ("root",)) -> Iterator[tuple[int, _TokenType, str]]: ...

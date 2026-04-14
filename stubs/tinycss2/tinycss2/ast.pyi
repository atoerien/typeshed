"""Data structures for the CSS abstract syntax tree."""

from typing import Literal

class Node:
    """
    Every node type inherits from this class,
    which is never instantiated directly.

    .. attribute:: type

        Each child class has a :attr:`type` class attribute
        with a unique string value.
        This allows checking for the node type with code like:

        .. code-block:: python

            if node.type == 'whitespace':

        instead of the more verbose:

        .. code-block:: python

            from tinycss2.ast import WhitespaceToken
            if isinstance(node, WhitespaceToken):

    Every node also has these attributes and methods,
    which are not repeated for brevity:

    .. attribute:: source_line

        The line number of the start of the node in the CSS source.
        Starts at 1.

    .. attribute:: source_column

        The column number within :attr:`source_line` of the start of the node
        in the CSS source.
        Starts at 1.

    .. automethod:: serialize
    """
    source_line: int
    source_column: int
    type: str

    def __init__(self, source_line: int, source_column: int) -> None: ...
    def serialize(self) -> str:
        """Serialize this node to CSS syntax and return a Unicode string."""
        ...

class ParseError(Node):
    """
    A syntax error of some sort. May occur anywhere in the tree.

    Syntax errors are not fatal in the parser
    to allow for different error handling behaviors.
    For example, an error in a Selector list makes the whole rule invalid,
    but an error in a Media Query list only replaces one comma-separated query
    with ``not all``.

    .. autoattribute:: type

    .. attribute:: kind

        Machine-readable string indicating the type of error.
        Example: ``'bad-url'``.

    .. attribute:: message

        Human-readable explanation of the error, as a string.
        Could be translated, expanded to include details, etc.
    """
    type: Literal["error"]
    kind: str
    message: str
    repr_format: str
    def __init__(self, line: int, column: int, kind: str, message: str) -> None: ...

class Comment(Node):
    """
    A CSS comment.

    Comments can be ignored by passing ``skip_comments=True``
    to functions such as :func:`~tinycss2.parse_component_value_list`.

    .. autoattribute:: type

    .. attribute:: value

        The content of the comment, between ``/*`` and ``*/``, as a string.
    """
    type: Literal["comment"]
    value: str
    repr_format: str
    def __init__(self, line: int, column: int, value: str) -> None: ...

class WhitespaceToken(Node):
    """
    A :diagram:`whitespace-token`.

    .. autoattribute:: type

    .. attribute:: value

        The whitespace sequence, as a string, as in the original CSS source.
    """
    type: Literal["whitespace"]
    value: str
    repr_format: str
    def __init__(self, line: int, column: int, value: str) -> None: ...

class LiteralToken(Node):
    """
    Token that represents one or more characters as in the CSS source.

    .. autoattribute:: type

    .. attribute:: value

        A string of one to four characters.

    Instances compare equal to their :attr:`value`,
    so that these are equivalent:

    .. code-block:: python

        if node == ';':
        if node.type == 'literal' and node.value == ';':

    This regroups what `the specification`_ defines as separate token types:

    .. _the specification: https://drafts.csswg.org/css-syntax-3/

    * *<colon-token>* ``:``
    * *<semicolon-token>* ``;``
    * *<comma-token>* ``,``
    * *<cdc-token>* ``-->``
    * *<cdo-token>* ``<!--``
    * *<include-match-token>* ``~=``
    * *<dash-match-token>* ``|=``
    * *<prefix-match-token>* ``^=``
    * *<suffix-match-token>* ``$=``
    * *<substring-match-token>* ``*=``
    * *<column-token>* ``||``
    * *<delim-token>* (a single ASCII character not part of any another token)
    """
    type: Literal["literal"]
    value: str
    repr_format: str
    def __init__(self, line: int, column: int, value: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class IdentToken(Node):
    """
    An :diagram:`ident-token`.

    .. autoattribute:: type

    .. attribute:: value

        The unescaped value, as a Unicode string.

    .. attribute:: lower_value

        Same as :attr:`value` but normalized to *ASCII lower case*,
        see :func:`~webencodings.ascii_lower`.
        This is the value to use when comparing to a CSS keyword.
    """
    type: Literal["ident"]
    value: str
    lower_value: str
    repr_format: str
    def __init__(self, line: int, column: int, value: str) -> None: ...

class AtKeywordToken(Node):
    """
    An :diagram:`at-keyword-token`.

    .. code-block:: text

        '@' <value>

    .. autoattribute:: type

    .. attribute:: value

        The unescaped value, as a Unicode string, without the preceding ``@``.

    .. attribute:: lower_value

        Same as :attr:`value` but normalized to *ASCII lower case*,
        see :func:`~webencodings.ascii_lower`.
        This is the value to use when comparing to a CSS at-keyword.

        .. code-block:: python

            if node.type == 'at-keyword' and node.lower_value == 'import':
    """
    type: Literal["at-keyword"]
    value: str
    lower_value: str
    repr_format: str
    def __init__(self, line: int, column: int, value: str) -> None: ...

class HashToken(Node):
    """
    A :diagram:`hash-token`.

    .. code-block:: text

        '#' <value>

    .. autoattribute:: type

    .. attribute:: value

        The unescaped value, as a Unicode string, without the preceding ``#``.

    .. attribute:: is_identifier

        A boolean, true if the CSS source for this token
        was ``#`` followed by a valid identifier.
        (Only such hash tokens are valid ID selectors.)
    """
    type: Literal["hash"]
    value: str
    is_identifier: bool
    repr_format: str
    def __init__(self, line: int, column: int, value: str, is_identifier: bool) -> None: ...

class StringToken(Node):
    """
    A :diagram:`string-token`.

    .. code-block:: text

        '"' <value> '"'

    .. autoattribute:: type

    .. attribute:: value

        The unescaped value, as a Unicode string, without the quotes.
    """
    type: Literal["string"]
    value: str
    representation: str
    repr_format: str
    def __init__(self, line: int, column: int, value: str, representation: str) -> None: ...

class URLToken(Node):
    """
    An :diagram:`url-token`.

    .. code-block:: text

        'url(' <value> ')'

    .. autoattribute:: type

    .. attribute:: value

        The unescaped URL, as a Unicode string, without the ``url(`` and ``)``
        markers.
    """
    type: Literal["url"]
    value: str
    representation: str
    repr_format: str
    def __init__(self, line: int, column: int, value: str, representation: str) -> None: ...

class UnicodeRangeToken(Node):
    """
    A :diagram:`unicode-range-token`.

    .. autoattribute:: type

    .. attribute:: start

        The start of the range, as an integer between 0 and 1114111.

    .. attribute:: end

        The end of the range, as an integer between 0 and 1114111.
        Same as :attr:`start` if the source only specified one value.
    """
    type: Literal["unicode-range"]
    start: int
    end: int
    repr_format: str
    def __init__(self, line: int, column: int, start: int, end: int) -> None: ...

class NumberToken(Node):
    """
    A :diagram:`number-token`.

    .. autoattribute:: type

    .. attribute:: value

        The numeric value as a :class:`float`.

    .. attribute:: int_value

        The numeric value as an :class:`int`
        if :attr:`is_integer` is true, :obj:`None` otherwise.

    .. attribute:: is_integer

        Whether the token was syntactically an integer, as a boolean.

    .. attribute:: representation

        The CSS representation of the value, as a Unicode string.
    """
    type: Literal["number"]
    value: float
    int_value: int | None
    is_integer: bool
    representation: str
    repr_format: str
    def __init__(self, line: int, column: int, value: float, int_value: int | None, representation: str) -> None: ...

class PercentageToken(Node):
    """
    A :diagram:`percentage-token`.

    .. code-block:: text

        <representation> '%'

    .. autoattribute:: type

    .. attribute:: value

        The value numeric as a :class:`float`.

    .. attribute:: int_value

        The numeric value as an :class:`int`
        if the token was syntactically an integer,
        or :obj:`None`.

    .. attribute:: is_integer

        Whether the token’s value was syntactically an integer, as a boolean.

    .. attribute:: representation

        The CSS representation of the value without the unit,
        as a Unicode string.
    """
    type: Literal["percentage"]
    value: float
    int_value: int | None
    is_integer: bool
    representation: str
    repr_format: str
    def __init__(self, line: int, column: int, value: float, int_value: int | None, representation: str) -> None: ...

class DimensionToken(Node):
    """
    A :diagram:`dimension-token`.

    .. code-block:: text

        <representation> <unit>

    .. autoattribute:: type

    .. attribute:: value

        The value numeric as a :class:`float`.

    .. attribute:: int_value

        The numeric value as an :class:`int`
        if the token was syntactically an integer,
        or :obj:`None`.

    .. attribute:: is_integer

        Whether the token’s value was syntactically an integer, as a boolean.

    .. attribute:: representation

        The CSS representation of the value without the unit,
        as a Unicode string.

    .. attribute:: unit

        The unescaped unit, as a Unicode string.

    .. attribute:: lower_unit

        Same as :attr:`unit` but normalized to *ASCII lower case*,
        see :func:`~webencodings.ascii_lower`.
        This is the value to use when comparing to a CSS unit.

        .. code-block:: python

            if node.type == 'dimension' and node.lower_unit == 'px':
    """
    type: Literal["dimension"]
    value: float
    int_value: int | None
    is_integer: bool
    representation: str
    unit: str
    lower_unit: str
    repr_format: str
    def __init__(self, line: int, column: int, value: float, int_value: int | None, representation: str, unit: str) -> None: ...

class ParenthesesBlock(Node):
    """
    A :diagram:`()-block`.

    .. code-block:: text

        '(' <content> ')'

    .. autoattribute:: type

    .. attribute:: content

        The content of the block, as list of :term:`component values`.
        The ``(`` and ``)`` markers themselves are not represented in the list.
    """
    type: Literal["() block"]
    content: list[Node]
    repr_format: str
    def __init__(self, line: int, column: int, content: list[Node]) -> None: ...

class SquareBracketsBlock(Node):
    """
    A :diagram:`[]-block`.

    .. code-block:: text

        '[' <content> ']'

    .. autoattribute:: type

    .. attribute:: content

        The content of the block, as list of :term:`component values`.
        The ``[`` and ``]`` markers themselves are not represented in the list.
    """
    type: Literal["[] block"]
    content: list[Node]
    repr_format: str
    def __init__(self, line: int, column: int, content: list[Node]) -> None: ...

class CurlyBracketsBlock(Node):
    """
    A :diagram:`{}-block`.

    .. code-block:: text

        '{' <content> '}'

    .. autoattribute:: type

    .. attribute:: content

        The content of the block, as list of :term:`component values`.
        The ``[`` and ``]`` markers themselves are not represented in the list.
    """
    type: Literal["{} block"]
    content: list[Node]
    repr_format: str
    def __init__(self, line: int, column: int, content: list[Node]) -> None: ...

class FunctionBlock(Node):
    """
    A :diagram:`function-block`.

    .. code-block:: text

        <name> '(' <arguments> ')'

    .. autoattribute:: type

    .. attribute:: name

        The unescaped name of the function, as a Unicode string.

    .. attribute:: lower_name

        Same as :attr:`name` but normalized to *ASCII lower case*,
        see :func:`~webencodings.ascii_lower`.
        This is the value to use when comparing to a CSS function name.

    .. attribute:: arguments

        The arguments of the function, as list of :term:`component values`.
        The ``(`` and ``)`` markers themselves are not represented in the list.
        Commas are not special, but represented as :obj:`LiteralToken` objects
        in the list.
    """
    type: Literal["function"]
    name: str
    lower_name: str
    arguments: list[Node]
    repr_format: str
    def __init__(self, line: int, column: int, name: str, arguments: list[Node]) -> None: ...

class Declaration(Node):
    """
    A (property or descriptor) :diagram:`declaration`.

    .. code-block:: text

        <name> ':' <value>
        <name> ':' <value> '!important'

    .. autoattribute:: type

    .. attribute:: name

        The unescaped name, as a Unicode string.

    .. attribute:: lower_name

        Same as :attr:`name` but normalized to *ASCII lower case*,
        see :func:`~webencodings.ascii_lower`.
        This is the value to use when comparing to
        a CSS property or descriptor name.

        .. code-block:: python

            if node.type == 'declaration' and node.lower_name == 'color':

    .. attribute:: value

        The declaration value as a list of :term:`component values`:
        anything between ``:`` and
        the end of the declaration, or ``!important``.

    .. attribute:: important

        A boolean, true if the declaration had an ``!important`` marker.
        It is up to the consumer to reject declarations that do not accept
        this flag, such as non-property descriptor declarations.
    """
    type: Literal["declaration"]
    name: str
    lower_name: str
    value: list[Node]
    important: bool
    repr_format: str
    def __init__(self, line: int, column: int, name: str, lower_name: str, value: list[Node], important: bool) -> None: ...

class QualifiedRule(Node):
    """
    A :diagram:`qualified rule`.

    .. code-block:: text

        <prelude> '{' <content> '}'

    The interpretation of qualified rules depend on their context.
    At the top-level of a stylesheet
    or in a conditional rule such as ``@media``,
    they are **style rules** where the :attr:`prelude` is Selectors list
    and the :attr:`content` is a list of property declarations.

    .. autoattribute:: type

    .. attribute:: prelude

        The rule’s prelude, the part before the {} block,
        as a list of :term:`component values`.

    .. attribute:: content

        The rule’s content, the part inside the {} block,
        as a list of :term:`component values`.
    """
    type: Literal["qualified-rule"]
    prelude: list[Node]
    content: list[Node]
    repr_format: str
    def __init__(self, line: int, column: int, prelude: list[Node], content: list[Node]) -> None: ...

class AtRule(Node):
    """
    An :diagram:`at-rule`.

    .. code-block:: text

        @<at_keyword> <prelude> '{' <content> '}'
        @<at_keyword> <prelude> ';'

    The interpretation of at-rules depend on their at-keyword
    as well as their context.
    Most types of at-rules (ie. at-keyword values)
    are only allowed in some context,
    and must either end with a {} block or a semicolon.

    .. autoattribute:: type

    .. attribute:: at_keyword

        The unescaped value of the rule’s at-keyword,
        without the ``@`` symbol, as a Unicode string.

    .. attribute:: lower_at_keyword

        Same as :attr:`at_keyword` but normalized to *ASCII lower case*,
        see :func:`~webencodings.ascii_lower`.
        This is the value to use when comparing to a CSS at-keyword.

        .. code-block:: python

            if node.type == 'at-rule' and node.lower_at_keyword == 'import':

    .. attribute:: prelude

        The rule’s prelude, the part before the {} block or semicolon,
        as a list of :term:`component values`.

    .. attribute:: content

        The rule’s content, if any.
        The block’s content as a list of :term:`component values`
        for at-rules with a {} block,
        or :obj:`None` for at-rules ending with a semicolon.
    """
    type: Literal["at-rule"]
    at_keyword: str
    lower_at_keyword: str
    prelude: list[Node]
    content: list[Node] | None
    repr_format: str
    def __init__(
        self, line: int, column: int, at_keyword: str, lower_at_keyword: str, prelude: list[Node], content: list[Node] | None
    ) -> None: ...

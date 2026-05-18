from _typeshed import Incomplete
from collections.abc import Generator
from typing import Literal, overload

def htmlentityreplace_errors(exc: UnicodeError) -> tuple[str | bytes, int]: ...

@overload
def serialize(
    input,
    tree: Literal["dom", "genshi", "lxml", "etree"] = "etree",
    encoding: Literal[""] | None = None,
    *,
    quote_attr_values: Literal["legacy", "spec", "always"] = "legacy",
    quote_char: str = '"',
    use_best_quote_char: bool = ...,  # default value depends on whether quote_char was passed
    omit_optional_tags: bool = True,
    minimize_boolean_attributes: bool = True,
    use_trailing_solidus: bool = False,
    space_before_trailing_solidus: bool = True,
    escape_lt_in_attrs: bool = False,
    escape_rcdata: bool = False,
    resolve_entities: bool = True,
    alphabetical_attributes: bool = False,
    inject_meta_charset: bool = True,
    strip_whitespace: bool = False,
    sanitize: bool = False,
) -> str:
    """
    Serializes the input token stream using the specified treewalker

    :arg input: the token stream to serialize

    :arg tree: the treewalker to use

    :arg encoding: the encoding to use

    :arg serializer_opts: any options to pass to the
        :py:class:`html5lib.serializer.HTMLSerializer` that gets created

    :returns: the tree serialized as a string

    Example:

    >>> from html5lib.html5parser import parse
    >>> from html5lib.serializer import serialize
    >>> token_stream = parse('<html><body><p>Hi!</p></body></html>')
    >>> serialize(token_stream, omit_optional_tags=False)
    '<html><head></head><body><p>Hi!</p></body></html>'
    """
    ...
@overload
def serialize(
    input,
    tree: Literal["dom", "genshi", "lxml", "etree"] = "etree",
    encoding: str = ...,
    *,
    quote_attr_values: Literal["legacy", "spec", "always"] = "legacy",
    quote_char: str = '"',
    use_best_quote_char: bool = ...,  # default value depends on whether quote_char was passed
    omit_optional_tags: bool = True,
    minimize_boolean_attributes: bool = True,
    use_trailing_solidus: bool = False,
    space_before_trailing_solidus: bool = True,
    escape_lt_in_attrs: bool = False,
    escape_rcdata: bool = False,
    resolve_entities: bool = True,
    alphabetical_attributes: bool = False,
    inject_meta_charset: bool = True,
    strip_whitespace: bool = False,
    sanitize: bool = False,
) -> bytes:
    """
    Serializes the input token stream using the specified treewalker

    :arg input: the token stream to serialize

    :arg tree: the treewalker to use

    :arg encoding: the encoding to use

    :arg serializer_opts: any options to pass to the
        :py:class:`html5lib.serializer.HTMLSerializer` that gets created

    :returns: the tree serialized as a string

    Example:

    >>> from html5lib.html5parser import parse
    >>> from html5lib.serializer import serialize
    >>> token_stream = parse('<html><body><p>Hi!</p></body></html>')
    >>> serialize(token_stream, omit_optional_tags=False)
    '<html><head></head><body><p>Hi!</p></body></html>'
    """
    ...

class HTMLSerializer:
    quote_attr_values: Literal["legacy", "spec", "always"]
    quote_char: str
    use_best_quote_char: bool
    omit_optional_tags: bool
    minimize_boolean_attributes: bool
    use_trailing_solidus: bool
    space_before_trailing_solidus: bool
    escape_lt_in_attrs: bool
    escape_rcdata: bool
    resolve_entities: bool
    alphabetical_attributes: bool
    inject_meta_charset: bool
    strip_whitespace: bool
    sanitize: bool
    options: tuple[str, ...]
    errors: list[Incomplete]
    strict: bool
    def __init__(
        self,
        *,
        quote_attr_values: Literal["legacy", "spec", "always"] = "legacy",
        quote_char: str = '"',
        use_best_quote_char: bool = ...,  # default value depends on whether quote_char was passed
        omit_optional_tags: bool = True,
        minimize_boolean_attributes: bool = True,
        use_trailing_solidus: bool = False,
        space_before_trailing_solidus: bool = True,
        escape_lt_in_attrs: bool = False,
        escape_rcdata: bool = False,
        resolve_entities: bool = True,
        alphabetical_attributes: bool = False,
        inject_meta_charset: bool = True,
        strip_whitespace: bool = False,
        sanitize: bool = False,
    ) -> None:
        """
        Initialize HTMLSerializer

        :arg inject_meta_charset: Whether or not to inject the meta charset.

            Defaults to ``True``.

        :arg quote_attr_values: Whether to quote attribute values that don't
            require quoting per legacy browser behavior (``"legacy"``), when
            required by the standard (``"spec"``), or always (``"always"``).

            Defaults to ``"legacy"``.

        :arg quote_char: Use given quote character for attribute quoting.

            Defaults to ``"`` which will use double quotes unless attribute
            value contains a double quote, in which case single quotes are
            used.

        :arg escape_lt_in_attrs: Whether or not to escape ``<`` in attribute
            values.

            Defaults to ``False``.

        :arg escape_rcdata: Whether to escape characters that need to be
            escaped within normal elements within rcdata elements such as
            style.

            Defaults to ``False``.

        :arg resolve_entities: Whether to resolve named character entities that
            appear in the source tree. The XML predefined entities &lt; &gt;
            &amp; &quot; &apos; are unaffected by this setting.

            Defaults to ``True``.

        :arg strip_whitespace: Whether to remove semantically meaningless
            whitespace. (This compresses all whitespace to a single space
            except within ``pre``.)

            Defaults to ``False``.

        :arg minimize_boolean_attributes: Shortens boolean attributes to give
            just the attribute value, for example::

              <input disabled="disabled">

            becomes::

              <input disabled>

            Defaults to ``True``.

        :arg use_trailing_solidus: Includes a close-tag slash at the end of the
            start tag of void elements (empty elements whose end tag is
            forbidden). E.g. ``<hr/>``.

            Defaults to ``False``.

        :arg space_before_trailing_solidus: Places a space immediately before
            the closing slash in a tag using a trailing solidus. E.g.
            ``<hr />``. Requires ``use_trailing_solidus=True``.

            Defaults to ``True``.

        :arg sanitize: Strip all unsafe or unknown constructs from output.
            See :py:class:`html5lib.filters.sanitizer.Filter`.

            Defaults to ``False``.

        :arg omit_optional_tags: Omit start/end tags that are optional.

            Defaults to ``True``.

        :arg alphabetical_attributes: Reorder attributes to be in alphabetical order.

            Defaults to ``False``.
        """
        ...
    def encode(self, string: str) -> str | bytes: ...  # result depends on self.encoding
    def encodeStrict(self, string: str) -> str | bytes: ...  # result depends on self.encoding
    encoding: str | None

    @overload
    def serialize(self, treewalker, encoding: Literal[""] | None = None) -> Generator[str]: ...
    @overload
    def serialize(self, treewalker, encoding: str = ...) -> Generator[bytes]: ...

    @overload
    def render(self, treewalker, encoding: Literal[""] | None = None) -> str:
        """
        Serializes the stream from the treewalker into a string

        :arg treewalker: the treewalker to serialize

        :arg encoding: the string encoding to use

        :returns: the serialized tree

        Example:

        >>> from html5lib import parse, getTreeWalker
        >>> from html5lib.serializer import HTMLSerializer
        >>> token_stream = parse('<html><body>Hi!</body></html>')
        >>> walker = getTreeWalker('etree')
        >>> serializer = HTMLSerializer(omit_optional_tags=False)
        >>> serializer.render(walker(token_stream))
        '<html><head></head><body>Hi!</body></html>'
        """
        ...
    @overload
    def render(self, treewalker, encoding: str = ...) -> bytes: ...

    def serializeError(self, data="XXX ERROR MESSAGE NEEDED") -> None: ...

class SerializeError(Exception):
    """Error in serialized tree"""
    ...

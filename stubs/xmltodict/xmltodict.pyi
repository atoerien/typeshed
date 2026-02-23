"""Makes working with XML feel like you are working with JSON"""

from _typeshed import ReadableBuffer, SupportsRead, SupportsWrite
from collections.abc import Callable, Container, Generator, Mapping
from typing import Any, overload
from typing_extensions import TypeAlias

class ParsingInterrupted(Exception): ...

# dict as attribute value is exclusive to xmlns: https://github.com/bigpick/xmltodict/commit/22541b4874365cb8d2397f23087a866b3081fd9c
_AttrValue: TypeAlias = str | dict[str, str]
_AttrDict: TypeAlias = dict[str, _AttrValue]

class _DictSAXHandler:
    path: list[tuple[str, _AttrDict | None]]
    stack: list[tuple[_AttrDict | None, list[str]]]
    data: list[str]
    item: _AttrDict | None
    item_depth: int
    xml_attribs: bool
    item_callback: Callable[[list[tuple[str, _AttrDict | None]], str | _AttrDict | None], bool]
    attr_prefix: str
    cdata_key: str
    force_cdata: bool | Container[str] | Callable[[tuple[str, _AttrDict | None], str, str], bool]
    cdata_separator: str
    postprocessor: Callable[[list[tuple[str, _AttrDict | None]], str, _AttrValue], tuple[str, _AttrValue]] | None
    dict_constructor: type
    strip_whitespace: bool
    namespace_separator: str
    namespaces: Mapping[str, str | None] | None
    namespace_declarations: dict[str, str]
    force_list: bool | Container[str] | Callable[[tuple[str, _AttrDict | None], str, str], bool] | None
    comment_key: str
    def __init__(
        self,
        item_depth: int = 0,
        item_callback: Callable[[list[tuple[str, _AttrDict | None]], str | _AttrDict | None], bool] = ...,
        xml_attribs: bool = True,
        attr_prefix: str = "@",
        cdata_key: str = "#text",
        force_cdata: bool | Container[str] | Callable[[tuple[str, _AttrDict | None], str, str], bool] = False,
        cdata_separator: str = "",
        postprocessor: Callable[[list[tuple[str, _AttrDict | None]], str, _AttrValue], tuple[str, _AttrValue]] | None = None,
        dict_constructor: type = ...,
        strip_whitespace: bool = True,
        namespace_separator: str = ":",
        namespaces: Mapping[str, str | None] | None = None,
        force_list: bool | Container[str] | Callable[[tuple[str, _AttrDict | None], str, str], bool] | None = None,
        comment_key: str = "#comment",
    ) -> None: ...
    def startNamespaceDecl(self, prefix: str, uri: str) -> None: ...
    def startElement(self, full_name: str, attrs: dict[str, str] | list[str]) -> None: ...
    def endElement(self, full_name: str) -> None: ...
    def characters(self, data: str) -> None: ...
    def comments(self, data: str) -> None: ...
    def push_data(self, item: _AttrDict | None, key: str, data: str) -> _AttrDict: ...

def parse(
    xml_input: str | ReadableBuffer | SupportsRead[bytes] | Generator[ReadableBuffer],
    encoding: str | None = None,
    expat: Any = ...,
    process_namespaces: bool = False,
    namespace_separator: str = ":",
    disable_entities: bool = True,
    process_comments: bool = False,
    *,
    item_depth: int = 0,
    item_callback: Callable[[list[tuple[str, _AttrDict | None]], str | _AttrDict | None], bool] = ...,
    xml_attribs: bool = True,
    attr_prefix: str = "@",
    cdata_key: str = "#text",
    force_cdata: bool | Container[str] | Callable[[tuple[str, _AttrDict | None], str, str], bool] = False,
    cdata_separator: str = "",
    postprocessor: Callable[[list[tuple[str, _AttrDict | None]], str, _AttrValue], tuple[str, _AttrValue]] | None = None,
    dict_constructor: type = ...,
    strip_whitespace: bool = True,
    namespaces: Mapping[str, str | None] | None = None,
    force_list: bool | Container[str] | Callable[[tuple[str, _AttrDict | None], str, str], bool] | None = None,
    comment_key: str = "#comment",
) -> dict[str, Any]:
    """
    Parse the given XML input and convert it into a dictionary.

    `xml_input` can either be a `string`, a file-like object, or a generator of strings.

    If `xml_attribs` is `True`, element attributes are put in the dictionary
    among regular child elements, using `@` as a prefix to avoid collisions. If
    set to `False`, they are just ignored.

    Simple example::

        >>> import xmltodict
        >>> doc = xmltodict.parse(\"\"\"
        ... <a prop="x">
        ...   <b>1</b>
        ...   <b>2</b>
        ... </a>
        ... \"\"\")
        >>> doc['a']['@prop']
        'x'
        >>> doc['a']['b']
        ['1', '2']

    If `item_depth` is `0`, the function returns a dictionary for the root
    element (default behavior). Otherwise, it calls `item_callback` every time
    an item at the specified depth is found and returns `None` in the end
    (streaming mode).

    The callback function receives two parameters: the `path` from the document
    root to the item (name-attribs pairs), and the `item` (dict). If the
    callback's return value is false-ish, parsing will be stopped with the
    :class:`ParsingInterrupted` exception.

    Streaming example::

        >>> def handle(path, item):
        ...     print('path:%s item:%s' % (path, item))
        ...     return True
        ...
        >>> xmltodict.parse(\"\"\"
        ... <a prop="x">
        ...   <b>1</b>
        ...   <b>2</b>
        ... </a>\"\"\", item_depth=2, item_callback=handle)
        path:[('a', {'prop': 'x'}), ('b', None)] item:1
        path:[('a', {'prop': 'x'}), ('b', None)] item:2

    The optional argument `postprocessor` is a function that takes `path`,
    `key` and `value` as positional arguments and returns a new `(key, value)`
    pair where both `key` and `value` may have changed. Usage example::

        >>> def postprocessor(path, key, value):
        ...     try:
        ...         return key + ':int', int(value)
        ...     except (ValueError, TypeError):
        ...         return key, value
        >>> xmltodict.parse('<a><b>1</b><b>2</b><b>x</b></a>',
        ...                 postprocessor=postprocessor)
        {'a': {'b:int': [1, 2], 'b': 'x'}}

    You can pass an alternate version of `expat` (such as `defusedexpat`) by
    using the `expat` parameter. E.g:

        >>> import defusedexpat
        >>> xmltodict.parse('<a>hello</a>', expat=defusedexpat.pyexpat)
        {'a': 'hello'}

    You can use the force_list argument to force lists to be created even
    when there is only a single child of a given level of hierarchy. The
    force_list argument is a tuple of keys. If the key for a given level
    of hierarchy is in the force_list argument, that level of hierarchy
    will have a list as a child (even if there is only one sub-element).
    The index_keys operation takes precedence over this. This is applied
    after any user-supplied postprocessor has already run.

        For example, given this input:
        <servers>
          <server>
            <name>host1</name>
            <os>Linux</os>
            <interfaces>
              <interface>
                <name>em0</name>
                <ip_address>10.0.0.1</ip_address>
              </interface>
            </interfaces>
          </server>
        </servers>

        If called with force_list=('interface',), it will produce
        this dictionary:
        {'servers':
          {'server':
            {'name': 'host1',
             'os': 'Linux'},
             'interfaces':
              {'interface':
                [ {'name': 'em0', 'ip_address': '10.0.0.1' } ] } } }

        `force_list` can also be a callable that receives `path`, `key` and
        `value`. This is helpful in cases where the logic that decides whether
        a list should be forced is more complex.


        If `process_comments` is `True`, comments will be added using `comment_key`
        (default=`'#comment'`) to the tag that contains the comment.

            For example, given this input:
            <a>
              <b>
                <!-- b comment -->
                <c>
                    <!-- c comment -->
                    1
                </c>
                <d>2</d>
              </b>
            </a>

            If called with `process_comments=True`, it will produce
            this dictionary:
            'a': {
                'b': {
                    '#comment': 'b comment',
                    'c': {

                        '#comment': 'c comment',
                        '#text': '1',
                    },
                    'd': '2',
                },
            }
        Comment text is subject to the `strip_whitespace` flag: when it is left
        at the default `True`, comments will have leading and trailing
        whitespace removed. Disable `strip_whitespace` to keep comment
        indentation or padding intact.
    """
    ...
@overload
def unparse(
    input_dict: Mapping[str, Any],
    output: SupportsWrite[bytes] | SupportsWrite[str],
    encoding: str = "utf-8",
    full_document: bool = True,
    short_empty_elements: bool = False,
    comment_key: str = "#comment",
    *,
    attr_prefix: str = "@",
    cdata_key: str = "#text",
    depth: int = 0,
    # preprocessor is called like (preprocessor(key, value) for key, value in input_dict.items()).
    # It is expected to return its input, or a modification thereof
    preprocessor: Callable[[str, Any], tuple[str, Any]] | None = None,
    pretty: bool = False,
    newl: str = "\n",
    indent: str | int = "\t",
    namespace_separator: str = ":",
    namespaces: Mapping[str, str | None] | None = None,
    expand_iter: str | None = None,
) -> None:
    """
    Emit an XML document for the given `input_dict` (reverse of `parse`).

        The resulting XML document is returned as a string, but if `output` (a
        file-like object) is specified, it is written there instead.

        Dictionary keys prefixed with `attr_prefix` (default=`'@'`) are interpreted
        as XML node attributes, whereas keys equal to `cdata_key`
        (default=`'#text'`) are treated as character data.

        Empty lists are omitted entirely: ``{"a": []}`` produces no ``<a>`` element.
        Provide a placeholder entry (for example ``{"a": [""]}``) when an explicit
        empty container element must be emitted.

        The `pretty` parameter (default=`False`) enables pretty-printing. In this
        mode, lines are terminated with `'
    '` and indented with `' '`, but this
        can be customized with the `newl` and `indent` parameters.
        The `bytes_errors` parameter controls decoding errors for byte values and
        defaults to `'replace'`.

    
    """
    ...
@overload
def unparse(
    input_dict: Mapping[str, Any],
    output: None = None,
    encoding: str = "utf-8",
    full_document: bool = True,
    short_empty_elements: bool = False,
    comment_key: str = "#comment",
    *,
    attr_prefix: str = "@",
    cdata_key: str = "#text",
    depth: int = 0,
    # preprocessor is called like (preprocessor(key, value) for key, value in input_dict.items()).
    # It is expected to return its input, or a modification thereof
    preprocessor: Callable[[str, Any], tuple[str, Any]] | None = None,
    pretty: bool = False,
    newl: str = "\n",
    indent: str | int = "\t",
    namespace_separator: str = ":",
    namespaces: Mapping[str, str | None] | None = None,
    expand_iter: str | None = None,
) -> str:
    """
    Emit an XML document for the given `input_dict` (reverse of `parse`).

        The resulting XML document is returned as a string, but if `output` (a
        file-like object) is specified, it is written there instead.

        Dictionary keys prefixed with `attr_prefix` (default=`'@'`) are interpreted
        as XML node attributes, whereas keys equal to `cdata_key`
        (default=`'#text'`) are treated as character data.

        Empty lists are omitted entirely: ``{"a": []}`` produces no ``<a>`` element.
        Provide a placeholder entry (for example ``{"a": [""]}``) when an explicit
        empty container element must be emitted.

        The `pretty` parameter (default=`False`) enables pretty-printing. In this
        mode, lines are terminated with `'
    '` and indented with `' '`, but this
        can be customized with the `newl` and `indent` parameters.
        The `bytes_errors` parameter controls decoding errors for byte values and
        defaults to `'replace'`.

    
    """
    ...

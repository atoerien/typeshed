import xml.etree.ElementTree as ET
from _typeshed import Unused
from collections.abc import Callable
from typing import Any, Literal, overload

def current_global_nsmap() -> dict[str, str]: ...

class IncrementalTree(ET.ElementTree):
    def write(  # type: ignore[override]
        self,
        file_or_filename: ET._FileWrite,
        encoding: str | None = None,
        xml_declaration: bool | None = None,
        default_namespace: str | None = None,
        method: Literal["xml", "html", "text"] | None = None,  # does not accept 'c14n', unlike parent method
        *,
        short_empty_elements: bool = True,
        nsmap: dict[str, str] | None = None,
        root_ns_only: bool = False,
        minimal_ns_only: bool = False,
    ) -> None:
        """
        Write element tree to a file as XML.

        Arguments:
          *file_or_filename* -- file name or a file object opened for writing

          *encoding* -- the output encoding (default: US-ASCII)

          *xml_declaration* -- bool indicating if an XML declaration should be
                               added to the output. If None, an XML declaration
                               is added if encoding IS NOT either of:
                               US-ASCII, UTF-8, or Unicode

          *default_namespace* -- sets the default XML namespace (for "xmlns").
                                 Takes precedence over any default namespace
                                 provided in nsmap or
                                 xml.etree.ElementTree.register_namespace().

          *method* -- either "xml" (default), "html, "text", or "c14n"

          *short_empty_elements* -- controls the formatting of elements
                                    that contain no content. If True (default)
                                    they are emitted as a single self-closed
                                    tag, otherwise they are emitted as a pair
                                    of start/end tags

          *nsmap* -- a mapping of namespace prefixes to URIs. These take
                     precedence over any mappings registered using
                     xml.etree.ElementTree.register_namespace(). The
                     default_namespace argument, if supplied, takes precedence
                     over any default namespace supplied in nsmap. All supplied
                     namespaces will be declared on the root element, even if
                     unused in the document.

          *root_ns_only* -- bool indicating namespace declrations should only
                            be written on the root element.  This requires two
                            passes of the xml tree adding additional time to
                            the writing process. This is primarily meant to
                            mimic xml.etree.ElementTree's behaviour.

          *minimal_ns_only* -- bool indicating only namespaces that were used
                               to qualify elements or attributes should be
                               declared. All namespace declarations will be
                               written on the root element regardless of the
                               value of the root_ns_only arg. Requires two
                               passes of the xml tree adding additional time to
                               the writing process.
        """
        ...

def process_attribs(
    elem: ET.Element[Any],
    is_nsmap_scope_changed: bool | None,
    default_ns_attr_prefix: str | None,
    nsmap_scope: dict[str, str],
    global_nsmap: dict[str, str],
    new_namespace_prefixes: set[str],
    uri_to_prefix: dict[str, str],
) -> tuple[list[tuple[str, str]], str | None, dict[str, str]]: ...
def write_elem_start(
    write: Callable[..., None],
    elem: ET.Element[Any],
    nsmap_scope: dict[str, str],
    global_nsmap: dict[str, str],
    short_empty_elements: bool | None,
    is_html: bool | None,
    is_root: bool = False,
    uri_to_prefix: dict[str, str] | None = None,
    default_ns_attr_prefix: str | None = None,
    new_nsmap: dict[str, str] | None = None,
    **kwargs: Unused,
) -> tuple[str | None, dict[str, str], str | None, dict[str, str] | None, bool]:
    """
    Write the opening tag (including self closing) and element text.

    Refer to _serialize_ns_xml for description of arguments.

    nsmap_scope should be an empty dictionary on first call. All nsmap prefixes
    must be strings with the default namespace prefix represented by "".

    eg.
    - <foo attr1="one">      (returns tag = 'foo')
    - <foo attr1="one">text  (returns tag = 'foo')
    - <foo attr1="one" />    (returns tag = None)

    Returns:
        tag:
            The tag name to be closed or None if no closing required.
        nsmap_scope:
            The current nsmap after any prefix to uri additions from this
            element. This is the input dict if unmodified or an updated copy.
        default_ns_attr_prefix:
            The prefix for the default namespace to use with attrs.
        uri_to_prefix:
            The current uri to prefix map after any uri to prefix additions
            from this element. This is the input dict if unmodified or an
            updated copy.
        next_remains_root:
            A bool indicating if the child element(s) should be treated as
            their own roots.
    """
    ...

@overload
def tostring(
    element: ET.Element[Any],
    encoding: None = None,
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = False,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> bytes:
    """
    Generate string representation of XML element.

    All subelements are included.  If encoding is "unicode", a string
    is returned. Otherwise a bytestring is returned.

    *element* is an Element instance, *encoding* is an optional output
    encoding defaulting to US-ASCII, *method* is an optional output which can
    be one of "xml" (default), "html", "text" or "c14n", *default_namespace*
    sets the default XML namespace (for "xmlns").

    Returns an (optionally) encoded string containing the XML data.
    """
    ...
@overload
def tostring(
    element: ET.Element[Any],
    encoding: Literal["unicode"],
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = False,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> str:
    """
    Generate string representation of XML element.

    All subelements are included.  If encoding is "unicode", a string
    is returned. Otherwise a bytestring is returned.

    *element* is an Element instance, *encoding* is an optional output
    encoding defaulting to US-ASCII, *method* is an optional output which can
    be one of "xml" (default), "html", "text" or "c14n", *default_namespace*
    sets the default XML namespace (for "xmlns").

    Returns an (optionally) encoded string containing the XML data.
    """
    ...
@overload
def tostring(
    element: ET.Element[Any],
    encoding: str,
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = False,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> Any:
    """
    Generate string representation of XML element.

    All subelements are included.  If encoding is "unicode", a string
    is returned. Otherwise a bytestring is returned.

    *element* is an Element instance, *encoding* is an optional output
    encoding defaulting to US-ASCII, *method* is an optional output which can
    be one of "xml" (default), "html", "text" or "c14n", *default_namespace*
    sets the default XML namespace (for "xmlns").

    Returns an (optionally) encoded string containing the XML data.
    """
    ...

@overload
def tostringlist(
    element: ET.Element[Any],
    encoding: None = None,
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = False,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> list[bytes]: ...
@overload
def tostringlist(
    element: ET.Element[Any],
    encoding: Literal["unicode"],
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = False,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> list[str]: ...
@overload
def tostringlist(
    element: ET.Element[Any],
    encoding: str,
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = False,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> list[Any]: ...

@overload
def compat_tostring(
    element: ET.Element[Any],
    encoding: None = None,
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = True,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> bytes:
    """
    tostring with options that produce the same results as xml.etree.ElementTree.tostring

    root_ns_only=True is a bit slower than False as it needs to traverse the
    tree one more time to collect all the namespaces.
    """
    ...
@overload
def compat_tostring(
    element: ET.Element[Any],
    encoding: Literal["unicode"],
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = True,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> str:
    """
    tostring with options that produce the same results as xml.etree.ElementTree.tostring

    root_ns_only=True is a bit slower than False as it needs to traverse the
    tree one more time to collect all the namespaces.
    """
    ...
@overload
def compat_tostring(
    element: ET.Element[Any],
    encoding: str,
    method: Literal["xml", "html", "text"] | None = None,
    *,
    xml_declaration: bool | None = None,
    default_namespace: str | None = None,
    short_empty_elements: bool = True,
    nsmap: dict[str, str] | None = None,
    root_ns_only: bool = True,
    minimal_ns_only: bool = False,
    tree_cls: type[ET.ElementTree] = ...,
) -> Any:
    """
    tostring with options that produce the same results as xml.etree.ElementTree.tostring

    root_ns_only=True is a bit slower than False as it needs to traverse the
    tree one more time to collect all the namespaces.
    """
    ...

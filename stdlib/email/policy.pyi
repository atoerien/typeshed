"""
This will be the home for the policy that hooks in the new
code that adds all the email6 features.
"""

from collections.abc import Callable
from email._policybase import Compat32 as Compat32, Policy as Policy, _MessageFactory, _MessageT, compat32 as compat32
from email.contentmanager import ContentManager
from email.message import EmailMessage
from typing import Any, overload
from typing_extensions import Self

__all__ = ["Compat32", "compat32", "Policy", "EmailPolicy", "default", "strict", "SMTP", "HTTP"]

class EmailPolicy(Policy[_MessageT]):
    r"""
    Controls for how messages are interpreted and formatted.

    Most of the classes and many of the methods in the email package accept
    Policy objects as parameters.  A Policy object contains a set of values and
    functions that control how input is interpreted and how output is rendered.
    For example, the parameter 'raise_on_defect' controls whether or not an RFC
    violation results in an error being raised or not, while 'max_line_length'
    controls the maximum length of output lines when a Message is serialized.

    Any valid attribute may be overridden when a Policy is created by passing
    it as a keyword argument to the constructor.  Policy objects are immutable,
    but a new Policy object can be created with only certain values changed by
    calling the Policy instance with keyword arguments.  Policy objects can
    also be added, producing a new Policy object in which the non-default
    attributes set in the right hand operand overwrite those specified in the
    left operand.

    Settable attributes:

    raise_on_defect     -- If true, then defects should be raised as errors.
                           Default: False.

    linesep             -- string containing the value to use as separation
                           between output lines.  Default '\n'.

    cte_type            -- Type of allowed content transfer encodings

                           7bit  -- ASCII only
                           8bit  -- Content-Transfer-Encoding: 8bit is allowed

                           Default: 8bit.  Also controls the disposition of
                           (RFC invalid) binary data in headers; see the
                           documentation of the binary_fold method.

    max_line_length     -- maximum length of lines, excluding 'linesep',
                           during serialization.  None or 0 means no line
                           wrapping is done.  Default is 78.

    mangle_from_        -- a flag that, when True escapes From_ lines in the
                           body of the message by putting a '>' in front of
                           them. This is used when the message is being
                           serialized by a generator. Default: False.

    message_factory     -- the class to use to create new message objects.
                           If the value is None, the default is Message.

    verify_generated_headers
                        -- if true, the generator verifies that each header
                           they are properly folded, so that a parser won't
                           treat it as multiple headers, start-of-body, or
                           part of another header.
                           This is a check against custom Header & fold()
                           implementations.
    PROVISIONAL

    The API extensions enabled by this policy are currently provisional.
    Refer to the documentation for details.

    This policy adds new header parsing and folding algorithms.  Instead of
    simple strings, headers are custom objects with custom attributes
    depending on the type of the field.  The folding algorithm fully
    implements RFCs 2047 and 5322.

    In addition to the settable attributes listed above that apply to
    all Policies, this policy adds the following additional attributes:

    utf8                -- if False (the default) message headers will be
                           serialized as ASCII, using encoded words to encode
                           any non-ASCII characters in the source strings.  If
                           True, the message headers will be serialized using
                           utf8 and will not contain encoded words (see RFC
                           6532 for more on this serialization format).

    refold_source       -- if the value for a header in the Message object
                           came from the parsing of some source, this attribute
                           indicates whether or not a generator should refold
                           that value when transforming the message back into
                           stream form.  The possible values are:

                           none  -- all source values use original folding
                           long  -- source values that have any line that is
                                    longer than max_line_length will be
                                    refolded
                           all  -- all values are refolded.

                           The default is 'long'.

    header_factory      -- a callable that takes two arguments, 'name' and
                           'value', where 'name' is a header field name and
                           'value' is an unfolded header field value, and
                           returns a string-like object that represents that
                           header.  A default header_factory is provided that
                           understands some of the RFC5322 header field types.
                           (Currently address fields and date fields have
                           special treatment, while all other fields are
                           treated as unstructured.  This list will be
                           completed before the extension is marked stable.)

    content_manager     -- an object with at least two methods: get_content
                           and set_content.  When the get_content or
                           set_content method of a Message object is called,
                           it calls the corresponding method of this object,
                           passing it the message object as its first argument,
                           and any arguments or keywords that were passed to
                           it as additional arguments.  The default
                           content_manager is
                           :data:`~email.contentmanager.raw_data_manager`.
    """
    utf8: bool
    refold_source: str
    header_factory: Callable[[str, Any], Any]
    content_manager: ContentManager

    @overload
    def __init__(
        self: EmailPolicy[EmailMessage],
        *,
        max_line_length: int | None = ...,
        linesep: str = ...,
        cte_type: str = ...,
        raise_on_defect: bool = ...,
        mangle_from_: bool = ...,
        message_factory: None = None,
        # Added in Python 3.9.20, 3.10.15, 3.11.10, 3.12.5
        verify_generated_headers: bool = ...,
        utf8: bool = ...,
        refold_source: str = ...,
        header_factory: Callable[[str, str], str] = ...,
        content_manager: ContentManager = ...,
    ) -> None: ...
    @overload
    def __init__(
        self,
        *,
        max_line_length: int | None = ...,
        linesep: str = ...,
        cte_type: str = ...,
        raise_on_defect: bool = ...,
        mangle_from_: bool = ...,
        message_factory: _MessageFactory[_MessageT] | None = ...,
        # Added in Python 3.9.20, 3.10.15, 3.11.10, 3.12.5
        verify_generated_headers: bool = ...,
        utf8: bool = ...,
        refold_source: str = ...,
        header_factory: Callable[[str, str], str] = ...,
        content_manager: ContentManager = ...,
    ) -> None: ...

    def header_source_parse(self, sourcelines: list[str]) -> tuple[str, str]: ...
    def header_store_parse(self, name: str, value: Any) -> tuple[str, Any]: ...
    def header_fetch_parse(self, name: str, value: str) -> Any: ...
    def fold(self, name: str, value: str) -> Any: ...
    def fold_binary(self, name: str, value: str) -> bytes: ...
    def clone(
        self,
        *,
        max_line_length: int | None = ...,
        linesep: str = ...,
        cte_type: str = ...,
        raise_on_defect: bool = ...,
        mangle_from_: bool = ...,
        message_factory: _MessageFactory[_MessageT] | None = ...,
        # Added in Python 3.9.20, 3.10.15, 3.11.10, 3.12.5
        verify_generated_headers: bool = ...,
        utf8: bool = ...,
        refold_source: str = ...,
        header_factory: Callable[[str, str], str] = ...,
        content_manager: ContentManager = ...,
    ) -> Self:
        """
        Return a new instance with specified attributes changed.

        The new instance has the same attribute values as the current object,
        except for the changes passed in as keyword arguments.
        """
        ...

default: EmailPolicy[EmailMessage]
SMTP: EmailPolicy[EmailMessage]
SMTPUTF8: EmailPolicy[EmailMessage]
HTTP: EmailPolicy[EmailMessage]
strict: EmailPolicy[EmailMessage]

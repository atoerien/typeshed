"""Contains the Nextgen Pythonic Protobuf Text Format APIs."""

from collections.abc import Callable
from typing import TypeVar
from typing_extensions import TypeAlias

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

_MessageT = TypeVar("_MessageT", bound=Message)
_MsgFormatter: TypeAlias = Callable[[Message, int, bool], str | None]

def serialize(
    message: Message,
    as_utf8: bool = True,
    as_one_line: bool = False,
    use_short_repeated_primitives: bool = False,
    pointy_brackets: bool = False,
    use_index_order: bool = False,
    use_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    indent: int = 0,
    message_formatter: _MsgFormatter | None = None,
    print_unknown_fields: bool = False,
    force_colon: bool = False,
) -> str:
    """
    Convert protobuf message to text format.

    Double values can be formatted compactly with 15 digits of
    precision (which is the most that IEEE 754 "double" can guarantee)
    using double_format='.15g'. To ensure that converting to text and back to a
    proto will result in an identical value, double_format='.17g' should be used.

    Args:
      message: The protocol buffers message.
      as_utf8: Return unescaped Unicode for non-ASCII characters.
      as_one_line: Don't introduce newlines between fields.
      use_short_repeated_primitives: Use short repeated format for primitives.
      pointy_brackets: If True, use angle brackets instead of curly braces for
        nesting.
      use_index_order: If True, fields of a proto message will be printed using
        the order defined in source code instead of the field number, extensions
        will be printed at the end of the message and their relative order is
        determined by the extension number. By default, use the field number
        order.
      use_field_number: If True, print field numbers instead of names.
      descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
      indent (int): The initial indent level, in terms of spaces, for pretty
        print.
      message_formatter (function(message, indent, as_one_line) -> unicode|None):
        Custom formatter for selected sub-messages (usually based on message
        type). Use to pretty print parts of the protobuf for easier diffing.
      print_unknown_fields: If True, unknown fields will be printed.
      force_colon: If set, a colon will be added after the field name even if the
        field is a proto message.

    Returns:
      str: A string of the text formatted protocol buffer message.
    """
    ...
def parse(
    message_class: type[_MessageT],
    text: str | bytes,
    allow_unknown_extension: bool = False,
    allow_field_number: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    allow_unknown_field: bool = False,
) -> _MessageT:
    """
    Parses a text representation of a protocol message into a message.

    Args:
      message_class: The message meta class.
      text (str): Message text representation.
      message (Message): A protocol buffer message to merge into.
      allow_unknown_extension: if True, skip over missing extensions and keep
        parsing
      allow_field_number: if True, both field number and field name are allowed.
      descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
      allow_unknown_field: if True, skip over unknown field and keep parsing.
        Avoid to use this option if possible. It may hide some errors (e.g.
        spelling error on field name)

    Returns:
      Message: A new message passed from text.

    Raises:
      ParseError: On text parsing problems.
    """
    ...

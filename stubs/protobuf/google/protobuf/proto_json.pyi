"""Contains the Nextgen Pythonic Protobuf JSON APIs."""

from typing import Any, TypeVar

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

_MessageT = TypeVar("_MessageT", bound=Message)

def serialize(
    message: Message,
    always_print_fields_with_no_presence: bool = False,
    preserving_proto_field_name: bool = False,
    use_integers_for_enums: bool = False,
    descriptor_pool: DescriptorPool | None = None,
) -> dict[str, Any]:
    """
    Converts protobuf message to a dictionary.

    When the dictionary is encoded to JSON, it conforms to ProtoJSON spec.

    Args:
      message: The protocol buffers message instance to serialize.
      always_print_fields_with_no_presence: If True, fields without presence
        (implicit presence scalars, repeated fields, and map fields) will always
        be serialized. Any field that supports presence is not affected by this
        option (including singular message fields and oneof fields).
      preserving_proto_field_name: If True, use the original proto field names as
        defined in the .proto file. If False, convert the field names to
        lowerCamelCase.
      use_integers_for_enums: If true, print integers instead of enum names.
      descriptor_pool: A Descriptor Pool for resolving types. If None use the
        default.

    Returns:
      A dict representation of the protocol buffer message.
    """
    ...
def parse(
    message_class: type[_MessageT],
    js_dict: dict[str, Any],
    ignore_unknown_fields: bool = False,
    descriptor_pool: DescriptorPool | None = None,
    max_recursion_depth: int = 100,
) -> _MessageT:
    """
    Parses a JSON dictionary representation into a message.

    Args:
      message_class: The message meta class.
      js_dict: Dict representation of a JSON message.
      ignore_unknown_fields: If True, do not raise errors for unknown fields.
      descriptor_pool: A Descriptor Pool for resolving types. If None use the
        default.
      max_recursion_depth: max recursion depth of JSON message to be deserialized.
        JSON messages over this depth will fail to be deserialized. Default value
        is 100.

    Returns:
      A new message passed from json_dict.
    """
    ...

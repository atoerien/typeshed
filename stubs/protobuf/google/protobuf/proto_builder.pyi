"""Dynamic Protobuf class creator."""

from collections import OrderedDict

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

def MakeSimpleProtoClass(
    fields: dict[str, int] | OrderedDict[str, int], full_name: str | None = None, pool: DescriptorPool | None = None
) -> type[Message]:
    """
    Create a Protobuf class whose fields are basic types.

    Note: this doesn't validate field names!

    Args:
      fields: dict of {name: field_type} mappings for each field in the proto. If
          this is an OrderedDict the order will be maintained, otherwise the
          fields will be sorted by name.
      full_name: optional str, the fully-qualified name of the proto type.
      pool: optional DescriptorPool instance.
    Returns:
      a class, the new protobuf class with a FileDescriptor.
    """
    ...

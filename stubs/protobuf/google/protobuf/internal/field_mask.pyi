"""Contains FieldMask class."""

from google.protobuf.descriptor import Descriptor, FieldDescriptor as FieldDescriptor
from google.protobuf.message import Message

class FieldMask:
    """Class for FieldMask message type."""
    def ToJsonString(self) -> str:
        """Converts FieldMask to string according to ProtoJSON spec."""
        ...
    def FromJsonString(self, value: str) -> None:
        """Converts string to FieldMask according to ProtoJSON spec."""
        ...
    def IsValidForDescriptor(self, message_descriptor: Descriptor) -> bool:
        """Checks whether the FieldMask is valid for Message Descriptor."""
        ...
    def AllFieldsFromDescriptor(self, message_descriptor: Descriptor) -> None:
        """Gets all direct fields of Message Descriptor to FieldMask."""
        ...
    def CanonicalFormFromMask(self, mask: FieldMask) -> None:
        """
        Converts a FieldMask to the canonical form.

        Removes paths that are covered by another path. For example,
        "foo.bar" is covered by "foo" and will be removed if "foo"
        is also in the FieldMask. Then sorts all paths in alphabetical order.

        Args:
          mask: The original FieldMask to be converted.
        """
        ...
    def Union(self, mask1: FieldMask, mask2: FieldMask) -> None:
        """Merges mask1 and mask2 into this FieldMask."""
        ...
    def Intersect(self, mask1: FieldMask, mask2: FieldMask) -> None:
        """Intersects mask1 and mask2 into this FieldMask."""
        ...
    def MergeMessage(
        self, source: Message, destination: Message, replace_message_field: bool = False, replace_repeated_field: bool = False
    ) -> None:
        """
        Merges fields specified in FieldMask from source to destination.

        Args:
          source: Source message.
          destination: The destination message to be merged into.
          replace_message_field: Replace message field if True. Merge message
              field if False.
          replace_repeated_field: Replace repeated field if True. Append
              elements of repeated field if False.
        """
        ...

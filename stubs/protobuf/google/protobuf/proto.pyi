"""Contains the Nextgen Pythonic protobuf APIs."""

from io import BytesIO
from typing import TypeVar

from google.protobuf.message import Message

_MessageT = TypeVar("_MessageT", bound=Message)

def serialize(message: Message, deterministic: bool | None = None) -> bytes:
    """
    Return the serialized proto.

    Args:
      message: The proto message to be serialized.
      deterministic: If true, requests deterministic serialization
          of the protobuf, with predictable ordering of map keys.

    Returns:
      A binary bytes representation of the message.
    """
    ...
def parse(message_class: type[_MessageT], payload: bytes) -> _MessageT:
    """
    Given a serialized data in binary form, deserialize it into a Message.

    Args:
      message_class: The message meta class.
      payload: A serialized bytes in binary form.

    Returns:
      A new message deserialized from payload.
    """
    ...
def serialize_length_prefixed(message: Message, output: BytesIO) -> None:
    """
    Writes the size of the message as a varint and the serialized message.

    Writes the size of the message as a varint and then the serialized message.
    This allows more data to be written to the output after the message. Use
    parse_length_prefixed to parse messages written by this method.

    The output stream must be buffered, e.g. using
    https://docs.python.org/3/library/io.html#buffered-streams.

    Example usage:
      out = io.BytesIO()
      for msg in message_list:
        proto.serialize_length_prefixed(msg, out)

    Args:
      message: The protocol buffer message that should be serialized.
      output: BytesIO or custom buffered IO that data should be written to.
    """
    ...
def parse_length_prefixed(message_class: type[_MessageT], input_bytes: BytesIO) -> _MessageT:
    """
    Parse a message from input_bytes.

    Args:
      message_class: The protocol buffer message class that parser should parse.
      input_bytes: A buffered input.

    Example usage:
      while True:
        msg = proto.parse_length_prefixed(message_class, input_bytes)
        if msg is None:
          break
        ...

    Returns:
      A parsed message if successful. None if input_bytes is at EOF.
    """
    ...
def byte_size(message: Message) -> int:
    """
    Returns the serialized size of this message.

    Args:
      message: A proto message.

    Returns:
      int: The number of bytes required to serialize this message.
    """
    ...
def clear_message(message: Message) -> None:
    """
    Clears all data that was set in the message.

    Args:
      message: The proto message to be cleared.
    """
    ...
def clear_field(message: Message, field_name: str) -> None:
    """
    Clears the contents of a given field.

    Inside a oneof group, clears the field set. If the name neither refers to a
    defined field or oneof group, :exc:`ValueError` is raised.

    Args:
      message: The proto message.
      field_name (str): The name of the field to be cleared.

    Raises:
      ValueError: if the `field_name` is not a member of this message.
    """
    ...

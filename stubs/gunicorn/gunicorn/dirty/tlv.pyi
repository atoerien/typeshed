"""
TLV (Type-Length-Value) Binary Encoder/Decoder

Provides efficient binary serialization for dirty worker protocol messages.
Inspired by OpenBSD msgctl/msgsnd message format.

Type Codes:
    0x00: None (no value bytes)
    0x01: bool (1 byte: 0x00 or 0x01)
    0x05: int64 (8 bytes big-endian signed)
    0x06: float64 (8 bytes IEEE 754)
    0x10: bytes (4-byte length + raw bytes)
    0x11: string (4-byte length + UTF-8 encoded)
    0x20: list (4-byte count + encoded elements)
    0x21: dict (4-byte count + encoded key-value pairs)
"""

from _typeshed import Incomplete
from typing import Final

TYPE_NONE: Final = 0x00
TYPE_BOOL: Final = 0x01
TYPE_INT64: Final = 0x05
TYPE_FLOAT64: Final = 0x06
TYPE_BYTES: Final = 0x10
TYPE_STRING: Final = 0x11
TYPE_LIST: Final = 0x20
TYPE_DICT: Final = 0x21
MAX_STRING_SIZE: Final = 67108864
MAX_BYTES_SIZE: Final = 67108864
MAX_LIST_SIZE: Final = 1048576
MAX_DICT_SIZE: Final = 1048576

class TLVEncoder:
    """
    TLV binary encoder/decoder.

    Encodes Python values to binary TLV format and decodes back.
    Supports: None, bool, int, float, bytes, str, list, dict.
    """
    @staticmethod
    def encode(
        value: bool | float | str | bytes | list[Incomplete] | tuple[Incomplete, ...] | dict[object, Incomplete] | None,
    ) -> bytes:
        """
        Encode a Python value to TLV binary format.

        Args:
            value: Python value to encode (None, bool, int, float,
                   bytes, str, list, or dict)

        Returns:
            bytes: TLV-encoded binary data

        Raises:
            DirtyProtocolError: If value type is not supported
        """
        ...
    @staticmethod
    def decode(data: bytes, offset: int = 0) -> tuple[Incomplete, int]:
        """
        Decode a TLV-encoded value from binary data.

        Args:
            data: Binary data to decode
            offset: Starting offset in the data

        Returns:
            tuple: (decoded_value, new_offset)

        Raises:
            DirtyProtocolError: If data is malformed or truncated
        """
        ...
    @staticmethod
    def decode_full(data: bytes):
        """
        Decode a complete TLV-encoded value, ensuring all data is consumed.

        Args:
            data: Binary data to decode

        Returns:
            Decoded Python value

        Raises:
            DirtyProtocolError: If data is malformed or has trailing bytes
        """
        ...

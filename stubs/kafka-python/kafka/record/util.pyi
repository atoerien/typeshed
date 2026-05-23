def encode_varint(value, write):
    """
    Encode an integer to a varint presentation. See
    https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
    on how those can be produced.

        Arguments:
            value (int): Value to encode
            write (function): Called per byte that needs to be writen

        Returns:
            int: Number of bytes written
    """
    ...
def size_of_varint(value):
    """
    Number of bytes needed to encode an integer in variable-length format.
    
    """
    ...
def decode_varint(buffer, pos: int = 0):
    """
    Decode an integer from a varint presentation. See
    https://developers.google.com/protocol-buffers/docs/encoding?csw=1#varints
    on how those can be produced.

        Arguments:
            buffer (bytearray): buffer to read from.
            pos (int): optional position to read from

        Returns:
            (int, int): Decoded int value and next read position
    """
    ...
def calc_crc32c(memview, _crc32c=...):
    """
    Calculate CRC-32C (Castagnoli) checksum over a memoryview of data
    
    """
    ...
def calc_crc32(memview):
    """
    Calculate simple CRC-32 checksum over a memoryview of data
    
    """
    ...

from _typeshed import Incomplete

ZSTD_MAX_OUTPUT_SIZE: Incomplete
PYPY: Incomplete

def has_gzip(): ...
def has_snappy(): ...
def has_zstd(): ...
def has_lz4(): ...
def gzip_encode(payload, compresslevel=None): ...
def gzip_decode(payload): ...
def snappy_encode(payload, xerial_compatible: bool = True, xerial_blocksize=32768):
    """
    Encodes the given data with snappy compression.

    If xerial_compatible is set then the stream is encoded in a fashion
    compatible with the xerial snappy library.

    The block size (xerial_blocksize) controls how frequent the blocking occurs
    32k is the default in the xerial library.

    The format winds up being:


        +-------------+------------+--------------+------------+--------------+
        |   Header    | Block1 len | Block1 data  | Blockn len | Blockn data  |
        +-------------+------------+--------------+------------+--------------+
        |  16 bytes   |  BE int32  | snappy bytes |  BE int32  | snappy bytes |
        +-------------+------------+--------------+------------+--------------+


    It is important to note that the blocksize is the amount of uncompressed
    data presented to snappy at each block, whereas the blocklen is the number
    of bytes that will be present in the stream; so the length will always be
    <= blocksize.
    """
    ...
def snappy_decode(payload): ...

lz4_encode: Incomplete

def lz4f_decode(payload):
    """Decode payload using interoperable LZ4 framing. Requires Kafka >= 0.10"""
    ...

lz4_decode: Incomplete
lz4_decode = lz4f_decode

def lz4_encode_old_kafka(payload):
    """Encode payload for 0.8/0.9 brokers -- requires an incorrect header checksum."""
    ...
def lz4_decode_old_kafka(payload): ...
def zstd_encode(payload): ...
def zstd_decode(payload): ...

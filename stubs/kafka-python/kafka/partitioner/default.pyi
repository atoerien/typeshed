from .abc import Partitioner

class DefaultPartitioner(Partitioner):
    """
    Default partitioner.

    Hashes key to partition using murmur2 hashing (from java client)
    If key is None, selects partition randomly from available,
    or from all partitions if none are currently available
    """
    def partition(self, topic, key, serialized_key, value, serialized_value, cluster) -> int: ...

def murmur2(data: bytes) -> int:
    """
    Pure-python Murmur2 implementation.

    Based on java client, see org.apache.kafka.common.utils.Utils.murmur2

    Args:
        data (bytes): opaque bytes

    Returns: MurmurHash2 of data
    """
    ...

from _typeshed import Incomplete

from kafka.record.abc import ABCRecord, ABCRecordBatch, ABCRecordBatchBuilder

class LegacyRecordBase:
    HEADER_STRUCT_V0: Incomplete
    HEADER_STRUCT_V1: Incomplete
    LOG_OVERHEAD: Incomplete
    CRC_OFFSET: Incomplete
    MAGIC_OFFSET: Incomplete
    RECORD_OVERHEAD_V0: Incomplete
    RECORD_OVERHEAD_V1: Incomplete
    KEY_OFFSET_V0: Incomplete
    KEY_OFFSET_V1: Incomplete
    KEY_LENGTH: Incomplete
    VALUE_LENGTH: Incomplete
    CODEC_MASK: int
    CODEC_NONE: int
    CODEC_GZIP: int
    CODEC_SNAPPY: int
    CODEC_LZ4: int
    TIMESTAMP_TYPE_MASK: int
    LOG_APPEND_TIME: int
    CREATE_TIME: int
    NO_TIMESTAMP: int

class LegacyRecordBatch(ABCRecordBatch, LegacyRecordBase):
    def __init__(self, buffer, magic) -> None: ...
    @property
    def base_offset(self): ...
    @property
    def size_in_bytes(self): ...
    @property
    def timestamp_type(self):
        """
        0 for CreateTime; 1 for LogAppendTime; None if unsupported.

        Value is determined by broker; produced messages should always set to 0
        Requires Kafka >= 0.10 / message version >= 1
        """
        ...
    @property
    def compression_type(self): ...
    @property
    def magic(self): ...
    def validate_crc(self): ...
    def __iter__(self): ...

class LegacyRecord(ABCRecord):
    def __init__(self, magic, offset, timestamp, timestamp_type, key, value, crc, crc_bytes) -> None: ...
    @property
    def magic(self): ...
    @property
    def offset(self): ...
    @property
    def timestamp(self):
        """
        Epoch milliseconds
        
        """
        ...
    @property
    def timestamp_type(self):
        """
        CREATE_TIME(0) or APPEND_TIME(1)
        
        """
        ...
    @property
    def key(self):
        """
        Bytes key or None
        
        """
        ...
    @property
    def value(self):
        """
        Bytes value or None
        
        """
        ...
    @property
    def headers(self): ...
    @property
    def checksum(self): ...
    def validate_crc(self): ...
    @property
    def size_in_bytes(self): ...

class LegacyRecordBatchBuilder(ABCRecordBatchBuilder, LegacyRecordBase):
    def __init__(self, magic, compression_type, batch_size) -> None: ...
    def append(self, offset, timestamp, key, value, headers=None):
        """
        Append message to batch.
        
        """
        ...
    def build(self):
        """Compress batch to be ready for send"""
        ...
    def size(self):
        """
        Return current size of data written to buffer
        
        """
        ...
    def size_in_bytes(self, offset, timestamp, key, value, headers=None):
        """
        Actual size of message to add
        
        """
        ...
    @classmethod
    def record_size(cls, magic, key, value): ...
    @classmethod
    def record_overhead(cls, magic): ...
    @classmethod
    def estimate_size_in_bytes(cls, magic, compression_type, key, value):
        """
        Upper bound estimate of record size.
        
        """
        ...

class LegacyRecordMetadata:
    def __init__(self, offset, crc, size, timestamp) -> None: ...
    @property
    def offset(self): ...
    @property
    def crc(self): ...
    @property
    def size(self): ...
    @property
    def timestamp(self): ...

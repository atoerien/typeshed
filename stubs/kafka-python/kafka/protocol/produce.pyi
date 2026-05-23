import abc
from _typeshed import Incomplete
from typing import type_check_only

from kafka.protocol.api import Request, Response

class ProduceResponse_v0(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v1(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v2(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v3(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v4(Response):
    """
    The version number is bumped up to indicate that the client supports KafkaStorageException.
    The KafkaStorageException will be translated to NotLeaderForPartitionException in the response if version <= 3
    """
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v5(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v6(Response):
    """The version number is bumped to indicate that on quota violation brokers send out responses before throttling."""
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v7(Response):
    """V7 bumped up to indicate ZStandard capability. (see KIP-110)"""
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class ProduceResponse_v8(Response):
    """
    V8 bumped up to add two new fields record_errors offset list and error_message
    (See KIP-467)
    """
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

@type_check_only
class _ProduceRequest(Request, metaclass=abc.ABCMeta):
    API_KEY: int
    def expect_response(self): ...

class ProduceRequest_v0(_ProduceRequest):
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v0
    SCHEMA: Incomplete

class ProduceRequest_v1(_ProduceRequest):
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v1
    SCHEMA: Incomplete

class ProduceRequest_v2(_ProduceRequest):
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v2
    SCHEMA: Incomplete

class ProduceRequest_v3(_ProduceRequest):
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v3
    SCHEMA: Incomplete

class ProduceRequest_v4(_ProduceRequest):
    """
    The version number is bumped up to indicate that the client supports KafkaStorageException.
    The KafkaStorageException will be translated to NotLeaderForPartitionException in the response if version <= 3
    """
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v4
    SCHEMA: Incomplete

class ProduceRequest_v5(_ProduceRequest):
    """
    Same as v4. The version number is bumped since the v5 response includes an additional
    partition level field: the log_start_offset.
    """
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v5
    SCHEMA: Incomplete

class ProduceRequest_v6(_ProduceRequest):
    """The version number is bumped to indicate that on quota violation brokers send out responses before throttling."""
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v6
    SCHEMA: Incomplete

class ProduceRequest_v7(_ProduceRequest):
    """V7 bumped up to indicate ZStandard capability. (see KIP-110)"""
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v7
    SCHEMA: Incomplete

class ProduceRequest_v8(_ProduceRequest):
    """
    V8 bumped up to add two new fields record_errors offset list and error_message to PartitionResponse
    (See KIP-467)
    """
    API_VERSION: int
    RESPONSE_TYPE = ProduceResponse_v8
    SCHEMA: Incomplete

ProduceRequest: list[type[_ProduceRequest]]
ProduceResponse: Incomplete

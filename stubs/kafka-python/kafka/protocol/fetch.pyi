from _typeshed import Incomplete
from typing import NamedTuple

from kafka.protocol.api import Request, Response

class AbortedTransaction(NamedTuple):
    """AbortedTransaction(producer_id, first_offset)"""
    producer_id: Incomplete
    first_offset: Incomplete

class FetchResponse_v0(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v1(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v2(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v3(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v4(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v5(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v6(Response):
    """
    Same as FetchResponse_v5. The version number is bumped up to indicate that the client supports KafkaStorageException.
    The KafkaStorageException will be translated to NotLeaderForPartitionException in the response if version <= 5
    """
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v7(Response):
    """Add error_code and session_id to response"""
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v8(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v9(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v10(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchResponse_v11(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class FetchRequest_v0(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v0
    SCHEMA: Incomplete

class FetchRequest_v1(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v1
    SCHEMA: Incomplete

class FetchRequest_v2(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v2
    SCHEMA: Incomplete

class FetchRequest_v3(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v3
    SCHEMA: Incomplete

class FetchRequest_v4(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v4
    SCHEMA: Incomplete

class FetchRequest_v5(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v5
    SCHEMA: Incomplete

class FetchRequest_v6(Request):
    """
    The body of FETCH_REQUEST_V6 is the same as FETCH_REQUEST_V5.
    The version number is bumped up to indicate that the client supports KafkaStorageException.
    The KafkaStorageException will be translated to NotLeaderForPartitionException in the response if version <= 5
    """
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v6
    SCHEMA: Incomplete

class FetchRequest_v7(Request):
    """Add incremental fetch requests (see KIP-227)"""
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v7
    SCHEMA: Incomplete

class FetchRequest_v8(Request):
    """bump used to indicate that on quota violation brokers send out responses before throttling."""
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v8
    SCHEMA: Incomplete

class FetchRequest_v9(Request):
    """adds the current leader epoch (see KIP-320)"""
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v9
    SCHEMA: Incomplete

class FetchRequest_v10(Request):
    """bumped up to indicate ZStandard capability. (see KIP-110)"""
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v10
    SCHEMA: Incomplete

class FetchRequest_v11(Request):
    """added rack ID to support read from followers (KIP-392)"""
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = FetchResponse_v11
    SCHEMA: Incomplete

FetchRequest: Incomplete
FetchResponse: Incomplete

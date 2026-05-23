from _typeshed import Incomplete

from kafka.protocol.api import Request, Response

class MetadataResponse_v0(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v1(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v2(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v3(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v4(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v5(Response):
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v6(Response):
    """
    Metadata Request/Response v6 is the same as v5,
    but on quota violation, brokers send out responses before throttling.
    """
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v7(Response):
    """v7 adds per-partition leader_epoch field"""
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataResponse_v8(Response):
    """v8 adds authorized_operations fields"""
    API_KEY: int
    API_VERSION: int
    SCHEMA: Incomplete

class MetadataRequest_v0(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v0
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v1(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v1
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v2(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v2
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v3(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v3
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v4(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v4
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v5(Request):
    """
    The v5 metadata request is the same as v4.
    An additional field for offline_replicas has been added to the v5 metadata response
    """
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v5
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v6(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v6
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v7(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v7
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

class MetadataRequest_v8(Request):
    API_KEY: int
    API_VERSION: int
    RESPONSE_TYPE = MetadataResponse_v8
    SCHEMA: Incomplete
    ALL_TOPICS: Incomplete
    NO_TOPICS: Incomplete

MetadataRequest: Incomplete
MetadataResponse: Incomplete

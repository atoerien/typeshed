from _typeshed import Incomplete
from typing_extensions import Self

from kafka.protocol.api_data import ApiData
from kafka.protocol.api_message import ApiMessage

class SaslHandshakeRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 supports SASL_AUTHENTICATE.
      // NOTE: Version cannot be easily bumped due to incorrect
      // client negotiation for clients <= 2.4.
      // See https://issues.apache.org/jira/browse/KAFKA-9577
    """
    mechanism: str
    def __init__(self, *args, mechanism: str = ..., version: int | None = None, **kwargs) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class SaslHandshakeResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      // NOTE: Version cannot be easily bumped due to incorrect
      // client negotiation for clients <= 2.4.
      // See https://issues.apache.org/jira/browse/KAFKA-9577
    """
    error_code: int
    mechanisms: list[str]
    def __init__(
        self, *args, error_code: int = ..., mechanisms: list[str] = ..., version: int | None = None, **kwargs
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class SaslAuthenticateRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      // Version 2 adds flexible version support
    """
    auth_bytes: bytes | ApiData
    def __init__(self, *args, auth_bytes: bytes | ApiData = ..., version: int | None = None, **kwargs) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class SaslAuthenticateResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds the session lifetime.
      // Version 2 adds flexible version support
    """
    error_code: int
    error_message: str | None
    auth_bytes: bytes | ApiData
    session_lifetime_ms: int
    def __init__(
        self,
        *args,
        error_code: int = ...,
        error_message: str | None = ...,
        auth_bytes: bytes | ApiData = ...,
        session_lifetime_ms: int = ...,
        version: int | None = None,
        **kwargs,
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class SaslBytesRequest:
    """Request for raw SASL v0 exchange -- length-prefixed raw bytes."""
    API_VERSION: int
    header: SaslBytesResponse | None
    def __init__(self, data) -> None: ...
    def with_header(self, correlation_id=None, **kwargs) -> None: ...
    def encode(self, framed: bool = True, header: bool = True) -> bytes: ...
    def expect_response(self): ...

class SaslBytesResponse:
    """Response for raw SASL v0 exchange -- returns bytes as-is."""
    correlation_id: Incomplete
    error_code: int
    def __init__(self, correlation_id) -> None: ...
    def parse_header(self, read_buffer) -> Self: ...
    auth_bytes: Incomplete
    def decode(self, read_buffer) -> Self: ...
    def get_response_class(self) -> Self: ...

__all__ = [
    "SaslHandshakeRequest",
    "SaslHandshakeResponse",
    "SaslAuthenticateRequest",
    "SaslAuthenticateResponse",
    "SaslBytesRequest",
    "SaslBytesResponse",
]

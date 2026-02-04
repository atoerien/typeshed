"""
HTTP/2 specific exceptions.

These exceptions map to HTTP/2 error codes defined in RFC 7540.
"""

from typing import Final

class HTTP2ErrorCode:
    """HTTP/2 Error Codes (RFC 7540 Section 7)."""
    NO_ERROR: Final = 0x0
    PROTOCOL_ERROR: Final = 0x1
    INTERNAL_ERROR: Final = 0x2
    FLOW_CONTROL_ERROR: Final = 0x3
    SETTINGS_TIMEOUT: Final = 0x4
    STREAM_CLOSED: Final = 0x5
    FRAME_SIZE_ERROR: Final = 0x6
    REFUSED_STREAM: Final = 0x7
    CANCEL: Final = 0x8
    COMPRESSION_ERROR: Final = 0x9
    CONNECT_ERROR: Final = 0xA
    ENHANCE_YOUR_CALM: Final = 0xB
    INADEQUATE_SECURITY: Final = 0xC
    HTTP_1_1_REQUIRED: Final = 0xD

class HTTP2Error(Exception):
    """Base exception for HTTP/2 errors."""
    message: str
    error_code: int

    def __init__(self, message: str | None = None, error_code: int | None = None) -> None: ...

class HTTP2ProtocolError(HTTP2Error):
    """Protocol error detected."""
    ...
class HTTP2InternalError(HTTP2Error):
    """Internal error occurred."""
    ...
class HTTP2FlowControlError(HTTP2Error):
    """Flow control limits exceeded."""
    ...
class HTTP2SettingsTimeout(HTTP2Error):
    """Settings acknowledgment timeout."""
    ...
class HTTP2StreamClosed(HTTP2Error):
    """Stream was closed."""
    ...
class HTTP2FrameSizeError(HTTP2Error):
    """Frame size is incorrect."""
    ...
class HTTP2RefusedStream(HTTP2Error):
    """Stream was refused."""
    ...
class HTTP2Cancel(HTTP2Error):
    """Stream was cancelled."""
    ...
class HTTP2CompressionError(HTTP2Error):
    """Compression state error."""
    ...
class HTTP2ConnectError(HTTP2Error):
    """Connection error during CONNECT."""
    ...
class HTTP2EnhanceYourCalm(HTTP2Error):
    """Peer is generating excessive load."""
    ...
class HTTP2InadequateSecurity(HTTP2Error):
    """Transport security is inadequate."""
    ...
class HTTP2RequiresHTTP11(HTTP2Error):
    """HTTP/1.1 is required for this request."""
    ...

class HTTP2StreamError(HTTP2Error):
    """Error specific to a single stream."""
    stream_id: int

    def __init__(self, stream_id: int, message: str | None = None, error_code: int | None = None) -> None: ...

class HTTP2ConnectionError(HTTP2Error):
    """Error affecting the entire connection."""
    ...
class HTTP2ConfigurationError(HTTP2Error):
    """Invalid HTTP/2 configuration."""
    ...

class HTTP2NotAvailable(HTTP2Error):
    """HTTP/2 support is not available (h2 library not installed)."""
    def __init__(self, message: str | None = None) -> None: ...

__all__ = [
    "HTTP2ErrorCode",
    "HTTP2Error",
    "HTTP2ProtocolError",
    "HTTP2InternalError",
    "HTTP2FlowControlError",
    "HTTP2SettingsTimeout",
    "HTTP2StreamClosed",
    "HTTP2FrameSizeError",
    "HTTP2RefusedStream",
    "HTTP2Cancel",
    "HTTP2CompressionError",
    "HTTP2ConnectError",
    "HTTP2EnhanceYourCalm",
    "HTTP2InadequateSecurity",
    "HTTP2RequiresHTTP11",
    "HTTP2StreamError",
    "HTTP2ConnectionError",
    "HTTP2ConfigurationError",
    "HTTP2NotAvailable",
]

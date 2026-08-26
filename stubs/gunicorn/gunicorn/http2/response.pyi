"""WSGI response writer for HTTP/2 streams."""

import socket

from gunicorn.config import Config
from gunicorn.http import Request
from gunicorn.http.wsgi import Response
from gunicorn.http2.connection import HTTP2ServerConnection

class HTTP2Response(Response):
    """
    A WSGI Response that frames its output as HTTP/2 instead of HTTP/1.

    Only the wire framing is overridden. Everything the WSGI protocol needs
    (``start_response``, header processing, the no-body rules for HEAD, 1xx,
    204 and 304, the Content-Length accounting in ``write()``) is inherited,
    so HTTP/2 responses obey the same rules as HTTP/1 ones rather than a
    parallel set that has to be kept in step by hand.
    """
    h2_conn: HTTP2ServerConnection
    stream_id: int
    def __init__(
        self, req: Request, sock: socket.socket, cfg: Config, h2_conn: HTTP2ServerConnection, stream_id: int
    ) -> None: ...
    def is_chunked(self) -> bool: ...
    def can_sendfile(self) -> bool: ...
    def send_headers(self) -> None: ...
    def close(self) -> None: ...

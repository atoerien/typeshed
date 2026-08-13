import socket as _socket

from kafka.net.inet import KafkaNetSocket

class HttpConnectProxy(KafkaNetSocket):
    """
    Tunnels broker connections through an HTTP CONNECT proxy (RFC 7231 s4.3.6).

    Registered for the ``http`` scheme -- pass ``proxy_url='http://host:port'``
    to KafkaConsumer/KafkaProducer/KafkaAdminClient.

    Basic proxy auth is supported via URL credentials: ``http://user:pass@host:8080``.
    Broker hostnames are always forwarded unresolved so the proxy handles DNS.
    """
    SCHEMES: tuple[str, ...]
    def __init__(self, proxy_url) -> None: ...  # pyright: ignore[reportInconsistentConstructor]
    def dns_lookup(self, host, port, proxy: bool = False): ...
    def socket(self, family=..., sock_type=..., proto=...) -> _socket.socket: ...
    def connect_ex(self, sock, addr) -> int: ...

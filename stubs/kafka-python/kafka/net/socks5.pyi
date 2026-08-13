import socket as _socket
from typing import Final

from kafka.net.inet import KafkaNetSocket

class ProxyConnectionStates:
    DISCONNECTED: Final = "<disconnected>"
    CONNECTING: Final = "<connecting>"
    NEGOTIATE_PROPOSE: Final = "<negotiate_propose>"
    NEGOTIATING: Final = "<negotiating>"
    AUTHENTICATING: Final = "<authenticating>"
    REQUEST_SUBMIT: Final = "<request_submit>"
    REQUESTING: Final = "<requesting>"
    READ_ADDRESS: Final = "<read_address>"
    COMPLETE: Final = "<complete>"

class Socks5Proxy(KafkaNetSocket):
    """
    Socks5 proxy

    Manages connection through socks5 proxy with support for username/password
    authentication.
    """
    SCHEMES: tuple[str, ...]
    def __init__(self, proxy_url: str) -> None: ...  # pyright: ignore[reportInconsistentConstructor]
    def dns_lookup(self, host, port, proxy: bool = False): ...
    def socket(self, family=..., sock_type=..., proto=...) -> _socket.socket:
        """
        Open and record a socket.

        Returns the actual underlying socket
        object to ensure e.g. selects and ssl wrapping works as expected.
        """
        ...
    def connect_ex(self, sock, addr) -> int:
        """
        Runs a state machine through connection to authentication to
        proxy connection request.

        The somewhat strange setup is to facilitate non-intrusive use from
        BrokerConnection state machine.

        This function is called with a socket in non-blocking mode. Both
        send and receive calls can return in EWOULDBLOCK/EAGAIN which we
        specifically avoid handling here. These are handled in main
        BrokerConnection connection loop, which then would retry calls
        to this function.
        """
        ...

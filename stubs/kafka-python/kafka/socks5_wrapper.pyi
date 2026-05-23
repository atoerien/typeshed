from _typeshed import Incomplete

log: Incomplete

class ProxyConnectionStates:
    DISCONNECTED: str
    CONNECTING: str
    NEGOTIATE_PROPOSE: str
    NEGOTIATING: str
    AUTHENTICATING: str
    REQUEST_SUBMIT: str
    REQUESTING: str
    READ_ADDRESS: str
    COMPLETE: str

class Socks5Wrapper:
    """
    Socks5 proxy wrapper

    Manages connection through socks5 proxy with support for username/password
    authentication.
    """
    def __init__(self, proxy_url, afi) -> None: ...
    @classmethod
    def is_inet_4_or_6(cls, gai):
        """Given a getaddrinfo struct, return True iff ipv4 or ipv6"""
        ...
    @classmethod
    def dns_lookup(cls, host, port, afi=...):
        """Returns a list of getaddrinfo structs, optionally filtered to an afi (ipv4 / ipv6)"""
        ...
    @classmethod
    def use_remote_lookup(cls, proxy_url): ...
    def socket(self, family, sock_type):
        """
        Open and record a socket.

        Returns the actual underlying socket
        object to ensure e.g. selects and ssl wrapping works as expected.
        """
        ...
    def connect_ex(self, addr):
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

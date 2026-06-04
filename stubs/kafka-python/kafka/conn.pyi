import ssl
from _typeshed import Incomplete

log: Incomplete
DEFAULT_KAFKA_PORT: int
ssl_available: bool
SSLEOFError = ssl.SSLEOFError
SSLWantReadError = ssl.SSLWantReadError
SSLWantWriteError = ssl.SSLWantWriteError
SSLZeroReturnError = ssl.SSLZeroReturnError

AFI_NAMES: Incomplete

class ConnectionStates:
    DISCONNECTED: str
    CONNECTING: str
    HANDSHAKE: str
    CONNECTED: str
    AUTHENTICATING: str
    API_VERSIONS_SEND: str
    API_VERSIONS_RECV: str

class BrokerConnection:
    """
    Initialize a Kafka broker connection

    Keyword Arguments:
        client_id (str): a name for this client. This string is passed in
            each request to servers and can be used to identify specific
            server-side log entries that correspond to this client. Also
            submitted to GroupCoordinator for logging with respect to
            consumer group administration. Default: 'kafka-python-{version}'
        client_software_name (str): Sent to kafka broker for KIP-511.
            Default: 'kafka-python'
        client_software_version (str): Sent to kafka broker for KIP-511.
            Default: The kafka-python version (via kafka.version).
        reconnect_backoff_ms (int): The amount of time in milliseconds to
            wait before attempting to reconnect to a given host.
            Default: 50.
        reconnect_backoff_max_ms (int): The maximum amount of time in
            milliseconds to backoff/wait when reconnecting to a broker that has
            repeatedly failed to connect. If provided, the backoff per host
            will increase exponentially for each consecutive connection
            failure, up to this maximum. Once the maximum is reached,
            reconnection attempts will continue periodically with this fixed
            rate. To avoid connection storms, a randomization factor of 0.2
            will be applied to the backoff resulting in a random range between
            20% below and 20% above the computed value. Default: 30000.
        request_timeout_ms (int): Client request timeout in milliseconds.
            Default: 30000.
        max_in_flight_requests_per_connection (int): Requests are pipelined
            to kafka brokers up to this number of maximum requests per
            broker connection. Default: 5.
        receive_message_max_bytes (int): Maximum allowed network frame size.
            Used to avoid OOM when decoding malformed network message header.
            Default: 1000000.
        receive_buffer_bytes (int): The size of the TCP receive buffer
            (SO_RCVBUF) to use when reading data. Default: None (relies on
            system defaults). Java client defaults to 32768.
        send_buffer_bytes (int): The size of the TCP send buffer
            (SO_SNDBUF) to use when sending data. Default: None (relies on
            system defaults). Java client defaults to 131072.
        socket_options (list): List of tuple-arguments to socket.setsockopt
            to apply to broker connection sockets. Default:
            [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
        security_protocol (str): Protocol used to communicate with brokers.
            Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
            Default: PLAINTEXT.
        ssl_context (ssl.SSLContext): pre-configured SSLContext for wrapping
            socket connections. If provided, all other ssl_* configurations
            will be ignored. Default: None.
        ssl_check_hostname (bool): flag to configure whether ssl handshake
            should verify that the certificate matches the brokers hostname.
            default: True.
        ssl_cafile (str): optional filename of ca file to use in certificate
            verification. default: None.
        ssl_certfile (str): optional filename of file in pem format containing
            the client certificate, as well as any ca certificates needed to
            establish the certificate's authenticity. default: None.
        ssl_keyfile (str): optional filename containing the client private key.
            default: None.
        ssl_password (callable, str, bytes, bytearray): optional password or
            callable function that returns a password, for decrypting the
            client private key. Default: None.
        ssl_crlfile (str): optional filename containing the CRL to check for
            certificate expiration. By default, no CRL check is done. When
            providing a file, only the leaf certificate will be checked against
            this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+.
            default: None.
        ssl_ciphers (str): optionally set the available ciphers for ssl
            connections. It should be a string in the OpenSSL cipher list
            format. If no cipher can be selected (because compile-time options
            or other configuration forbids use of all the specified ciphers),
            an ssl.SSLError will be raised. See ssl.SSLContext.set_ciphers
        api_version (tuple): Specify which Kafka API version to use.
            Must be None or >= (0, 10, 0) to enable SASL authentication.
            Default: None
        api_version_auto_timeout_ms (int): number of milliseconds to throw a
            timeout exception from the constructor when checking the broker
            api version. Only applies if api_version is None. Default: 2000.
        selector (selectors.BaseSelector): Provide a specific selector
            implementation to use for I/O multiplexing.
            Default: selectors.DefaultSelector
        state_change_callback (callable): function to be called when the
            connection state changes from CONNECTING to CONNECTED etc.
        metrics (kafka.metrics.Metrics): Optionally provide a metrics
            instance for capturing network IO stats. Default: None.
        metric_group_prefix (str): Prefix for metric names. Default: ''
        sasl_mechanism (str): Authentication mechanism when security_protocol
            is configured for SASL_PLAINTEXT or SASL_SSL. Valid values are:
            PLAIN, GSSAPI, OAUTHBEARER, SCRAM-SHA-256, SCRAM-SHA-512.
        sasl_plain_username (str): username for sasl PLAIN and SCRAM authentication.
            Required if sasl_mechanism is PLAIN or one of the SCRAM mechanisms.
        sasl_plain_password (str): password for sasl PLAIN and SCRAM authentication.
            Required if sasl_mechanism is PLAIN or one of the SCRAM mechanisms.
        sasl_kerberos_name (str or gssapi.Name): Constructed gssapi.Name for use with
            sasl mechanism handshake. If provided, sasl_kerberos_service_name and
            sasl_kerberos_domain name are ignored. Default: None.
        sasl_kerberos_service_name (str): Service name to include in GSSAPI
            sasl mechanism handshake. Default: 'kafka'
        sasl_kerberos_domain_name (str): kerberos domain name to use in GSSAPI
            sasl mechanism handshake. Default: one of bootstrap servers
        sasl_oauth_token_provider (kafka.sasl.oauth.AbstractTokenProvider): OAuthBearer
            token provider instance. Default: None
        socks5_proxy (str): Socks5 proxy url. Default: None
    """
    DEFAULT_CONFIG: Incomplete
    SECURITY_PROTOCOLS: Incomplete
    VERSION_CHECKS: Incomplete
    host: Incomplete
    port: Incomplete
    afi: Incomplete
    config: Incomplete
    node_id: Incomplete
    in_flight_requests: Incomplete
    state: Incomplete
    last_attempt: int
    def __init__(self, host, port, afi, **configs) -> None: ...
    def connect_blocking(self, timeout=...): ...
    def connect(self):
        """Attempt to connect and return ConnectionState"""
        ...
    def blacked_out(self):
        """
        Return true if we are disconnected from the given node and can't
        re-establish a connection yet
        """
        ...
    def throttled(self):
        """Return True if we are connected but currently throttled."""
        ...
    def throttle_delay(self):
        """Return the number of milliseconds to wait until connection is no longer throttled."""
        ...
    def connection_delay(self):
        """
        Return the number of milliseconds to wait, based on the connection
        state, before attempting to send data. When connecting or disconnected,
        this respects the reconnect backoff time. When connected, returns a very
        large number to handle slow/stalled connections.
        """
        ...
    def connected(self):
        """Return True iff socket is connected."""
        ...
    def connecting(self):
        """
        Returns True if still connecting (this may encompass several
        different states, such as SSL handshake, authorization, etc).
        """
        ...
    def initializing(self):
        """
        Returns True if socket is connected but full connection is not complete.
        During this time the connection may send api requests to the broker to
        check api versions and perform SASL authentication.
        """
        ...
    def disconnected(self):
        """Return True iff socket is closed"""
        ...
    def connect_failed(self):
        """Return True iff connection attempt failed after attempting all dns records"""
        ...
    def __del__(self) -> None: ...
    def close(self, error=None) -> None:
        """
        Close socket and fail all in-flight-requests.

        Arguments:
            error (Exception, optional): pending in-flight-requests
                will be failed with this exception.
                Default: kafka.errors.KafkaConnectionError.
        """
        ...
    def send(self, request, blocking: bool = True, request_timeout_ms=None):
        """
        Queue request for async network send, return Future()

        Arguments:
            request (Request): kafka protocol request object to send.

        Keyword Arguments:
            blocking (bool, optional): Whether to immediately send via
                blocking socket I/O. Default: True.
            request_timeout_ms: Custom timeout in milliseconds for request.
                Default: None (uses value from connection configuration)

        Returns: future
        """
        ...
    def send_pending_requests(self):
        """
        Attempts to send pending requests messages via blocking IO
        If all requests have been sent, return True
        Otherwise, if the socket is blocked and there are more bytes to send,
        return False.
        """
        ...
    def send_pending_requests_v2(self):
        """
        Attempts to send pending requests messages via non-blocking IO
        If all requests have been sent, return True
        Otherwise, if the socket is blocked and there are more bytes to send,
        return False.
        """
        ...
    def can_send_more(self):
        """Check for throttling / quota violations and max in-flight-requests"""
        ...
    def recv(self):
        """
        Non-blocking network receive.

        Return list of (response, future) tuples
        """
        ...
    def requests_timed_out(self): ...
    def timed_out_ifrs(self): ...
    def next_ifr_request_timeout_ms(self): ...
    def get_api_versions(self): ...
    def check_version(self, timeout: int = 2, **kwargs):
        """
        Attempt to guess the broker version.

        Keyword Arguments:
            timeout (numeric, optional): Maximum number of seconds to block attempting
                to connect and check version. Default 2

        Note: This is a blocking call.

        Returns: version tuple, i.e. (3, 9), (2, 4), etc ...

        Raises: NodeNotReadyError on timeout
        """
        ...

class BrokerConnectionMetrics:
    metrics: Incomplete
    bytes_sent: Incomplete
    bytes_received: Incomplete
    request_time: Incomplete
    throttle_time: Incomplete
    def __init__(self, metrics, metric_group_prefix, node_id) -> None: ...

def get_ip_port_afi(host_and_port_str):
    """
    Parse the IP and port from a string in the format of:

        * host_or_ip          <- Can be either IPv4 address literal or hostname/fqdn
        * host_or_ipv4:port   <- Can be either IPv4 address literal or hostname/fqdn
        * [host_or_ip]        <- IPv6 address literal
        * [host_or_ip]:port.  <- IPv6 address literal

    .. note:: IPv6 address literals with ports *must* be enclosed in brackets

    .. note:: If the port is not specified, default will be returned.

    :return: tuple (host, port, afi), afi will be socket.AF_INET or socket.AF_INET6 or socket.AF_UNSPEC
    """
    ...
def is_inet_4_or_6(gai):
    """Given a getaddrinfo struct, return True iff ipv4 or ipv6"""
    ...
def dns_lookup(host, port, afi=...):
    """Returns a list of getaddrinfo structs, optionally filtered to an afi (ipv4 / ipv6)"""
    ...

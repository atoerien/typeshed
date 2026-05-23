from _typeshed import Incomplete
from collections import OrderedDict as OrderedDict

log: Incomplete
socketpair: Incomplete

class KafkaClient:
    """
    A network client for asynchronous request/response network I/O.

    This is an internal class used to implement the user-facing producer and
    consumer clients.

    This class is not thread-safe!

    Attributes:
        cluster (:any:`ClusterMetadata`): Local cache of cluster metadata, retrieved
            via MetadataRequests during :meth:`~kafka.KafkaClient.poll`.

    Keyword Arguments:
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) that the client should contact to bootstrap initial
            cluster metadata. This does not have to be the full node list.
            It just needs to have at least one broker that will respond to a
            Metadata API Request. Default port is 9092. If no servers are
            specified, will default to localhost:9092.
        client_id (str): a name for this client. This string is passed in
            each request to servers and can be used to identify specific
            server-side log entries that correspond to this client. Also
            submitted to GroupCoordinator for logging with respect to
            consumer group administration. Default: 'kafka-python-{version}'
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
        connections_max_idle_ms: Close idle connections after the number of
            milliseconds specified by this config. The broker closes idle
            connections after connections.max.idle.ms, so this avoids hitting
            unexpected socket disconnected errors on the client.
            Default: 540000
        retry_backoff_ms (int): Milliseconds to backoff when retrying on
            errors. Default: 100.
        max_in_flight_requests_per_connection (int): Requests are pipelined
            to kafka brokers up to this number of maximum requests per
            broker connection. Default: 5.
        receive_buffer_bytes (int): The size of the TCP receive buffer
            (SO_RCVBUF) to use when reading data. Default: None (relies on
            system defaults). Java client defaults to 32768.
        send_buffer_bytes (int): The size of the TCP send buffer
            (SO_SNDBUF) to use when sending data. Default: None (relies on
            system defaults). Java client defaults to 131072.
        socket_options (list): List of tuple-arguments to socket.setsockopt
            to apply to broker connection sockets. Default:
            [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
        metadata_max_age_ms (int): The period of time in milliseconds after
            which we force a refresh of metadata even if we haven't seen any
            partition leadership changes to proactively discover any new
            brokers or partitions. Default: 300000
        allow_auto_create_topics (bool): Enable/disable auto topic creation
            on metadata request. Only available with api_version >= (0, 11).
            Default: True
        security_protocol (str): Protocol used to communicate with brokers.
            Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
            Default: PLAINTEXT.
        ssl_context (ssl.SSLContext): Pre-configured SSLContext for wrapping
            socket connections. If provided, all other ssl_* configurations
            will be ignored. Default: None.
        ssl_check_hostname (bool): Flag to configure whether SSL handshake
            should verify that the certificate matches the broker's hostname.
            Default: True.
        ssl_cafile (str): Optional filename of CA file to use in certificate
            verification. Default: None.
        ssl_certfile (str): Optional filename of file in PEM format containing
            the client certificate, as well as any CA certificates needed to
            establish the certificate's authenticity. Default: None.
        ssl_keyfile (str): Optional filename containing the client private key.
            Default: None.
        ssl_password (str): Optional password to be used when loading the
            certificate chain. Default: None.
        ssl_crlfile (str): Optional filename containing the CRL to check for
            certificate expiration. By default, no CRL check is done. When
            providing a file, only the leaf certificate will be checked against
            this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+.
            Default: None.
        ssl_ciphers (str): optionally set the available ciphers for ssl
            connections. It should be a string in the OpenSSL cipher list
            format. If no cipher can be selected (because compile-time options
            or other configuration forbids use of all the specified ciphers),
            an ssl.SSLError will be raised. See ssl.SSLContext.set_ciphers
        api_version (tuple): Specify which Kafka API version to use. If set to
            None, the client will attempt to determine the broker version via
            ApiVersionsRequest API or, for brokers earlier than 0.10, probing
            various known APIs. Dynamic version checking is performed eagerly
            during __init__ and can raise NoBrokersAvailableError if no connection
            was made before timeout (see api_version_auto_timeout_ms below).
            Different versions enable different functionality.

            Examples:
                (3, 9) most recent broker release, enable all supported features
                (0, 10, 0) enables sasl authentication
                (0, 8, 0) enables basic functionality only

            Default: None
        api_version_auto_timeout_ms (int): number of milliseconds to throw a
            timeout exception from the constructor when checking the broker
            api version. Only applies if api_version set to None.
            Default: 2000
        selector (selectors.BaseSelector): Provide a specific selector
            implementation to use for I/O multiplexing.
            Default: selectors.DefaultSelector
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
        socks5_proxy (str): Socks5 proxy URL. Default: None
    """
    DEFAULT_CONFIG: Incomplete
    config: Incomplete
    cluster: Incomplete
    def __init__(self, **configs) -> None: ...
    def maybe_connect(self, node_id, wakeup: bool = True):
        """Queues a node for asynchronous connection during the next .poll()"""
        ...
    def connection_failed(self, node_id): ...
    def ready(self, node_id, metadata_priority: bool = True):
        """
        Check whether a node is connected and ok to send more requests.

        Arguments:
            node_id (int): the id of the node to check
            metadata_priority (bool): Mark node as not-ready if a metadata
                refresh is required. Default: True

        Returns:
            bool: True if we are ready to send to the given node
        """
        ...
    def connected(self, node_id):
        """Return True iff the node_id is connected."""
        ...
    def close(self, node_id=None) -> None:
        """
        Close one or all broker connections.

        Arguments:
            node_id (int, optional): the id of the node to close
        """
        ...
    def __del__(self) -> None: ...
    def is_disconnected(self, node_id):
        """
        Check whether the node connection has been disconnected or failed.

        A disconnected node has either been closed or has failed. Connection
        failures are usually transient and can be resumed in the next ready()
        call, but there are cases where transient failures need to be caught
        and re-acted upon.

        Arguments:
            node_id (int): the id of the node to check

        Returns:
            bool: True iff the node exists and is disconnected
        """
        ...
    def connection_delay(self, node_id):
        """
        Return the number of milliseconds to wait, based on the connection
        state, before attempting to send data. When connecting or disconnected,
        this respects the reconnect backoff time. When connected, returns a very large
        number to handle slow/stalled connections.

        Arguments:
            node_id (int): The id of the node to check

        Returns:
            int: The number of milliseconds to wait.
        """
        ...
    def throttle_delay(self, node_id):
        """
        Return the number of milliseconds to wait until a broker is no longer throttled.
        When disconnected / connecting, returns 0.
        """
        ...
    def is_ready(self, node_id, metadata_priority: bool = True):
        """
        Check whether a node is ready to send more requests.

        In addition to connection-level checks, this method also is used to
        block additional requests from being sent during a metadata refresh.

        Arguments:
            node_id (int): id of the node to check
            metadata_priority (bool): Mark node as not-ready if a metadata
                refresh is required. Default: True

        Returns:
            bool: True if the node is ready and metadata is not refreshing
        """
        ...
    def send(self, node_id, request, wakeup: bool = True, request_timeout_ms=None):
        """
        Send a request to a specific node. Bytes are placed on an
        internal per-connection send-queue. Actual network I/O will be
        triggered in a subsequent call to .poll()

        Arguments:
            node_id (int): destination node
            request (Struct): request object (not-encoded)

        Keyword Arguments:
            wakeup (bool, optional): optional flag to disable thread-wakeup.
            request_timeout_ms (int, optional): Provide custom timeout in milliseconds.
                If response is not processed before timeout, client will fail the
                request and close the connection.
                Default: None (uses value from client configuration)

        Raises:
            AssertionError: if node_id is not in current cluster metadata

        Returns:
            Future: resolves to Response struct or Error
        """
        ...
    def poll(self, timeout_ms=None, future=None):
        """
        Try to read and write to sockets.

        This method will also attempt to complete node connections, refresh
        stale metadata, and run previously-scheduled tasks.

        Arguments:
            timeout_ms (int, optional): maximum amount of time to wait (in ms)
                for at least one response. Must be non-negative. The actual
                timeout will be the minimum of timeout, request timeout and
                metadata timeout. Default: request_timeout_ms
            future (Future, optional): if provided, blocks until future.is_done

        Returns:
            list: responses received (can be empty)
        """
        ...
    def in_flight_request_count(self, node_id=None):
        """
        Get the number of in-flight requests for a node or all nodes.

        Arguments:
            node_id (int, optional): a specific node to check. If unspecified,
                return the total for all nodes

        Returns:
            int: pending in-flight requests for the node, or all nodes if None
        """
        ...
    def least_loaded_node(self):
        """
        Choose the node with fewest outstanding requests, with fallbacks.

        This method will prefer a node with an existing connection (not throttled)
        with no in-flight-requests. If no such node is found, a node will be chosen
        randomly from all nodes that are not throttled or "blacked out" (i.e.,
        are not subject to a reconnect backoff). If no node metadata has been
        obtained, will return a bootstrap node.

        Returns:
            node_id or None if no suitable node was found
        """
        ...
    def least_loaded_node_refresh_ms(self):
        """
        Return connection or throttle delay in milliseconds for next available node.

        This method is used primarily for retry/backoff during metadata refresh
        during / after a cluster outage, in which there are no available nodes.

        Returns:
           float: delay_ms
        """
        ...
    def set_topics(self, topics):
        """
        Set specific topics to track for metadata.

        Arguments:
            topics (list of str): topics to check for metadata

        Returns:
            Future: resolves after metadata request/response
        """
        ...
    def add_topic(self, topic):
        """
        Add a topic to the list of topics tracked via metadata.

        Arguments:
            topic (str): topic to track

        Returns:
            Future: resolves after metadata request/response

        Raises:
            TypeError: if topic is not a string
            ValueError: if topic is invalid: must be chars (a-zA-Z0-9._-), and less than 250 length
        """
        ...
    def get_api_versions(self):
        """
        Return the ApiVersions map, if available.

        Note: Only available after bootstrap; requires broker version 0.10.0 or later.

        Returns: a map of dict mapping {api_key : (min_version, max_version)},
        or None if ApiVersion is not supported by the kafka cluster.
        """
        ...
    def check_version(self, node_id=None, timeout=None, **kwargs):
        """
        Attempt to guess the version of a Kafka broker.

        Keyword Arguments:
            node_id (str, optional): Broker node id from cluster metadata. If None, attempts
                to connect to any available broker until version is identified.
                Default: None
            timeout (num, optional): Maximum time in seconds to try to check broker version.
                If unable to identify version before timeout, raise error (see below).
                Default: api_version_auto_timeout_ms / 1000

        Returns: version tuple, i.e. (3, 9), (2, 0), (0, 10, 2) etc

        Raises:
            NodeNotReadyError (if node_id is provided)
            NoBrokersAvailable (if node_id is None)
        """
        ...
    def api_version(self, operation, max_version=None):
        """
        Find the latest version of the protocol operation supported by both
        this library and the broker.

        This resolves to the lesser of either the latest api version this
        library supports, or the max version supported by the broker.

        Arguments:
            operation: A list of protocol operation versions from kafka.protocol.

        Keyword Arguments:
            max_version (int, optional): Provide an alternate maximum api version
                to reflect limitations in user code.

        Returns:
            int: The highest api version number compatible between client and broker.

        Raises: IncompatibleBrokerVersion if no matching version is found
        """
        ...
    def wakeup(self) -> None: ...
    def bootstrap_connected(self):
        """Return True if a bootstrap node is connected"""
        ...
    def await_ready(self, node_id, timeout_ms: int = 30000):
        """
        Invokes `poll` to discard pending disconnects, followed by `client.ready` and 0 or more `client.poll`
        invocations until the connection to `node` is ready, the timeoutMs expires or the connection fails.

        It returns `true` if the call completes normally or `false` if the timeoutMs expires. If the connection fails,
        an `IOException` is thrown instead. Note that if the `NetworkClient` has been configured with a positive
        connection timeoutMs, it is possible for this method to raise an `IOException` for a previous connection which
        has recently disconnected.

        This method is useful for implementing blocking behaviour on top of the non-blocking `NetworkClient`, use it with
        care.
        """
        ...
    def send_and_receive(self, node_id, request): ...

class IdleConnectionManager:
    connections_max_idle: Incomplete
    next_idle_close_check_time: Incomplete
    lru_connections: Incomplete
    def __init__(self, connections_max_idle_ms) -> None: ...
    def update(self, conn_id) -> None: ...
    def remove(self, conn_id) -> None: ...
    def is_expired(self, conn_id): ...
    def next_check_ms(self): ...
    def update_next_idle_close_check_time(self, ts) -> None: ...
    def poll_expired_connection(self): ...

class KafkaClientMetrics:
    metrics: Incomplete
    metric_group_name: Incomplete
    connection_closed: Incomplete
    connection_created: Incomplete
    select_time: Incomplete
    io_time: Incomplete
    def __init__(self, metrics, metric_group_prefix, conns) -> None: ...

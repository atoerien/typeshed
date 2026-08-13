"""KafkaAdminClient - high-level Kafka cluster administration."""

import selectors
import ssl
from _typeshed import Incomplete
from collections.abc import Callable, Sequence
from types import TracebackType
from typing import Literal
from typing_extensions import Self

from kafka.admin._acls import ACLAdminMixin
from kafka.admin._cluster import ClusterAdminMixin
from kafka.admin._configs import ConfigAdminMixin
from kafka.admin._groups import GroupAdminMixin
from kafka.admin._partitions import PartitionAdminMixin
from kafka.admin._topics import TopicAdminMixin
from kafka.admin._transactions import TransactionsAdminMixin
from kafka.admin._users import UserAdminMixin
from kafka.net.sasl.oauth import AbstractTokenProvider

class KafkaAdminClient(
    ACLAdminMixin,
    ClusterAdminMixin,
    ConfigAdminMixin,
    GroupAdminMixin,
    PartitionAdminMixin,
    TopicAdminMixin,
    TransactionsAdminMixin,
    UserAdminMixin,
):
    """
    A class for administering the Kafka cluster.

    Keyword Arguments:
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) that the consumer should contact to bootstrap initial
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
        receive_message_max_bytes (int): Maximum allowed network frame size.
            Used to avoid OOM when decoding malformed network message header.
            Default: 100_000_000.
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
            this CRL. Default: None.
        api_version (tuple): Specify which Kafka API version to use. If set to
            None, the client will infer the broker version from the results of
            ApiVersionsRequest API. For brokers earlier than 0.10, which do not
            support the ApiVersionsRequest API, api_version is required.
            Note: Dynamic version checking is performed eagerly during __init__
            and can raise KafkaTimeoutError if no connection can be made before
            timeout (see bootstrap_timeout_ms below).
            Different versions enable different functionality.

            Examples::

                (4, 3) most recent broker release, enable all supported features
                (2, 7) support SCRAM user credential apis
                (0, 11) enables message format v2 (internal)
                (0, 10, 0) enables sasl authentication and message format v1
                (0, 9) enables full group coordination features with automatic
                    partition assignment and rebalancing,
                (0, 8, 2) enables kafka-storage offset commits with manual
                    partition assignment only,
                (0, 8, 1) enables zookeeper-storage offset commits with manual
                    partition assignment only,
                (0, 8, 0) enables basic functionality but requires manual
                    partition assignment and offset management.

            Default: None
        bootstrap_timeout_ms (int): number of milliseconds to wait for first
            successful cluster bootstrap. If provided, an attempt to bootstrap
            will raise KafkaTimeoutError if it is unable to fetch cluster
            metadata before the configured timeout. Note that bootstrap is
            called eagerly from __init__().
            Default: 30000
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
        sasl_oauth_token_provider (kafka.net.sasl.oauth.AbstractTokenProvider): OAuthBearer
            token provider instance. Default: None
        proxy_url (str): URL to proxy socket connections through. Supports SOCKS5 only.
            Requires scheme:// (e.g., socks5://foo.bar/). Default: None
        kafka_client (callable): Custom class / callable for creating KafkaNetClient instances
    """
    DEFAULT_CONFIG: dict[str, Incomplete]
    config: dict[str, Incomplete]
    def __init__(
        self,
        *,
        bootstrap_servers: str | Sequence[str] = "localhost",
        client_id: str = ...,
        request_timeout_ms: int = 30_000,
        connections_max_idle_ms: int = 540_000,
        reconnect_backoff_ms: int = 50,
        reconnect_backoff_max_ms: int = 30_000,
        max_in_flight_requests_per_connection: int = 5,
        receive_message_max_bytes: int = 100_000_000,
        receive_buffer_bytes: int | None = None,
        send_buffer_bytes: int | None = None,
        socket_options: Sequence[tuple[int, int, int]] = ...,
        retry_backoff_ms: int = 100,
        metadata_max_age_ms: int = 300_000,
        client_dns_lookup: str = "use_all_dns_ips",
        security_protocol: Literal["PLAINTEXT", "SSL", "SASL_PLAINTEXT", "SASL_SSL"] = "PLAINTEXT",
        ssl_context: ssl.SSLContext | None = None,
        ssl_check_hostname: bool = True,
        ssl_cafile: str | None = None,
        ssl_certfile: str | None = None,
        ssl_keyfile: str | None = None,
        ssl_password: str | None = None,
        ssl_crlfile: str | None = None,
        api_version: tuple[int, ...] | None = None,
        bootstrap_timeout_ms: int = 30_000,
        selector: type[selectors.BaseSelector] = selectors.DefaultSelector,
        sasl_mechanism: Literal["PLAIN", "GSSAPI", "OAUTHBEARER", "SCRAM-SHA-256", "SCRAM-SHA-512"] | None = None,
        sasl_plain_username: str | None = None,
        sasl_plain_password: str | None = None,
        sasl_kerberos_name: object | None = None,
        sasl_kerberos_service_name: str = "kafka",
        sasl_kerberos_domain_name: str | None = None,
        sasl_oauth_token_provider: AbstractTokenProvider | None = None,
        proxy_url: str | None = None,
        socks5_proxy: str | None = None,
        metric_reporters: Sequence[type[object]] = [],
        metrics_num_samples: int = 2,
        metrics_sample_window_ms: int = 30_000,
        kafka_client: Callable[..., object] = ...,
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def close(self) -> None:
        """Close the KafkaAdminClient connection to the Kafka broker."""
        ...

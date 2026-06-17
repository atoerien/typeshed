"""Core protocol implementation"""

from _typeshed import FileDescriptorOrPath
from collections.abc import Callable, Iterable, Mapping, Sequence
from logging import Logger
from socket import socket
from threading import Condition, Event, Lock, Thread
from typing import Any, Protocol, TypeAlias, type_check_only

from paramiko.auth_handler import AuthHandler, AuthOnlyHandler, _InteractiveCallback
from paramiko.channel import Channel
from paramiko.message import Message
from paramiko.packet import Packetizer
from paramiko.pkey import PKey
from paramiko.proxy import ProxyCommand
from paramiko.server import ServerInterface, SubsystemHandler
from paramiko.sftp_client import SFTPClient
from paramiko.util import ClosingContextManager

_Addr: TypeAlias = tuple[str, int]
_SocketLike: TypeAlias = str | _Addr | socket | Channel | ProxyCommand

@type_check_only
class _KexEngine(Protocol):
    def start_kex(self) -> None: ...
    def parse_next(self, ptype: int, m: Message) -> None: ...

class Transport(Thread, ClosingContextManager):
    daemon: bool
    sock: socket | Channel

    packetizer: Packetizer
    local_version: str
    remote_version: str
    local_cipher: str
    local_kex_init: bytes | None
    local_mac: str | None
    local_compression: str | None
    session_id: bytes | None
    host_key_type: str | None
    host_key: PKey | None

    kex_engine: _KexEngine | None
    H: bytes | None
    K: int | None

    initial_kex_done: bool
    in_kex: bool
    authenticated: bool
    lock: Lock

    channel_events: dict[int, Event]
    channels_seen: dict[int, bool]
    default_max_packet_size: int
    default_window_size: int

    saved_exception: Exception | None
    clear_to_send: Event
    clear_to_send_lock: Lock
    clear_to_send_timeout: float
    log_name: str
    logger: Logger
    auth_handler: AuthHandler | None
    global_response: Message | None
    completion_event: Event | None
    banner_timeout: float
    handshake_timeout: float
    auth_timeout: float
    channel_timeout: float
    disabled_algorithms: Mapping[str, Iterable[str]] | None
    server_sig_algs: bool

    server_mode: bool
    server_object: ServerInterface | None
    server_key_dict: dict[str, PKey]
    server_accepts: list[Channel]
    server_accept_cv: Condition
    subsystem_table: dict[str, tuple[type[SubsystemHandler], tuple[Any, ...], dict[str, Any]]]

    def __init__(
        self,
        sock: _SocketLike,
        default_window_size: int = 2097152,
        default_max_packet_size: int = 32768,
        disabled_algorithms: Mapping[str, Iterable[str]] | None = None,
        server_sig_algs: bool = True,
        strict_kex: bool = True,
        packetizer_class: type[Packetizer] | None = None,
    ) -> None:
        """
        Create a new SSH session over an existing socket, or socket-like
        object.  This only creates the `.Transport` object; it doesn't begin
        the SSH session yet.  Use `connect` or `start_client` to begin a client
        session, or `start_server` to begin a server session.

        If the object is not actually a socket, it must have the following
        methods:

        - ``send(bytes)``: Writes from 1 to ``len(bytes)`` bytes, and returns
          an int representing the number of bytes written.  Returns
          0 or raises ``EOFError`` if the stream has been closed.
        - ``recv(int)``: Reads from 1 to ``int`` bytes and returns them as a
          string.  Returns 0 or raises ``EOFError`` if the stream has been
          closed.
        - ``close()``: Closes the socket.
        - ``settimeout(n)``: Sets a (float) timeout on I/O operations.

        For ease of use, you may also pass in an address (as a tuple) or a host
        string as the ``sock`` argument.  (A host string is a hostname with an
        optional port (separated by ``":"``) which will be converted into a
        tuple of ``(hostname, port)``.)  A socket will be connected to this
        address and used for communication.  Exceptions from the ``socket``
        call may be thrown in this case.

        .. note::
            Modifying the the window and packet sizes might have adverse
            effects on your channels created from this transport. The default
            values are the same as in the OpenSSH code base and have been
            battle tested.

        :param socket sock:
            a socket or socket-like object to create the session over.
        :param int default_window_size:
            sets the default window size on the transport. (defaults to
            2097152)
        :param int default_max_packet_size:
            sets the default max packet size on the transport. (defaults to
            32768)
        :param bool gss_kex:
            Whether to enable GSSAPI key exchange when GSSAPI is in play.
            Default: ``False``.
        :param bool gss_deleg_creds:
            Whether to enable GSSAPI credential delegation when GSSAPI is in
            play. Default: ``True``.
        :param dict disabled_algorithms:
            If given, must be a dictionary mapping algorithm type to an
            iterable of algorithm identifiers, which will be disabled for the
            lifetime of the transport.

            Keys should match the last word in the class' builtin algorithm
            tuple attributes, such as ``"ciphers"`` to disable names within
            ``_preferred_ciphers``; or ``"kex"`` to disable something defined
            inside ``_preferred_kex``. Values should exactly match members of
            the matching attribute.

            For example, if you need to disable
            ``diffie-hellman-group16-sha512`` key exchange (perhaps because
            your code talks to a server which implements it differently from
            Paramiko), specify ``disabled_algorithms={"kex":
            ["diffie-hellman-group16-sha512"]}``.
        :param bool server_sig_algs:
            Whether to send an extra message to compatible clients, in server
            mode, with a list of supported pubkey algorithms. Default:
            ``True``.
        :param bool strict_kex:
            Whether to advertise (and implement, if client also advertises
            support for) a "strict kex" mode for safer handshaking. Default:
            ``True``.
        :param packetizer_class:
            Which class to use for instantiating the internal packet handler.
            Default: ``None`` (i.e.: use `Packetizer` as normal).

        .. versionchanged:: 1.15
            Added the ``default_window_size`` and ``default_max_packet_size``
            arguments.
        .. versionchanged:: 1.15
            Added the ``gss_kex`` and ``gss_deleg_creds`` kwargs.
        .. versionchanged:: 2.6
            Added the ``disabled_algorithms`` kwarg.
        .. versionchanged:: 2.9
            Added the ``server_sig_algs`` kwarg.
        .. versionchanged:: 3.4
            Added the ``strict_kex`` kwarg.
        .. versionchanged:: 3.4
            Added the ``packetizer_class`` kwarg.
        """
        ...
    @property
    def preferred_ciphers(self) -> Sequence[str]: ...
    @property
    def preferred_macs(self) -> Sequence[str]: ...
    @property
    def preferred_keys(self) -> Sequence[str]: ...
    @property
    def preferred_pubkeys(self) -> Sequence[str]: ...
    @property
    def preferred_kex(self) -> Sequence[str]: ...
    @property
    def preferred_compression(self) -> Sequence[str]: ...
    def atfork(self) -> None: ...
    def get_security_options(self) -> SecurityOptions: ...
    def start_client(self, event: Event | None = None, timeout: float | None = None) -> None: ...
    def start_server(self, event: Event | None = None, server: ServerInterface | None = None) -> None: ...
    def add_server_key(self, key: PKey) -> None: ...
    def get_server_key(self) -> PKey | None: ...
    @staticmethod
    def load_server_moduli(filename: FileDescriptorOrPath | None = None) -> bool:
        """
        (optional)
        Load a file of prime moduli for use in doing group-exchange key
        negotiation in server mode.  It's a rather obscure option and can be
        safely ignored.

        In server mode, the remote client may request "group-exchange" key
        negotiation, which asks the server to send a random prime number that
        fits certain criteria.  These primes are pretty difficult to compute,
        so they can't be generated on demand.  But many systems contain a file
        of suitable primes (usually named something like ``/etc/ssh/moduli``).
        If you call `load_server_moduli` and it returns ``True``, then this
        file of primes has been loaded and we will support "group-exchange" in
        server mode.  Otherwise server mode will just claim that it doesn't
        support that method of key negotiation.

        :param str filename:
            optional path to the moduli file, if you happen to know that it's
            not in a standard location.
        :return:
            True if a moduli file was successfully loaded; False otherwise.

        .. note:: This has no effect when used in client mode.
        """
        ...
    def close(self) -> None:
        """Close this session, and any open channels that are tied to it."""
        ...
    def get_remote_server_key(self) -> PKey:
        """
        Return the host key of the server (in client mode).

        .. note::
            Previously this call returned a tuple of ``(key type, key
            string)``. You can get the same effect by calling `.PKey.get_name`
            for the key type, and ``str(key)`` for the key string.

        :raises: `.SSHException` -- if no session is currently active.

        :return: public key (`.PKey`) of the remote server
        """
        ...
    def is_active(self) -> bool:
        """
        Return true if this session is active (open).

        :return:
            True if the session is still active (open); False if the session is
            closed
        """
        ...
    def open_session(
        self, window_size: int | None = None, max_packet_size: int | None = None, timeout: float | None = None
    ) -> Channel:
        """
        Request a new channel to the server, of type ``"session"``.  This is
        just an alias for calling `open_channel` with an argument of
        ``"session"``.

        .. note:: Modifying the the window and packet sizes might have adverse
            effects on the session created. The default values are the same
            as in the OpenSSH code base and have been battle tested.

        :param int window_size:
            optional window size for this session.
        :param int max_packet_size:
            optional max packet size for this session.

        :return: a new `.Channel`

        :raises:
            `.SSHException` -- if the request is rejected or the session ends
            prematurely

        .. versionchanged:: 1.13.4/1.14.3/1.15.3
            Added the ``timeout`` argument.
        .. versionchanged:: 1.15
            Added the ``window_size`` and ``max_packet_size`` arguments.
        """
        ...
    def open_x11_channel(self, src_addr: _Addr | None = None) -> Channel:
        """
        Request a new channel to the client, of type ``"x11"``.  This
        is just an alias for ``open_channel('x11', src_addr=src_addr)``.

        :param tuple src_addr:
            the source address (``(str, int)``) of the x11 server (port is the
            x11 port, ie. 6010)
        :return: a new `.Channel`

        :raises:
            `.SSHException` -- if the request is rejected or the session ends
            prematurely
        """
        ...
    def open_forward_agent_channel(self) -> Channel:
        """
        Request a new channel to the client, of type
        ``"auth-agent@openssh.com"``.

        This is just an alias for ``open_channel('auth-agent@openssh.com')``.

        :return: a new `.Channel`

        :raises: `.SSHException` --
            if the request is rejected or the session ends prematurely
        """
        ...
    def open_forwarded_tcpip_channel(self, src_addr: _Addr, dest_addr: _Addr) -> Channel:
        """
        Request a new channel back to the client, of type ``forwarded-tcpip``.

        This is used after a client has requested port forwarding, for sending
        incoming connections back to the client.

        :param src_addr: originator's address
        :param dest_addr: local (server) connected address
        """
        ...
    def open_channel(
        self,
        kind: str,
        dest_addr: _Addr | None = None,
        src_addr: _Addr | None = None,
        window_size: int | None = None,
        max_packet_size: int | None = None,
        timeout: float | None = None,
    ) -> Channel:
        """
        Request a new channel to the server. `Channels <.Channel>` are
        socket-like objects used for the actual transfer of data across the
        session. You may only request a channel after negotiating encryption
        (using `connect` or `start_client`) and authenticating.

        .. note:: Modifying the the window and packet sizes might have adverse
            effects on the channel created. The default values are the same
            as in the OpenSSH code base and have been battle tested.

        :param str kind:
            the kind of channel requested (usually ``"session"``,
            ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``)
        :param tuple dest_addr:
            the destination address (address + port tuple) of this port
            forwarding, if ``kind`` is ``"forwarded-tcpip"`` or
            ``"direct-tcpip"`` (ignored for other channel types)
        :param src_addr: the source address of this port forwarding, if
            ``kind`` is ``"forwarded-tcpip"``, ``"direct-tcpip"``, or ``"x11"``
        :param int window_size:
            optional window size for this session.
        :param int max_packet_size:
            optional max packet size for this session.
        :param float timeout:
            optional timeout opening a channel, default 3600s (1h)

        :return: a new `.Channel` on success

        :raises:
            `.SSHException` -- if the request is rejected, the session ends
            prematurely or there is a timeout opening a channel

        .. versionchanged:: 1.15
            Added the ``window_size`` and ``max_packet_size`` arguments.
        """
        ...
    def request_port_forward(
        self, address: str, port: int, handler: Callable[[Channel, _Addr, _Addr], object] | None = None
    ) -> int:
        """
        Ask the server to forward TCP connections from a listening port on
        the server, across this SSH session.

        If a handler is given, that handler is called from a different thread
        whenever a forwarded connection arrives.  The handler parameters are::

            handler(
                channel,
                (origin_addr, origin_port),
                (server_addr, server_port),
            )

        where ``server_addr`` and ``server_port`` are the address and port that
        the server was listening on.

        If no handler is set, the default behavior is to send new incoming
        forwarded connections into the accept queue, to be picked up via
        `accept`.

        :param str address: the address to bind when forwarding
        :param int port:
            the port to forward, or 0 to ask the server to allocate any port
        :param callable handler:
            optional handler for incoming forwarded connections, of the form
            ``func(Channel, (str, int), (str, int))``.

        :return: the port number (`int`) allocated by the server

        :raises:
            `.SSHException` -- if the server refused the TCP forward request
        """
        ...
    def cancel_port_forward(self, address: str, port: int) -> None:
        """
        Ask the server to cancel a previous port-forwarding request.  No more
        connections to the given address & port will be forwarded across this
        ssh connection.

        :param str address: the address to stop forwarding
        :param int port: the port to stop forwarding
        """
        ...
    def open_sftp_client(self) -> SFTPClient | None:
        """
        Create an SFTP client channel from an open transport.  On success, an
        SFTP session will be opened with the remote host, and a new
        `.SFTPClient` object will be returned.

        :return:
            a new `.SFTPClient` referring to an sftp session (channel) across
            this transport
        """
        ...
    def send_ignore(self, byte_count: int | None = None) -> None:
        """
        Send a junk packet across the encrypted link.  This is sometimes used
        to add "noise" to a connection to confuse would-be attackers.  It can
        also be used as a keep-alive for long lived connections traversing
        firewalls.

        :param int byte_count:
            the number of random bytes to send in the payload of the ignored
            packet -- defaults to a random number from 10 to 41.
        """
        ...
    def renegotiate_keys(self) -> None:
        """
        Force this session to switch to new keys.  Normally this is done
        automatically after the session hits a certain number of packets or
        bytes sent or received, but this method gives you the option of forcing
        new keys whenever you want.  Negotiating new keys causes a pause in
        traffic both ways as the two sides swap keys and do computations.  This
        method returns when the session has switched to new keys.

        :raises:
            `.SSHException` -- if the key renegotiation failed (which causes
            the session to end)
        """
        ...
    def set_keepalive(self, interval: float) -> None:
        """
        Turn on/off keepalive packets (default is off).  If this is set, after
        ``interval`` seconds without sending any data over the connection, a
        "keepalive" packet will be sent (and ignored by the remote host).  This
        can be useful to keep connections alive over a NAT, for example.

        :param int interval:
            seconds to wait before sending a keepalive packet (or
            0 to disable keepalives).
        """
        ...
    def global_request(self, kind: str, data: Iterable[Any] | None = None, wait: bool = True) -> Message | None:
        """
        Make a global request to the remote host.  These are normally
        extensions to the SSH2 protocol.

        :param str kind: name of the request.
        :param tuple data:
            an optional tuple containing additional data to attach to the
            request.
        :param bool wait:
            ``True`` if this method should not return until a response is
            received; ``False`` otherwise.
        :return:
            a `.Message` containing possible additional data if the request was
            successful (or an empty `.Message` if ``wait`` was ``False``);
            ``None`` if the request was denied.
        """
        ...
    def accept(self, timeout: float | None = None) -> Channel | None:
        """
        Return the next channel opened by the client over this transport, in
        server mode.  If no channel is opened before the given timeout,
        ``None`` is returned.

        :param int timeout:
            seconds to wait for a channel, or ``None`` to wait forever
        :return: a new `.Channel` opened by the client
        """
        ...
    def connect(
        self, hostkey: PKey | None = None, username: str = "", password: str | None = None, pkey: PKey | None = None
    ) -> None: ...
    def get_exception(self) -> Exception | None: ...
    def set_subsystem_handler(self, name: str, handler: type[SubsystemHandler], *larg: Any, **kwarg: Any) -> None: ...
    def is_authenticated(self) -> bool: ...
    def get_username(self) -> str | None: ...
    def get_banner(self) -> bytes | None: ...
    def auth_none(self, username: str) -> list[str]: ...
    def auth_password(self, username: str, password: str, event: Event | None = None, fallback: bool = True) -> list[str]: ...
    def auth_publickey(self, username: str, key: PKey, event: Event | None = None) -> list[str]: ...
    def auth_interactive(self, username: str, handler: _InteractiveCallback, submethods: str = "") -> list[str]: ...
    def auth_interactive_dumb(
        self, username: str, handler: _InteractiveCallback | None = None, submethods: str = ""
    ) -> list[str]: ...
    def set_log_channel(self, name: str) -> None: ...
    def get_log_channel(self) -> str: ...
    def set_hexdump(self, hexdump: bool) -> None: ...
    def get_hexdump(self) -> bool: ...
    def use_compression(self, compress: bool = True) -> None: ...
    def getpeername(self) -> tuple[str, int]: ...
    def stop_thread(self) -> None: ...
    def run(self) -> None: ...

class SecurityOptions:
    """
    Simple object containing the security preferences of an ssh transport.
    These are tuples of acceptable ciphers, digests, key types, and key
    exchange algorithms, listed in order of preference.

    Changing the contents and/or order of these fields affects the underlying
    `.Transport` (but only if you change them before starting the session).
    If you try to add an algorithm that paramiko doesn't recognize,
    ``ValueError`` will be raised.  If you try to assign something besides a
    tuple to one of the fields, ``TypeError`` will be raised.
    """
    __slots__ = "_transport"
    def __init__(self, transport: Transport) -> None: ...

    @property
    def ciphers(self) -> Sequence[str]:
        """Symmetric encryption ciphers"""
        ...
    @ciphers.setter
    def ciphers(self, x: Sequence[str]) -> None:
        """Symmetric encryption ciphers"""
        ...

    @property
    def digests(self) -> Sequence[str]:
        """Digest (one-way hash) algorithms"""
        ...
    @digests.setter
    def digests(self, x: Sequence[str]) -> None:
        """Digest (one-way hash) algorithms"""
        ...

    @property
    def key_types(self) -> Sequence[str]:
        """Public-key algorithms"""
        ...
    @key_types.setter
    def key_types(self, x: Sequence[str]) -> None:
        """Public-key algorithms"""
        ...

    @property
    def kex(self) -> Sequence[str]:
        """Key exchange algorithms"""
        ...
    @kex.setter
    def kex(self, x: Sequence[str]) -> None:
        """Key exchange algorithms"""
        ...

    @property
    def compression(self) -> Sequence[str]:
        """Compression algorithms"""
        ...
    @compression.setter
    def compression(self, x: Sequence[str]) -> None:
        """Compression algorithms"""
        ...

class ChannelMap:
    def __init__(self) -> None: ...
    def put(self, chanid: int, chan: Channel) -> None: ...
    def get(self, chanid: int) -> Channel: ...
    def delete(self, chanid: int) -> None: ...
    def values(self) -> list[Channel]: ...
    def __len__(self) -> int: ...

class ServiceRequestingTransport(Transport):
    """
    Transport, but also handling service requests, like it oughtta!

    .. versionadded:: 3.2
    """
    def ensure_session(self) -> None: ...
    def get_auth_handler(self) -> AuthOnlyHandler: ...
    def auth_password(self, username: str, password: str, fallback: bool = True) -> list[str]: ...  # type: ignore[override]
    def auth_publickey(self, username: str, key: PKey) -> list[str]: ...  # type: ignore[override]

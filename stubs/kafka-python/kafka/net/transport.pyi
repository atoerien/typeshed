import socket
from _typeshed import Incomplete

class KafkaTCPTransport:
    host: Incomplete | None
    last_write: float
    last_read: float
    def __init__(self, net, sock, host=None) -> None: ...
    @property
    def last_activity(self) -> float: ...
    def is_closing(self) -> bool:
        """Return True if the transport is closing or closed."""
        ...
    def close(self) -> None:
        """
        Close the transport.

        Buffered data will be flushed asynchronously.  No more data
        will be received.  After all buffered data is flushed, the
        protocol's connection_lost() method will (eventually) be
        called with None as its argument.
        """
        ...
    def set_protocol(self, protocol) -> None:
        """Set a new protocol."""
        ...
    def get_protocol(self):
        """Return the current protocol."""
        ...
    def is_reading(self) -> bool:
        """Return True if the transport is receiving."""
        ...
    def pause_reading(self) -> None:
        """
        Pause the receiving end.

        No data will be passed to the protocol's data_received()
        method until resume_reading() is called.
        """
        ...
    def resume_reading(self) -> None:
        """
        Resume the receiving end.

        Data received will once again be passed to the protocol's
        data_received() method.
        """
        ...
    def set_write_buffer_limits(self, high=None, low=None):
        """
        Set the high- and low-water limits for write flow control.

        These two values control when to call the protocol's
        pause_writing() and resume_writing() methods.  If specified,
        the low-water limit must be less than or equal to the
        high-water limit.  Neither value can be negative.

        The defaults are implementation-specific.  If only the
        high-water limit is given, the low-water limit defaults to an
        implementation-specific value less than or equal to the
        high-water limit.  Setting high to zero forces low to zero as
        well, and causes pause_writing() to be called whenever the
        buffer becomes non-empty.  Setting low to zero causes
        resume_writing() to be called only once the buffer is empty.
        Use of zero for either limit is generally sub-optimal as it
        reduces opportunities for doing I/O and computation
        concurrently.
        """
        ...
    def get_write_buffer_size(self):
        """Return the current size of the write buffer."""
        ...
    def get_write_buffer_limits(self):
        """
        Get the high and low watermarks for write flow control.
        Return a tuple (low, high) where low and high are
        positive number of bytes.
        """
        ...
    def write(self, data) -> None:
        """
        Write some data bytes to the transport.

        This does not block; it buffers the data and arranges for it
        to be sent out asynchronously.
        """
        ...
    def writelines(self, list_of_data) -> None:
        """Write a list (or any iterable) of data bytes to the transport."""
        ...
    def write_eof(self) -> None:
        """
        Close the write end after flushing buffered data.

        (This is like typing ^D into a UNIX program reading from stdin.)

        Data may still be received.
        """
        ...
    def can_write_eof(self):
        """Return True if this transport supports write_eof(), False if not."""
        ...
    def abort(self, error=None) -> None:
        """
        Close the transport immediately.

        Buffered data will be lost.  No more data will be received.
        The protocol's connection_lost() method will (eventually) be
        called with None as its argument.
        """
        ...
    def abortConnection(self) -> None:
        """Close the connection abruptly."""
        ...
    def getHost(self) -> socket._RetAddress:
        """
        Similar to getPeer, but returns an address describing this side of the connection.

        Returns IPv4Address or IPv6Address.
        """
        ...
    def getPeer(self) -> socket._RetAddress:
        """
        Get the remote address of this connection.

        Treat this method with caution. It is the unfortunate result of the CGI and Jabber standards,
        but should not be considered reliable for the usual host of reasons;
        port forwarding, proxying, firewalls, IP masquerading, etc.

        Returns IPv4Address or IPv6Address.
        """
        ...
    def getTcpKeepAlive(self) -> int:
        """Return if SO_KEEPALIVE is enabled."""
        ...
    def getTcpNoDelay(self) -> int:
        """Return if TCP_NODELAY is enabled."""
        ...
    def loseWriteConnection(self) -> None:
        """Half-close the write side of a TCP connection."""
        ...
    def setTcpKeepAlive(self, enabled) -> None:
        """Enable/disable SO_KEEPALIVE."""
        ...
    def setTcpNoDelay(self, enabled) -> None:
        """Enable/disable TCP_NODELAY."""
        ...
    def loseConnection(self) -> None:
        """
        Close my connection, after writing all pending data.

        Note that if there is a registered producer on a transport it will not be closed until the producer has been unregistered.
        """
        ...
    def writeSequence(self, data) -> None:
        """
        Write an iterable of byte strings to the physical connection.

        If possible, make sure that all of the data is written to the socket at once,
        without first copying it all into a single byte string.
        """
        ...
    async def handshake(self) -> None: ...
    def host_port(self) -> str: ...

class KafkaSSLTransport(KafkaTCPTransport):
    DEFAULT_CONFIG: dict[str, Incomplete]
    ssl_config: dict[str, Incomplete]
    def __init__(self, net, sock, host=None, **configs) -> None: ...
    async def handshake(self) -> None: ...

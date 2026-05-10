"""
Base class extended by connection adapters. This extends the
connection.Connection class to encapsulate connection behavior but still
isolate socket and low level communication.
"""

import abc
from _typeshed import Incomplete
from collections.abc import Callable
from logging import Logger
from typing_extensions import Self

from ..adapters.utils.nbio_interface import AbstractIOServices, AbstractStreamProtocol
from ..connection import Connection, Parameters

LOGGER: Logger

class BaseConnection(Connection, metaclass=abc.ABCMeta):
    """
    BaseConnection class that should be extended by connection adapters.

    This class abstracts I/O loop and transport services from pika core.
    """
    def __init__(
        self,
        parameters: Parameters | None,
        on_open_callback: Callable[[Self], object] | None,
        on_open_error_callback: Callable[[Self, BaseException], object] | None,
        on_close_callback: Callable[[Self, BaseException], object] | None,
        nbio: AbstractIOServices,
        internal_connection_workflow: bool = True,
    ) -> None: ...
    @classmethod
    @abc.abstractmethod
    def create_connection(cls, connection_configs, on_done, custom_ioloop=None, workflow=None):
        """
        Asynchronously create a connection to an AMQP broker using the given
        configurations. Will attempt to connect using each config in the given
        order, including all compatible resolved IP addresses of the hostname
        supplied in each config, until one is established or all attempts fail.

        See also `_start_connection_workflow()`.

        :param sequence connection_configs: A sequence of one or more
            `pika.connection.Parameters`-based objects.
        :param callable on_done: as defined in
            `connection_workflow.AbstractAMQPConnectionWorkflow.start()`.
        :param object | None custom_ioloop: Provide a custom I/O loop that is
            native to the specific adapter implementation; if None, the adapter
            will use a default loop instance, which is typically a singleton.
        :param connection_workflow.AbstractAMQPConnectionWorkflow | None workflow:
            Pass an instance of an implementation of the
            `connection_workflow.AbstractAMQPConnectionWorkflow` interface;
            defaults to a `connection_workflow.AMQPConnectionWorkflow` instance
            with default values for optional args.
        :returns: Connection workflow instance in use. The user should limit
            their interaction with this object only to it's `abort()` method.
        :rtype: connection_workflow.AbstractAMQPConnectionWorkflow
        """
        ...
    @property
    def ioloop(self):
        """
        :returns: the native I/O loop instance underlying async services selected
            by user or the default selected by the specialized connection
            adapter (e.g., Twisted reactor, `asyncio.SelectorEventLoop`,
            `select_connection.IOLoop`, etc.)
        :rtype: object
        """
        ...

class _StreamingProtocolShim(AbstractStreamProtocol):
    connection_made: Incomplete
    connection_lost: Incomplete
    eof_received: Incomplete
    data_received: Incomplete
    conn: Incomplete
    def __init__(self, conn) -> None:
        """:param BaseConnection conn:"""
        ...
    def __getattr__(self, attr: str):
        """
        Proxy inexistent attribute requests to our connection instance
        so that AMQPConnectionWorkflow/AMQPConnector may treat the shim as an
        actual connection.
        """
        ...

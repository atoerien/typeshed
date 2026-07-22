"""
Implements `AMQPConnectionWorkflow` - the default workflow of performing
multiple TCP/[SSL]/AMQP connection attempts with timeouts and retries until one
succeeds or all attempts fail.

Defines the interface `AbstractAMQPConnectionWorkflow` that facilitates
implementing custom connection workflows.
"""

from _typeshed import Incomplete
from collections.abc import Callable, Iterable, Sequence

import pika.compat
import pika.connection
from pika.adapters.utils.nbio_interface import AbstractIOServices, AbstractStreamProtocol

class AMQPConnectorException(Exception):
    """Base exception for this module"""
    ...
class AMQPConnectorStackTimeout(AMQPConnectorException):
    """Overall TCP/[SSL]/AMQP stack connection attempt timed out."""
    ...
class AMQPConnectorAborted(AMQPConnectorException):
    """Asynchronous request was aborted"""
    ...
class AMQPConnectorWrongState(AMQPConnectorException):
    """
    AMQPConnector operation requested in wrong state, such as aborting after
    completion was reported.
    """
    ...

class AMQPConnectorPhaseErrorBase(AMQPConnectorException):
    exception: BaseException
    def __init__(self, exception: BaseException, *args: object) -> None: ...

    
    """
    exception: Incomplete
    def __init__(self, exception, *args) -> None:
        """
        :param BaseException exception: error that occurred while waiting for a
            subclass-specific protocol bring-up phase to complete.
        :param args: args for parent class
        """
        ...

class AMQPConnectorSocketConnectError(AMQPConnectorPhaseErrorBase):
    """Error connecting TCP socket to remote peer"""
    ...
class AMQPConnectorTransportSetupError(AMQPConnectorPhaseErrorBase):
    """
    Error setting up transport after TCP connected but before AMQP handshake.

    
    """
    ...
class AMQPConnectorAMQPHandshakeError(AMQPConnectorPhaseErrorBase):
    """Error during AMQP handshake"""
    ...
class AMQPConnectionWorkflowAborted(AMQPConnectorException):
    """AMQP Connection workflow was aborted."""
    ...
class AMQPConnectionWorkflowWrongState(AMQPConnectorException):
    """
    AMQP Connection Workflow operation requested in wrong state, such as
    aborting after completion was reported.
    """
    ...

class AMQPConnectionWorkflowFailed(AMQPConnectorException):
    exceptions: tuple[BaseException, ...]
    def __init__(self, exceptions: Iterable[BaseException], *args: object) -> None: ...

class AMQPConnector:
    def __init__(
        self, conn_factory: Callable[[pika.connection.Parameters], AbstractStreamProtocol], nbio: AbstractIOServices
    ) -> None: ...
    def start(
        self,
        addr_record: tuple[  # tuple taken result of socket.getaddrinfo
            int, int, int, str, tuple[str, int] | tuple[str, int, int, int] | tuple[int, bytes]
        ],
        conn_params: pika.connection.Parameters,
        on_done: Callable[[pika.connection.Connection | BaseException], None],
    ) -> None: ...
    def abort(self) -> None: ...

class AbstractAMQPConnectionWorkflow(pika.compat.AbstractBase):
    def start(
        self,
        connection_configs: Sequence[pika.connection.Parameters],
        connector_factory: Callable[..., Incomplete],
        native_loop,
        on_done: Callable[[pika.connection.Connection | AMQPConnectorException], None],
    ) -> None: ...
    def abort(self) -> None: ...

class AMQPConnectionWorkflow(AbstractAMQPConnectionWorkflow):
    def __init__(self, _until_first_amqp_attempt: bool = False) -> None: ...
    def set_io_services(self, nbio: AbstractIOServices) -> None: ...
    def start(
        self,
        connection_configs: Sequence[pika.connection.Parameters],
        connector_factory: Callable[..., Incomplete],
        native_loop,
        on_done: Callable[[pika.connection.Connection | AMQPConnectorException], None],
    ) -> None: ...
    def abort(self) -> None: ...

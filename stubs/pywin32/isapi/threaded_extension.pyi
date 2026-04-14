"""An ISAPI extension base class implemented using a thread-pool."""

import threading
from _typeshed import Unused
from collections.abc import Callable
from typing import Final

import isapi.simple

ISAPI_REQUEST: Final = 1
ISAPI_SHUTDOWN: Final = 2

class WorkerThread(threading.Thread):
    running: bool
    io_req_port: int
    extension: ThreadPoolExtension
    def __init__(self, extension: ThreadPoolExtension, io_req_port: int) -> None: ...
    def call_handler(self, cblock) -> None: ...

class ThreadPoolExtension(isapi.simple.SimpleExtension):
    """Base class for an ISAPI extension based around a thread-pool"""
    max_workers: int
    worker_shutdown_wait: int
    workers: list[WorkerThread]
    dispatch_map: dict[int, Callable[..., Unused]]
    io_req_port: int
    def GetExtensionVersion(self, vi) -> None: ...
    def HttpExtensionProc(self, control_block) -> int: ...
    def TerminateExtension(self, status) -> None: ...
    def DispatchConnection(self, errCode, bytes, key, overlapped) -> None: ...
    def Dispatch(self, ecb) -> None:
        """
        Overridden by the sub-class to handle connection requests.

        This class creates a thread-pool using a Windows completion port,
        and dispatches requests via this port.  Sub-classes can generally
        implement each connection request using blocking reads and writes, and
        the thread-pool will still provide decent response to the end user.

        The sub-class can set a max_workers attribute (default is 20).  Note
        that this generally does *not* mean 20 threads will all be concurrently
        running, via the magic of Windows completion ports.

        There is no default implementation - sub-classes must implement this.
        """
        ...
    def HandleDispatchError(self, ecb) -> None:
        """
        Handles errors in the Dispatch method.

        When a Dispatch method call fails, this method is called to handle
        the exception.  The default implementation formats the traceback
        in the browser.
        """
        ...

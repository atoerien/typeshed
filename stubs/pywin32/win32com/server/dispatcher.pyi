"""
Dispatcher

Please see policy.py for a discussion on dispatchers and policies
"""

from logging import Logger
from typing_extensions import TypeAlias

from win32com.server.policy import BasicWrapPolicy

class DispatcherBase:
    """
    The base class for all Dispatchers.

    This dispatcher supports wrapping all operations in exception handlers,
    and all the necessary delegation to the policy.

    This base class supports the printing of "unexpected" exceptions.  Note, however,
    that exactly where the output of print goes may not be useful!  A derived class may
    provide additional semantics for this.
    """
    policy: BasicWrapPolicy
    logger: Logger
    def __init__(self, policyClass, object) -> None: ...

class DispatcherTrace(DispatcherBase):
    """A dispatcher, which causes a 'print' line for each COM function called."""
    ...

class DispatcherWin32trace(DispatcherTrace):
    """A tracing dispatcher that sends its output to the win32trace remote collector."""
    def __init__(self, policyClass, object) -> None: ...

class DispatcherOutputDebugString(DispatcherTrace):
    """A tracing dispatcher that sends its output to win32api.OutputDebugString"""
    ...

DefaultDebugDispatcher: TypeAlias = DispatcherTrace

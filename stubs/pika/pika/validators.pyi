"""Common validation functions"""

from collections.abc import Callable
from typing import Literal, overload

def require_string(value: object, value_name: str) -> None:
    """
    Require that value is a string

    :raises: TypeError
    """
    ...
def require_callback(
    callback: object, callback_name: str = "callback"
) -> None: ...  # raise TypeError if callback is not callable

@overload
def rpc_completion_callback(callback: None) -> Literal[True]:
    """
    Verify callback is callable if not None

    :returns: boolean indicating nowait
    :rtype: bool
    :raises: TypeError
    """
    ...
@overload
def rpc_completion_callback(callback: Callable[..., object]) -> Literal[False]: ...

def zero_or_greater(name: str, value: str | float) -> None: ...

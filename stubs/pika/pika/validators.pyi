"""Common validation functions"""

from _typeshed import ConvertibleToInt
from collections.abc import Callable
from typing import Literal, overload

def require_string(value: object, value_name: str) -> None:
    """
    Require that value is a string

    :raises: TypeError
    """
    ...
def require_callback(
    callback: object, callback_name: str = "callback"  # raise TypeError if callback is not callable
) -> None:
    """
    Require that callback is callable and is not None

    :raises: TypeError
    """
    ...

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
def rpc_completion_callback(callback: Callable[..., object]) -> Literal[False]:
    """
    Verify callback is callable if not None

    :returns: boolean indicating nowait
    :rtype: bool
    :raises: TypeError
    """
    ...

def zero_or_greater(name: str, value: ConvertibleToInt) -> None:
    """
    Verify that value is zero or greater. If not, 'name'
    will be used in error message

    :raises: ValueError
    """
    ...

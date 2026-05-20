"""
Parameters deprecation
======================

.. _Tantale's Blog: https://tantale.github.io/
.. _Deprecated Parameters: https://tantale.github.io/articles/deprecated_params/

This module introduces a :class:`deprecated_params` decorator to specify that one (or more)
parameter(s) are deprecated: when the user executes a function with a deprecated parameter,
he will see a warning message in the console.

The decorator is customizable, the user can specify the deprecated parameter names
and associate to each of them a message providing the reason of the deprecation.
As with the :func:`~deprecated.classic.deprecated` decorator, the user can specify
a version number (using the *version* parameter) and also define the warning message category
(a subclass of :class:`Warning`) and when to display the messages (using the *action* parameter).

The complete study concerning the implementation of this decorator is available on the `Tantale's blog`_,
on the `Deprecated Parameters`_ page.
"""

from collections.abc import Callable, Iterable
from inspect import Signature
from typing import Any, ParamSpec, TypeVar

_P = ParamSpec("_P")
_R = TypeVar("_R")

class DeprecatedParams:
    """
    Decorator used to decorate a function which at least one
    of the parameters is deprecated.
    """
    messages: dict[str, str]
    category: type[Warning]
    def __init__(
        self, param: str | dict[str, str], reason: str = "", category: type[Warning] = DeprecationWarning  # noqa: Y011
    ) -> None: ...
    def populate_messages(self, param: str | dict[str, str], reason: str = "") -> None: ...
    def check_params(
        self, signature: Signature, *args: Any, **kwargs: Any  # args and kwargs passing to Signature.bind method
    ) -> list[str]: ...
    def warn_messages(self, messages: Iterable[str]) -> None: ...
    def __call__(self, f: Callable[_P, _R]) -> Callable[_P, _R]: ...

deprecated_params = DeprecatedParams

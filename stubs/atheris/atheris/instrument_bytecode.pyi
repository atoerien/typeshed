"""
This module provides the instrumentation functionality for atheris.

Mainly the function patch_code(), which can instrument a code object and the
helper class Instrumentor.
"""

from collections.abc import Callable
from typing import TypeVar

_T = TypeVar("_T")

def instrument_func(func: Callable[..., _T]) -> Callable[..., _T]:
    """Add Atheris instrumentation to a specific function."""
    ...
def instrument_all() -> None:
    """
    Add Atheris instrementation to all Python code already imported.

    This function is experimental.

    This function is able to instrument core library functions that can't be
    instrumented by instrument_func or instrument_imports, as those functions are
    used in the implementation of the instrumentation.
    """
    ...

"""
Routine to "compile" a .py file to a .pyc file.

This module has intimate knowledge of the format of .pyc files.
"""

import enum
from typing import AnyStr

__all__ = ["compile", "main", "PyCompileError", "PycInvalidationMode"]

class PyCompileError(Exception):
    """
    Exception raised when an error occurs while attempting to
    compile the file.

    To raise this exception, use

        raise PyCompileError(exc_type,exc_value,file[,msg])

    where

        exc_type:   exception type to be used in error message
                    type name can be accesses as class variable
                    'exc_type_name'

        exc_value:  exception value to be used in error message
                    can be accesses as class variable 'exc_value'

        file:       name of file being compiled to be used in error message
                    can be accesses as class variable 'file'

        msg:        string message to be written as error message
                    If no value is given, a default exception message will be
                    given, consistent with 'standard' py_compile output.
                    message (or default) can be accesses as class variable
                    'msg'
    """
    exc_type_name: str
    exc_value: BaseException
    file: str
    msg: str
    def __init__(self, exc_type: type[BaseException], exc_value: BaseException, file: str, msg: str = "") -> None: ...

class PycInvalidationMode(enum.Enum):
    """An enumeration."""
    TIMESTAMP = 1
    CHECKED_HASH = 2
    UNCHECKED_HASH = 3

def _get_default_invalidation_mode() -> PycInvalidationMode: ...
def compile(
    file: AnyStr,
    cfile: AnyStr | None = None,
    dfile: AnyStr | None = None,
    doraise: bool = False,
    optimize: int = -1,
    invalidation_mode: PycInvalidationMode | None = None,
    quiet: int = 0,
) -> AnyStr | None: ...
def main() -> None: ...

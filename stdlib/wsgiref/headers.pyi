"""
Manage HTTP Response Headers

Much of this module is red-handedly pilfered from email.message in the stdlib,
so portions are Copyright (C) 2001 Python Software Foundation, and were
written by Barry Warsaw.
"""

from re import Pattern
from typing import Final, TypeAlias, overload

_HeaderList: TypeAlias = list[tuple[str, str]]

tspecials: Final[Pattern[str]]  # undocumented

class Headers:
    """Manage a collection of HTTP response headers"""
    def __init__(self, headers: _HeaderList | None = None) -> None: ...
    def __len__(self) -> int: ...
    def __setitem__(self, name: str, val: str) -> None: ...
    def __delitem__(self, name: str) -> None: ...
    def __getitem__(self, name: str) -> str | None: ...
    def __contains__(self, name: str) -> bool: ...
    def get_all(self, name: str) -> list[str]: ...

    @overload
    def get(self, name: str, default: str) -> str:
        """Get the first header value for 'name', or return 'default'"""
        ...
    @overload
    def get(self, name: str, default: str | None = None) -> str | None: ...

    def keys(self) -> list[str]: ...
    def values(self) -> list[str]: ...
    def items(self) -> _HeaderList: ...
    def __bytes__(self) -> bytes: ...
    def setdefault(self, name: str, value: str) -> str:
        """
        Return first matching header value for 'name', or 'value'

        If there is no header named 'name', add a new header with name 'name'
        and value 'value'.
        """
        ...
    def add_header(self, _name: str, _value: str | None, **_params: str | None) -> None:
        """
        Extended header setting.

        _name is the header field to add.  keyword arguments can be used to set
        additional parameters for the header field, with underscores converted
        to dashes.  Normally the parameter will be added as key="value" unless
        value is None, in which case only the key will be added.

        Example:

        h.add_header('content-disposition', 'attachment', filename='bud.gif')

        Note that unlike the corresponding 'email.message' method, this does
        *not* handle '(charset, language, value)' tuples: all values must be
        strings or None.
        """
        ...

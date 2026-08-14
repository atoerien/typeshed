from collections.abc import Collection
from typing import overload

@overload
def list_to_scope(scope: str | Collection[str]) -> str:
    """Convert a list of scopes to a space separated string."""
    ...
@overload
def list_to_scope(scope: None) -> None:
    """Convert a list of scopes to a space separated string."""
    ...

@overload
def scope_to_list(scope: str | Collection[str]) -> list[str]:
    """Convert a space separated string to a list of scopes."""
    ...
@overload
def scope_to_list(scope: None) -> None:
    """Convert a space separated string to a list of scopes."""
    ...

def extract_basic_authorization(headers: dict[str, str]) -> tuple[str, str] | tuple[str, None] | tuple[None, None]: ...

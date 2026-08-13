"""
Generate .pyi type stub files for dynamically created protocol classes.

Usage:
    python -m kafka.protocol.generate_stubs           # generate stubs
    python -m kafka.protocol.generate_stubs --check    # exit 1 if stubs are out of date
    python -m kafka.protocol.generate_stubs --dry-run  # print to stdout
"""

from _typeshed import Incomplete
from types import ModuleType
from typing import Final

SIMPLE_TYPE_MAP: Final[dict[str, str]]
MESSAGE_MODULES: Final[list[str]]

def resolve_type(field: object) -> str:
    """Convert a field object to a Python type annotation string."""
    ...
def emit_class(cls: type, indent: int = 0, base_name: str | None = None) -> list[str]:
    """Generate stub lines for a single protocol class."""
    ...
def discover_modules() -> dict[str, tuple[ModuleType, list[tuple[str, Incomplete]]]]:
    """
    Import all message modules and collect their exports.

    Returns dict mapping module file path to list of (name, obj) pairs.
    """
    ...
def generate_module(mod, exports) -> str:
    """Generate the complete .pyi file content for a module."""
    ...
def generate_all(dry_run: bool = False, check: bool = False) -> bool:
    """Generate all stub files. Returns True if all stubs are up to date."""
    ...

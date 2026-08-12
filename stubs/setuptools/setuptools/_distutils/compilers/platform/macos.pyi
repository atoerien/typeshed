"""macOS-specific compiler support."""

from collections.abc import Mapping
from typing import Any, Final, TypeVar

_MappingT = TypeVar("_MappingT", bound=Mapping[Any, Any])

VERSION_VAR: Final = "MACOSX_DEPLOYMENT_TARGET"

def customize_compiler(config_vars) -> None:
    """
    Apply macOS SDK/architecture fixups to build config vars, in place.

    A no-op off macOS. Mirrors distutils' historical ``_customize_macos`` to
    support interpreters from binary installers, where the user's build tools
    and OS version may differ from the system Python itself was built on.
    """
    ...
def _target_ver_from_syscfg():
    """The deployment target latched into the interpreter's configuration."""
    ...
def target_ver() -> str | None:
    """
    Return the version of macOS for which we are building.

    Defaults to the version latched in sysconfig when the interpreter was
    built, unless overridden by ``MACOSX_DEPLOYMENT_TARGET``. Returns None if
    neither source has a value.
    """
    ...
def inject_ver(env: _MappingT | None) -> _MappingT | dict[str, str | int] | None:
    """
    Ensure a subprocess inherits the deployment target the build was
    configured with, so extensions link against a consistent macOS version.
    """
    ...

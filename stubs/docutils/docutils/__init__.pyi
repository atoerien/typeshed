from typing import Any, ClassVar, Final, NamedTuple, type_check_only
from typing_extensions import Self

from docutils.transforms import Transform

__docformat__: Final = "reStructuredText"
__version__: Final[str]

@type_check_only
class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int
    release: bool

class VersionInfo(_VersionInfo):
    __slots__ = ()
    def __new__(
        cls, major: int = 0, minor: int = 0, micro: int = 0, releaselevel: str = "final", serial: int = 0, release: bool = True
    ) -> Self: ...

__version_info__: Final[VersionInfo]
__version_details__: Final[str]

class ApplicationError(Exception): ...
class DataError(ApplicationError): ...

class SettingsSpec:
    """
    Runtime setting specification base class.

    SettingsSpec subclass objects used by `docutils.frontend.OptionParser`.
    """
    settings_spec: ClassVar[tuple[Any, ...]]  # Mixed tuple structure; uses Any for flexibility in nested option definitions
    settings_defaults: ClassVar[dict[Any, Any] | None]
    settings_default_overrides: ClassVar[dict[Any, Any] | None]
    relative_path_settings: ClassVar[tuple[Any, ...]]
    config_section: ClassVar[str | None]
    config_section_dependencies: ClassVar[tuple[str, ...] | None]

class TransformSpec:
    """
    Runtime transform specification base class.

    Provides the interface to register "transforms" and helper functions
    to resolve references with a `docutils.transforms.Transformer`.

    https://docutils.sourceforge.io/docs/ref/transforms.html
    """
    def get_transforms(self) -> list[type[Transform]]:
        """Transforms required by this class.  Override in subclasses."""
        ...
    default_transforms: ClassVar[tuple[Any, ...]]
    unknown_reference_resolvers: ClassVar[list[Any]]

class Component(SettingsSpec, TransformSpec):
    """Base class for Docutils components."""
    component_type: ClassVar[str | None]
    supported: ClassVar[tuple[str, ...]]
    def supports(self, format: str) -> bool:
        """
        Is `format` supported by this component?

        To be used by transforms to ask the dependent component if it supports
        a certain input context or output format.
        """
        ...

from typing import TypeAlias

_VersionInfo: TypeAlias = tuple[int, int, int, str, int]

class _Feature:
    def __init__(self, optionalRelease: _VersionInfo, mandatoryRelease: _VersionInfo | None, compiler_flag: int) -> None: ...
    def getOptionalRelease(self) -> _VersionInfo:
        """
        Return first release in which this feature was recognized.

        This is a 5-tuple, of the same form as sys.version_info.
        """
        ...
    def getMandatoryRelease(self) -> _VersionInfo | None:
        """
        Return release in which this feature will become mandatory.

        This is a 5-tuple, of the same form as sys.version_info, or, if
        the feature was dropped, or the release date is undetermined, is None.
        """
        ...
    compiler_flag: int

absolute_import: _Feature
division: _Feature
generators: _Feature
nested_scopes: _Feature
print_function: _Feature
unicode_literals: _Feature
with_statement: _Feature
barry_as_FLUFL: _Feature
generator_stop: _Feature
annotations: _Feature

all_feature_names: list[str]  # undocumented

__all__ = [
    "all_feature_names",
    "absolute_import",
    "division",
    "generators",
    "nested_scopes",
    "print_function",
    "unicode_literals",
    "with_statement",
    "barry_as_FLUFL",
    "generator_stop",
    "annotations",
]

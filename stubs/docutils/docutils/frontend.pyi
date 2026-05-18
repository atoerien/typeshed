"""
Command-line and common processing for Docutils front-end tools.

This module is provisional.
Major changes will happen with the transition from the
"optparse" module to "arparse" in Docutils 2.0 or later.

Applications should use the high-level API provided by `docutils.core`.
See https://docutils.sourceforge.io/docs/api/runtime-settings.html.

Exports the following classes:

* `OptionParser`: Standard Docutils command-line processing.
  Deprecated. Will be replaced by an ArgumentParser.
* `Option`: Customized version of `optparse.Option`; validation support.
  Deprecated. Will be removed.
* `Values`: Runtime settings; objects are simple structs
  (``object.attribute``).  Supports cumulative list settings (attributes).
  Deprecated. Will be removed.
* `ConfigParser`: Standard Docutils config file processing.
  Provisional. Details will change.

Also exports the following functions:

Interface function:
  `get_default_settings()`.  New in 0.19.

Option callbacks:
  `store_multiple()`, `read_config_file()`. Deprecated. To be removed.

Setting validators:
  `validate_encoding()`, `validate_encoding_error_handler()`,
  `validate_encoding_and_error_handler()`,
  `validate_boolean()`, `validate_ternary()`,
  `validate_nonnegative_int()`, `validate_threshold()`,
  `validate_colon_separated_string_list()`,
  `validate_comma_separated_list()`,
  `validate_url_trailing_slash()`,
  `validate_dependency_file()`,
  `validate_strip_class()`
  `validate_smartquotes_locales()`.

  Provisional.

Misc:
  `make_paths_absolute()`, `filter_settings_spec()`. Provisional.
"""

import optparse
from _typeshed import Incomplete, StrPath
from collections.abc import Iterable, Mapping, Sequence
from configparser import RawConfigParser
from typing import Any, ClassVar, Final, Literal, Protocol, overload, type_check_only
from typing_extensions import deprecated

from docutils import SettingsSpec
from docutils.utils import DependencyList

__docformat__: Final = "reStructuredText"

@type_check_only
class _OptionValidator(Protocol):
    def __call__(
        self,
        setting: str,
        value: str | None,
        option_parser: OptionParser,
        /,
        config_parser: ConfigParser | None = None,
        config_section: str | None = None,
    ) -> Any: ...

@deprecated("Deprecated and will be removed with the switch to from optparse to argparse.")
def store_multiple(option: optparse.Option, opt: str, value, parser: OptionParser, *args: str, **kwargs) -> None:
    """
    Store multiple values in `parser.values`.  (Option callback.)

    Store `None` for each attribute named in `args`, and store the value for
    each key (attribute name) in `kwargs`.

    Deprecated. Will be removed with the switch to from optparse to argparse.
    """
    ...
@deprecated("Deprecated and will be removed with the switch to from optparse to argparse.")
def read_config_file(option: optparse.Option, opt: str, value, parser: OptionParser) -> None:
    """
    Read a configuration file during option processing.  (Option callback.)

    Deprecated. Will be removed with the switch to from optparse to argparse.
    """
    ...
def validate_encoding(
    setting: str,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> str: ...
def validate_encoding_error_handler(
    setting: str,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> str: ...
def validate_encoding_and_error_handler(
    setting: str,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> str:
    """
    Check/normalize encoding settings

    Side-effect: if an error handler is included in the value, it is inserted
    into the appropriate place as if it were a separate setting/option.

    All arguments except `value` are ignored
    (kept for compatibility with "optparse" module).
    If there is only one positional argument, it is interpreted as `value`.
    """
    ...
def validate_boolean(
    setting: str | bool,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> bool:
    """
    Check/normalize boolean settings:

    :True:  '1', 'on', 'yes', 'true'
    :False: '0', 'off', 'no','false', ''

    All arguments except `value` are ignored
    (kept for compatibility with "optparse" module).
    If there is only one positional argument, it is interpreted as `value`.
    """
    ...
def validate_ternary(
    setting: str | bool,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> str | bool | None:
    """
    Check/normalize three-value settings:

    :True:  '1', 'on', 'yes', 'true'
    :False: '0', 'off', 'no','false', ''
    :any other value: returned as-is.

    All arguments except `value` are ignored
    (kept for compatibility with "optparse" module).
    If there is only one positional argument, it is interpreted as `value`.
    """
    ...
def validate_nonnegative_int(
    setting: str | int,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> int: ...
def validate_threshold(
    setting: str | int,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> int: ...
def validate_colon_separated_string_list(
    setting: str | list[str],
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> list[str]: ...
def validate_comma_separated_list(
    setting: str | list[str],
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> list[str]:
    """
    Check/normalize list arguments (split at "," and strip whitespace).

    All arguments except `value` are ignored
    (kept for compatibility with "optparse" module).
    If there is only one positional argument, it is interpreted as `value`.
    """
    ...
def validate_math_output(
    setting: str,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> tuple[()] | tuple[str, str]:
    """
    Check "math-output" setting, return list with "format" and "options".

    See also https://docutils.sourceforge.io/docs/user/config.html#math-output

    Argument list for compatibility with "optparse" module.
    All arguments except `value` are ignored.
    If there is only one positional argument, it is interpreted as `value`.
    """
    ...
def validate_url_trailing_slash(
    setting: str,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> str: ...
def validate_dependency_file(
    setting: str | None,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> DependencyList: ...
def validate_strip_class(
    setting: str,
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> list[str]: ...
def validate_smartquotes_locales(
    setting: str | list[str | tuple[str, str]],
    value: str | None = None,
    option_parser: OptionParser | None = None,
    config_parser: ConfigParser | None = None,
    config_section: str | None = None,
) -> list[tuple[str, Sequence[str]]]:
    """
    Check/normalize a comma separated list of smart quote definitions.

    Return a list of (language-tag, quotes) string tuples.

    All arguments except `value` are ignored
    (kept for compatibility with "optparse" module).
    If there is only one positional argument, it is interpreted as `value`.
    """
    ...
def make_paths_absolute(
    pathdict: dict[str, list[StrPath] | StrPath], keys: tuple[str], base_path: StrPath | None = None
) -> None:
    """
    Interpret filesystem path settings relative to the `base_path` given.

    Paths are values in `pathdict` whose keys are in `keys`.  Get `keys` from
    `OptionParser.relative_path_settings`.
    """
    ...
@deprecated("The `frontend.make_one_path_absolute` will be removed in Docutils 2.0 or later.")
def make_one_path_absolute(base_path: StrPath, path: StrPath) -> str: ...
def filter_settings_spec(settings_spec, *exclude, **replace) -> tuple[Any, ...]:
    """
    Return a copy of `settings_spec` excluding/replacing some settings.

    `settings_spec` is a tuple of configuration settings
    (cf. `docutils.SettingsSpec.settings_spec`).

    Optional positional arguments are names of to-be-excluded settings.
    Keyword arguments are option specification replacements.
    (See the html4strict writer for an example.)
    """
    ...

@deprecated("The `frontend.Values` class will be removed in Docutils 2.0 or later.")
class Values(optparse.Values):
    """
    Storage for option values.

    Updates list attributes by extension rather than by replacement.
    Works in conjunction with the `OptionParser.lists` instance attribute.

    Deprecated. Will be removed when switching to the "argparse" module.
    """
    record_dependencies: DependencyList
    def __init__(self, defaults: dict[str, Any] | None = None) -> None: ...
    def update(self, other_dict: Values | Mapping[str, Incomplete], option_parser: OptionParser) -> None: ...
    def copy(self) -> Values:
        """Return a shallow copy of `self`."""
        ...
    def setdefault(self, name: str, default):
        """
        Return ``self.name`` or ``default``.

        If ``self.name`` is unset, set ``self.name = default``.
        """
        ...

@deprecated("The `frontend.Option` class will be removed in Docutils 2.0 or later.")
class Option(optparse.Option):
    """
    Add validation and override support to `optparse.Option`.

    Deprecated. Will be removed.
    """
    ATTRS: list[str]
    validator: _OptionValidator
    overrides: str | None
    def __init__(self, *args: str | None, **kwargs) -> None: ...

@deprecated(
    "The `frontend.OptionParser` class will be replaced by a subclass of `argparse.ArgumentParser` in Docutils 2.0 or later."
)
class OptionParser(optparse.OptionParser, SettingsSpec):
    """
    Settings parser for command-line and library use.

    The `settings_spec` specification here and in other Docutils components
    are merged to build the set of command-line options and runtime settings
    for this process.

    Common settings (defined below) and component-specific settings must not
    conflict.  Short options are reserved for common settings, and components
    are restricted to using long options.

    Deprecated.
    Will be replaced by a subclass of `argparse.ArgumentParser`.
    """
    standard_config_files: ClassVar[list[str]]
    threshold_choices: ClassVar[tuple[str, ...]]
    thresholds: ClassVar[dict[str, int]]
    booleans: ClassVar[dict[str, bool]]
    default_error_encoding: ClassVar[str]
    default_error_encoding_error_handler: ClassVar[str]
    config_section: ClassVar[str]
    version_template: ClassVar[str]
    details: str
    lists: dict[str, Literal[True]]
    config_files: list[str]
    relative_path_settings: ClassVar[tuple[str, ...]]
    version: str
    components: tuple[SettingsSpec, ...]
    def __init__(
        self,
        components: Iterable[SettingsSpec | type[SettingsSpec]] = (),
        defaults: Mapping[str, Any] | None = None,
        read_config_files: bool | None = False,
        *args,
        **kwargs,
    ) -> None:
        """
        Set up OptionParser instance.

        `components` is a list of Docutils components each containing a
        ``.settings_spec`` attribute.
        `defaults` is a mapping of setting default overrides.
        """
        ...
    def populate_from_components(self, components: Iterable[SettingsSpec]) -> None:
        """
        Collect settings specification from components.

        For each component, populate from the `SettingsSpec.settings_spec`
        structure, then from the `SettingsSpec.settings_defaults` dictionary.
        After all components have been processed, check for and populate from
        each component's `SettingsSpec.settings_default_overrides` dictionary.
        """
        ...
    @classmethod
    def get_standard_config_files(cls) -> Sequence[StrPath]:
        """Return list of config files, from environment or standard."""
        ...
    def get_standard_config_settings(self) -> Values: ...
    def get_config_file_settings(self, config_file: str) -> dict[str, Incomplete]:
        """Returns a dictionary containing appropriate config file settings."""
        ...
    def check_values(self, values: Values, args: list[str]) -> Values:
        """Store positional arguments as runtime settings."""
        ...
    def check_args(self, args: list[str]) -> tuple[str | None, str | None]: ...
    def get_default_values(self) -> Values:
        """Needed to get custom `Values` instances."""
        ...
    def get_option_by_dest(self, dest: str) -> Option:
        """
        Get an option by its dest.

        If you're supplying a dest which is shared by several options,
        it is undefined which option of those is returned.

        A KeyError is raised if there is no option with the supplied
        dest.
        """
        ...

class ConfigParser(RawConfigParser):
    """
    Parser for Docutils configuration files.

    See https://docutils.sourceforge.io/docs/user/config.html.

    Option key normalization includes conversion of '-' to '_'.

    Config file encoding is "utf-8". Encoding errors are reported
    and the affected file(s) skipped.

    This class is provisional and will change in future versions.
    """
    old_settings: ClassVar[dict[str, tuple[str, str]]]
    old_warning: ClassVar[str]
    not_utf8_error: ClassVar[str]

    @overload  # type: ignore[override]
    def read(self, filenames: str | Sequence[str]) -> list[str]: ...
    @overload
    @deprecated("The `option_parser` parameter is deprecated and will be removed in Docutils 0.24.")
    def read(self, filenames: str | Sequence[str], option_parser: OptionParser | None) -> list[str]: ...

    def handle_old_config(self, filename: str) -> None: ...
    def validate_settings(self, filename: str, option_parser: OptionParser) -> None:
        """
        Call the validator function and implement overrides on all applicable
        settings.
        """
        ...
    def optionxform(self, optionstr: str) -> str:
        """
        Lowercase and transform '-' to '_'.

        So the cmdline form of option names can be used in config files.
        """
        ...

class ConfigDeprecationWarning(FutureWarning):
    """Warning for deprecated configuration file features."""
    ...

def get_default_settings(*components: SettingsSpec) -> Values:
    """
    Return default runtime settings for `components`.

    Return a `frontend.Values` instance with defaults for generic Docutils
    settings and settings from the `components` (`SettingsSpec` instances).

    This corresponds to steps 1 and 2 in the `runtime settings priority`__.

    __ https://docutils.sourceforge.io/docs/api/runtime-settings.html
       #settings-priority
    """
    ...

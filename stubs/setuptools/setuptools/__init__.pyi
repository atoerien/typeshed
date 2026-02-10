"""Extensions to the 'distutils' for large or complex distributions"""

from _typeshed import Incomplete, StrPath
from abc import abstractmethod
from collections.abc import ItemsView, Iterable, Mapping, Sequence
from typing import Any, Literal, Protocol, TypedDict, TypeVar, overload, type_check_only
from typing_extensions import Never, NotRequired

from ._distutils.cmd import Command as _Command
from ._distutils.dist import Distribution as _Distribution
from ._distutils.extension import Extension as _Extension
from .command.alias import alias
from .command.bdist_egg import bdist_egg
from .command.bdist_rpm import bdist_rpm
from .command.bdist_wheel import bdist_wheel
from .command.build import build
from .command.build_clib import build_clib
from .command.build_ext import build_ext
from .command.build_py import build_py
from .command.develop import develop
from .command.dist_info import dist_info
from .command.easy_install import easy_install
from .command.editable_wheel import editable_wheel
from .command.egg_info import egg_info
from .command.install import install
from .command.install_egg_info import install_egg_info
from .command.install_lib import install_lib
from .command.install_scripts import install_scripts
from .command.rotate import rotate
from .command.saveopts import saveopts
from .command.sdist import sdist
from .command.setopt import setopt
from .depends import Require as Require
from .discovery import _Finder
from .dist import Distribution as Distribution
from .extension import Extension as Extension
from .warnings import SetuptoolsDeprecationWarning as SetuptoolsDeprecationWarning

_CommandT = TypeVar("_CommandT", bound=_Command)
_DistributionT = TypeVar("_DistributionT", bound=_Distribution, default=Distribution)
_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)

__all__ = [
    "setup",
    "Distribution",
    "Command",
    "Extension",
    "Require",
    "SetuptoolsDeprecationWarning",
    "find_packages",
    "find_namespace_packages",
]

__version__: str

# We need any Command subclass to be valid
# Any: pyright would accept using covariance in __setitem__, but mypy won't let a dict be assignable to this protocol
# This is unsound, but it's a quirk of setuptools' internals
@type_check_only
class _DictLike(Protocol[_KT, _VT_co]):
    # See note about using _VT_co instead of Any
    def get(self, key: _KT, default: Any | None = None, /) -> _VT_co | None: ...
    def items(self) -> ItemsView[_KT, _VT_co]: ...
    def keys(self) -> Iterable[_KT]: ...
    def __getitem__(self, key: _KT, /) -> _VT_co: ...
    def __contains__(self, x: object, /) -> bool: ...

@type_check_only
class _MutableDictLike(_DictLike[_KT, _VT_co], Protocol):
    # See note about using _VT_co instead of Any
    def __setitem__(self, key: _KT, value: Any, /) -> None: ...
    def setdefault(self, key: _KT, default: Any, /) -> _VT_co: ...

@type_check_only
class _BuildInfo(TypedDict):
    sources: list[str] | tuple[str, ...]
    obj_deps: NotRequired[dict[str, list[str] | tuple[str, ...]]]
    macros: NotRequired[list[tuple[str] | tuple[str, str | None]]]
    include_dirs: NotRequired[list[str]]
    cflags: NotRequired[list[str]]

find_packages = _Finder.find
find_namespace_packages = _Finder.find

def setup(
    *,
    # Attributes from distutils.dist.DistributionMetadata.set_*
    # These take priority over attributes from distutils.dist.DistributionMetadata.__init__
    keywords: str | Iterable[str] = ...,
    platforms: str | Iterable[str] = ...,
    classifiers: str | Iterable[str] = ...,
    requires: Iterable[str] = ...,
    provides: Iterable[str] = ...,
    obsoletes: Iterable[str] = ...,
    # Attributes from distutils.dist.DistributionMetadata.__init__
    # These take priority over attributes from distutils.dist.Distribution.__init__
    name: str | None = None,
    version: str | None = None,
    author: str | None = None,
    author_email: str | None = None,
    maintainer: str | None = None,
    maintainer_email: str | None = None,
    url: str | None = None,
    license: str | None = None,
    description: str | None = None,
    long_description: str | None = None,
    download_url: str | None = None,
    # Attributes from distutils.dist.Distribution.__init__ (except self.metadata)
    # These take priority over attributes from distutils.dist.Distribution.display_option_names
    verbose: bool = True,
    help: bool = False,
    cmdclass: _MutableDictLike[str, type[_Command]] = {},
    command_packages: str | list[str] | None = None,
    script_name: StrPath | None = ...,  # default is actually set in distutils.core.setup
    script_args: list[str] | None = ...,  # default is actually set in distutils.core.setup
    command_options: _MutableDictLike[str, _DictLike[str, tuple[str, str]]] = {},
    packages: list[str] | None = None,
    package_dir: Mapping[str, str] | None = None,
    py_modules: list[str] | None = None,
    libraries: list[tuple[str, _BuildInfo]] | None = None,
    headers: list[str] | None = None,
    ext_modules: Sequence[_Extension] | None = None,
    ext_package: str | None = None,
    include_dirs: list[str] | None = None,
    extra_path: Never = ...,  # Deprecated
    scripts: list[str] | None = None,
    data_files: list[tuple[str, Sequence[str]]] | None = None,
    password: str = "",
    command_obj: _MutableDictLike[str, _Command] = {},
    have_run: _MutableDictLike[str, bool] = {},
    # kwargs used directly in distutils.dist.Distribution.__init__
    options: Mapping[str, Mapping[str, str]] | None = None,
    licence: Never = ...,  # Deprecated
    # Attributes from distutils.dist.Distribution.display_option_names
    # (this can more easily be copied from the `if TYPE_CHECKING` block)
    help_commands: bool = False,
    fullname: str | Literal[False] = False,
    contact: str | Literal[False] = False,
    contact_email: str | Literal[False] = False,
    # kwargs used directly in setuptools.dist.Distribution.__init__
    # and attributes from setuptools.dist.Distribution.__init__
    package_data: _DictLike[str, list[str]] = {},
    dist_files: list[tuple[str, str, str]] = [],
    include_package_data: bool | None = None,
    exclude_package_data: _DictLike[str, list[str]] | None = None,
    src_root: str | None = None,
    dependency_links: list[str] = [],
    setup_requires: list[str] = [],
    # From Distribution._DISTUTILS_UNSUPPORTED_METADATA set in Distribution._set_metadata_defaults
    long_description_content_type: str | None = None,
    project_urls: _DictLike[Incomplete, Incomplete] = {},
    provides_extras: _MutableDictLike[Incomplete, Incomplete] = {},
    license_expression: str | None = None,
    license_file: Never = ...,  # Deprecated
    license_files: Iterable[str] | None = None,
    install_requires: str | Iterable[str] = [],
    extras_require: _DictLike[Incomplete, Incomplete] = {},
    # kwargs used directly in distutils.core.setup
    distclass: type[_DistributionT] = Distribution,  # type: ignore[assignment] # noqa: Y011
    # Custom Distributions could accept more params
    **attrs: Any,
) -> _DistributionT:
    """
    The gateway to the Distutils: do everything your setup script needs
    to do, in a highly flexible and user-driven way.  Briefly: create a
    Distribution instance; find and parse config files; parse the command
    line; run each Distutils command found there, customized by the options
    supplied to 'setup()' (as keyword arguments), in config files, and on
    the command line.

    The Distribution instance might be an instance of a class supplied via
    the 'distclass' keyword argument to 'setup'; if no such class is
    supplied, then the Distribution class (in dist.py) is instantiated.
    All other arguments to 'setup' (except for 'cmdclass') are used to set
    attributes of the Distribution instance.

    The 'cmdclass' argument, if supplied, is a dictionary mapping command
    names to command classes.  Each command encountered on the command line
    will be turned into a command class, which is in turn instantiated; any
    class found in 'cmdclass' is used in place of the default, which is
    (for command 'foo_bar') class 'foo_bar' in module
    'distutils.command.foo_bar'.  The command class must provide a
    'user_options' attribute which is a list of option specifiers for
    'distutils.fancy_getopt'.  Any command-line options between the current
    and the next command are used to set attributes of the current command
    object.

    When the entire command-line has been successfully parsed, calls the
    'run()' method on each command object in turn.  This method will be
    driven entirely by the Distribution object (which each command object
    has a reference to, thanks to its constructor), and the
    command-specific options that became attributes of each command
    object.
    """
    ...

class Command(_Command):
    """
    Setuptools internal actions are organized using a *command design pattern*.
    This means that each action (or group of closely related actions) executed during
    the build should be implemented as a ``Command`` subclass.

    These commands are abstractions and do not necessarily correspond to a command that
    can (or should) be executed via a terminal, in a CLI fashion (although historically
    they would).

    When creating a new command from scratch, custom defined classes **SHOULD** inherit
    from ``setuptools.Command`` and implement a few mandatory methods.
    Between these mandatory methods, are listed:
    :meth:`initialize_options`, :meth:`finalize_options` and :meth:`run`.

    A useful analogy for command classes is to think of them as subroutines with local
    variables called "options".  The options are "declared" in :meth:`initialize_options`
    and "defined" (given their final values, aka "finalized") in :meth:`finalize_options`,
    both of which must be defined by every command class. The "body" of the subroutine,
    (where it does all the work) is the :meth:`run` method.
    Between :meth:`initialize_options` and :meth:`finalize_options`, ``setuptools`` may set
    the values for options/attributes based on user's input (or circumstance),
    which means that the implementation should be careful to not overwrite values in
    :meth:`finalize_options` unless necessary.

    Please note that other commands (or other parts of setuptools) may also overwrite
    the values of the command's options/attributes multiple times during the build
    process.
    Therefore it is important to consistently implement :meth:`initialize_options` and
    :meth:`finalize_options`. For example, all derived attributes (or attributes that
    depend on the value of other attributes) **SHOULD** be recomputed in
    :meth:`finalize_options`.

    When overwriting existing commands, custom defined classes **MUST** abide by the
    same APIs implemented by the original class. They also **SHOULD** inherit from the
    original class.
    """
    command_consumes_arguments: bool
    distribution: Distribution
    dry_run: bool
    # Any: Dynamic command subclass attributes
    def __init__(self, dist: Distribution, **kw: Any) -> None:
        """
        Construct the command for dist, updating
        vars(self) with any keyword parameters.
        """
        ...
    # Note: Commands that setuptools doesn't re-expose are considered deprecated (they must be imported from distutils directly)
    # So we're not listing them here. This list comes directly from the setuptools/command folder. Minus the test command.
    @overload  # type: ignore[override]
    def get_finalized_command(self, command: Literal["alias"], create: bool | Literal[0, 1] = 1) -> alias:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["bdist_egg"], create: bool | Literal[0, 1] = 1) -> bdist_egg:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["bdist_rpm"], create: bool | Literal[0, 1] = 1) -> bdist_rpm:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["bdist_wheel"], create: bool | Literal[0, 1] = 1) -> bdist_wheel:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["build"], create: bool | Literal[0, 1] = 1) -> build:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["build_clib"], create: bool | Literal[0, 1] = 1) -> build_clib:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["build_ext"], create: bool | Literal[0, 1] = 1) -> build_ext:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["build_py"], create: bool | Literal[0, 1] = 1) -> build_py:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["develop"], create: bool | Literal[0, 1] = 1) -> develop:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["dist_info"], create: bool | Literal[0, 1] = 1) -> dist_info:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["easy_install"], create: bool | Literal[0, 1] = 1) -> easy_install:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["editable_wheel"], create: bool | Literal[0, 1] = 1) -> editable_wheel:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["egg_info"], create: bool | Literal[0, 1] = 1) -> egg_info:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["install"], create: bool | Literal[0, 1] = 1) -> install:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(
        self, command: Literal["install_egg_info"], create: bool | Literal[0, 1] = 1
    ) -> install_egg_info:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["install_lib"], create: bool | Literal[0, 1] = 1) -> install_lib:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["install_scripts"], create: bool | Literal[0, 1] = 1) -> install_scripts:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["rotate"], create: bool | Literal[0, 1] = 1) -> rotate:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["saveopts"], create: bool | Literal[0, 1] = 1) -> saveopts:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["sdist"], create: bool | Literal[0, 1] = 1) -> sdist:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: Literal["setopt"], create: bool | Literal[0, 1] = 1) -> setopt:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload
    def get_finalized_command(self, command: str, create: bool | Literal[0, 1] = 1) -> Command:
        """
        Wrapper around Distribution's 'get_command_obj()' method: find
        (create if necessary and 'create' is true) the command object for
        'command', call its 'ensure_finalized()' method, and return the
        finalized command object.
        """
        ...
    @overload  # type: ignore[override] # Extra **kw param
    def reinitialize_command(self, command: Literal["alias"], reinit_subcommands: bool = False, **kw) -> alias: ...
    @overload
    def reinitialize_command(self, command: Literal["bdist_egg"], reinit_subcommands: bool = False, **kw) -> bdist_egg: ...
    @overload
    def reinitialize_command(self, command: Literal["bdist_rpm"], reinit_subcommands: bool = False, **kw) -> bdist_rpm: ...
    @overload
    def reinitialize_command(self, command: Literal["bdist_wheel"], reinit_subcommands: bool = False, **kw) -> bdist_wheel: ...
    @overload
    def reinitialize_command(self, command: Literal["build"], reinit_subcommands: bool = False, **kw) -> build: ...
    @overload
    def reinitialize_command(self, command: Literal["build_clib"], reinit_subcommands: bool = False, **kw) -> build_clib: ...
    @overload
    def reinitialize_command(self, command: Literal["build_ext"], reinit_subcommands: bool = False, **kw) -> build_ext: ...
    @overload
    def reinitialize_command(self, command: Literal["build_py"], reinit_subcommands: bool = False, **kw) -> build_py: ...
    @overload
    def reinitialize_command(self, command: Literal["develop"], reinit_subcommands: bool = False, **kw) -> develop: ...
    @overload
    def reinitialize_command(self, command: Literal["dist_info"], reinit_subcommands: bool = False, **kw) -> dist_info: ...
    @overload
    def reinitialize_command(self, command: Literal["easy_install"], reinit_subcommands: bool = False, **kw) -> easy_install: ...
    @overload
    def reinitialize_command(
        self, command: Literal["editable_wheel"], reinit_subcommands: bool = False, **kw
    ) -> editable_wheel: ...
    @overload
    def reinitialize_command(self, command: Literal["egg_info"], reinit_subcommands: bool = False, **kw) -> egg_info: ...
    @overload
    def reinitialize_command(self, command: Literal["install"], reinit_subcommands: bool = False, **kw) -> install: ...
    @overload
    def reinitialize_command(
        self, command: Literal["install_egg_info"], reinit_subcommands: bool = False, **kw
    ) -> install_egg_info: ...
    @overload
    def reinitialize_command(self, command: Literal["install_lib"], reinit_subcommands: bool = False, **kw) -> install_lib: ...
    @overload
    def reinitialize_command(
        self, command: Literal["install_scripts"], reinit_subcommands: bool = False, **kw
    ) -> install_scripts: ...
    @overload
    def reinitialize_command(self, command: Literal["rotate"], reinit_subcommands: bool = False, **kw) -> rotate: ...
    @overload
    def reinitialize_command(self, command: Literal["saveopts"], reinit_subcommands: bool = False, **kw) -> saveopts: ...
    @overload
    def reinitialize_command(self, command: Literal["sdist"], reinit_subcommands: bool = False, **kw) -> sdist: ...
    @overload
    def reinitialize_command(self, command: Literal["setopt"], reinit_subcommands: bool = False, **kw) -> setopt: ...
    @overload
    def reinitialize_command(self, command: str, reinit_subcommands: bool = False, **kw) -> Command: ...
    @overload
    def reinitialize_command(self, command: _CommandT, reinit_subcommands: bool = False, **kw) -> _CommandT: ...
    @abstractmethod
    def initialize_options(self) -> None:
        """
        Set or (reset) all options/attributes/caches used by the command
        to their default values. Note that these values may be overwritten during
        the build.
        """
        ...
    @abstractmethod
    def finalize_options(self) -> None:
        """
        Set final values for all options/attributes used by the command.
        Most of the time, each option/attribute/cache should only be set if it does not
        have any value yet (e.g. ``if self.attr is None: self.attr = val``).
        """
        ...
    @abstractmethod
    def run(self) -> None:
        """
        Execute the actions intended by the command.
        (Side effects **SHOULD** only take place when :meth:`run` is executed,
        for example, creating new files or writing to the terminal output).
        """
        ...

class sic(str):
    """Treat this string as-is (https://en.wikipedia.org/wiki/Sic)"""
    ...

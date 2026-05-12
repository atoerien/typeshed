"""Utilities to support packages."""

import sys
from _typeshed import StrOrBytesPath, SupportsRead
from _typeshed.importlib import LoaderProtocol, MetaPathFinderProtocol, PathEntryFinderProtocol
from collections.abc import Callable, Iterable, Iterator
from typing import IO, Any, NamedTuple, TypeVar
from typing_extensions import deprecated

__all__ = [
    "get_importer",
    "iter_importers",
    "walk_packages",
    "iter_modules",
    "get_data",
    "read_code",
    "extend_path",
    "ModuleInfo",
]
if sys.version_info < (3, 14):
    __all__ += ["get_loader", "find_loader"]
if sys.version_info < (3, 12):
    __all__ += ["ImpImporter", "ImpLoader"]

_PathT = TypeVar("_PathT", bound=Iterable[str])

class ModuleInfo(NamedTuple):
    """A namedtuple with minimal info about a module."""
    module_finder: MetaPathFinderProtocol | PathEntryFinderProtocol
    name: str
    ispkg: bool

def extend_path(path: _PathT, name: str) -> _PathT:
    """
    Extend a package's path.

    Intended use is to place the following code in a package's __init__.py:

        from pkgutil import extend_path
        __path__ = extend_path(__path__, __name__)

    For each directory on sys.path that has a subdirectory that
    matches the package name, add the subdirectory to the package's
    __path__.  This is useful if one wants to distribute different
    parts of a single logical package as multiple directories.

    It also looks for *.pkg files beginning where * matches the name
    argument.  This feature is similar to *.pth files (see site.py),
    except that it doesn't special-case lines starting with 'import'.
    A *.pkg file is trusted at face value: apart from checking for
    duplicates, all entries found in a *.pkg file are added to the
    path, regardless of whether they are exist the filesystem.  (This
    is a feature.)

    If the input path is not a list (as is the case for frozen
    packages) it is returned unchanged.  The input path is not
    modified; an extended copy is returned.  Items are only appended
    to the copy at the end.

    It is assumed that sys.path is a sequence.  Items of sys.path that
    are not (unicode or 8-bit) strings referring to existing
    directories are ignored.  Unicode items of sys.path that cause
    errors when used as filenames may cause this function to raise an
    exception (in line with os.path.isdir() behavior).
    """
    ...

if sys.version_info < (3, 12):
    @deprecated("Deprecated since Python 3.3; removed in Python 3.12. Use the `importlib` module instead.")
    class ImpImporter:
        """
        PEP 302 Finder that wraps Python's "classic" import algorithm

        ImpImporter(dirname) produces a PEP 302 finder that searches that
        directory.  ImpImporter(None) produces a PEP 302 finder that searches
        the current sys.path, plus any modules that are frozen or built-in.

        Note that ImpImporter does not currently support being used by placement
        on sys.meta_path.
        """
        def __init__(self, path: StrOrBytesPath | None = None) -> None: ...

    @deprecated("Deprecated since Python 3.3; removed in Python 3.12. Use the `importlib` module instead.")
    class ImpLoader:
        """
        PEP 302 Loader that wraps Python's "classic" import algorithm
    
        """
        def __init__(self, fullname: str, file: IO[str], filename: StrOrBytesPath, etc: tuple[str, str, int]) -> None: ...

if sys.version_info < (3, 14):
    @deprecated("Deprecated since Python 3.12; removed in Python 3.14. Use `importlib.util.find_spec()` instead.")
    def find_loader(fullname: str) -> LoaderProtocol | None:
        """
        Find a "loader" object for fullname

        This is a backwards compatibility wrapper around
        importlib.util.find_spec that converts most failures to ImportError
        and only returns the loader rather than the full spec
        """
        ...
    @deprecated("Deprecated since Python 3.12; removed in Python 3.14. Use `importlib.util.find_spec()` instead.")
    def get_loader(module_or_name: str) -> LoaderProtocol | None:
        """
        Get a "loader" object for module_or_name

        Returns None if the module cannot be found or imported.
        If the named module is not already imported, its containing package
        (if any) is imported, in order to establish the package __path__.
        """
        ...

def get_importer(path_item: StrOrBytesPath) -> PathEntryFinderProtocol | None:
    """
    Retrieve a finder for the given path item

    The returned finder is cached in sys.path_importer_cache
    if it was newly created by a path hook.

    The cache (or part of it) can be cleared manually if a
    rescan of sys.path_hooks is necessary.
    """
    ...
def iter_importers(fullname: str = "") -> Iterator[MetaPathFinderProtocol | PathEntryFinderProtocol]:
    """
    Yield finders for the given module name

    If fullname contains a '.', the finders will be for the package
    containing fullname, otherwise they will be all registered top level
    finders (i.e. those on both sys.meta_path and sys.path_hooks).

    If the named module is in a package, that package is imported as a side
    effect of invoking this function.

    If no module name is specified, all top level finders are produced.
    """
    ...
def iter_modules(path: Iterable[StrOrBytesPath] | None = None, prefix: str = "") -> Iterator[ModuleInfo]:
    """
    Yields ModuleInfo for all submodules on path,
    or, if path is None, all top-level modules on sys.path.

    'path' should be either None or a list of paths to look for
    modules in.

    'prefix' is a string to output on the front of every module name
    on output.
    """
    ...
def read_code(stream: SupportsRead[bytes]) -> Any: ...  # undocumented
def walk_packages(
    path: Iterable[StrOrBytesPath] | None = None, prefix: str = "", onerror: Callable[[str], object] | None = None
) -> Iterator[ModuleInfo]: ...
def get_data(package: str, resource: str) -> bytes | None: ...

if sys.version_info >= (3, 15):
    def resolve_name(name: str, *, strict: bool = False) -> Any: ...

else:
    def resolve_name(name: str) -> Any: ...

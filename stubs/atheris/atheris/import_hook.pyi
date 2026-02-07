"""
atheris instruments modules at import-time.

The instrument() function temporarily installs an import hook
(AtherisMetaPathFinder) in sys.meta_path that employs a custom loader
(AtherisSourceFileLoader, AtherisSourcelessFileLoader).
"""

import types
from collections.abc import Sequence
from importlib import abc, machinery
from typing_extensions import Self

def _should_skip(loader: abc.Loader) -> bool:
    """Returns whether modules loaded with this importer should be ignored."""
    ...

class AtherisMetaPathFinder(abc.MetaPathFinder):
    """Finds and loads package metapaths with Atheris loaders."""
    def __init__(
        self, include_packages: set[str], exclude_modules: set[str], enable_loader_override: bool, trace_dataflow: bool
    ) -> None:
        """
        Finds and loads package metapaths with Atheris loaders.

        Args:
          include_packages: If not empty, an allowlist of packages to instrument.
          exclude_modules: A denylist of modules to never instrument. This has
            higher precedent than include_packages.
          enable_loader_override: Use experimental support to instrument bytecode
            loaded from custom loaders.
          trace_dataflow: Whether or not to trace dataflow.
        """
        ...
    def find_spec(
        self, fullname: str, path: Sequence[str] | None, target: types.ModuleType | None = None
    ) -> machinery.ModuleSpec | None:
        """
        Returns the module spec if any.

        Args:
          fullname: Fully qualified name of the package.
          path: Parent package's __path__
          target: When passed in, target is a module object that the finder may use
            to make a more educated guess about what spec to return.

        Returns:
          The ModuleSpec if found, not excluded, and included if any are included.
        """
        ...
    def invalidate_caches(self) -> None: ...

class AtherisSourceFileLoader:
    """Loads a source file, patching its bytecode with Atheris instrumentation."""
    def __init__(self, name: str, path: str, trace_dataflow: bool) -> None: ...
    def get_code(self, fullname: str) -> types.CodeType | None: ...

class AtherisSourcelessFileLoader:
    """Loads a sourceless/bytecode file, patching it with Atheris instrumentation."""
    def __init__(self, name: str, path: str, trace_dataflow: bool) -> None: ...
    def get_code(self, fullname: str) -> types.CodeType | None: ...

def make_dynamic_atheris_loader(loader: abc.Loader | type[abc.Loader], trace_dataflow: bool) -> abc.Loader:
    """
    Create a loader via 'object inheritance' and return it.

    This technique allows us to override just the get_code function on an
    already-existing object loader. This is experimental.

    Args:
      loader: Loader or Loader class.
      trace_dataflow: Whether or not to trace dataflow.

    Returns:
      The loader class overriden with Atheris tracing.
    """
    ...

class HookManager:
    """A Context manager that manages hooks."""
    def __init__(
        self, include_packages: set[str], exclude_modules: set[str], enable_loader_override: bool, trace_dataflow: bool
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...

def instrument_imports(
    include: Sequence[str] | None = None, exclude: Sequence[str] | None = None, enable_loader_override: bool = True
) -> HookManager:
    """
    Returns a context manager that will instrument modules as imported.

    Args:
      include: module names that shall be instrumented. Submodules within these
        packages will be recursively instrumented too.
      exclude: module names that shall not be instrumented.
      enable_loader_override: Whether or not to enable the experimental feature of
        instrumenting custom loaders.

    Returns:

    Raises:
      TypeError: If any module name is not a str.
      ValueError: If any module name is a relative path or empty.
    """
    ...

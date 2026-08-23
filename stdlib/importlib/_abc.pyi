"""Subset of importlib.abc used to reduce importlib.util imports."""

import sys
import types
from abc import ABCMeta
from importlib.machinery import ModuleSpec
from typing_extensions import deprecated

class Loader(metaclass=ABCMeta):
    if sys.version_info < (3, 15):
        @deprecated("Deprecated since Python 3.10; removed in Python 3.15. Use `exec_module()` instead.")
        def load_module(self, fullname: str) -> types.ModuleType: ...
    if sys.version_info < (3, 12):
        @deprecated(
            "Deprecated since Python 3.4; removed in Python 3.12. "
            "The module spec is now used by the import machinery to generate a module repr."
        )
        def module_repr(self, module: types.ModuleType) -> str:
            """
            Return a module's repr.

            Used by the module type when the method does not raise
            NotImplementedError.

            This method is deprecated.
            """
            ...

    def create_module(self, spec: ModuleSpec) -> types.ModuleType | None:
        """
        Return a module to initialize and into which to load.

        This method should raise ImportError if anything prevents it
        from creating a new module.  It may return None to indicate
        that the spec should create the new module.
        """
        ...
    # Not defined on the actual class for backwards-compatibility reasons,
    # but expected in new code.
    def exec_module(self, module: types.ModuleType) -> None: ...

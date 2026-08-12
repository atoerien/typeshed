"""
distutils._msvccompiler

Contains MSVCCompiler, an implementation of the abstract CCompiler class
for Microsoft Visual Studio 2015.

This module requires VS 2015 or later.
"""

from _typeshed import StrOrBytesPath
from collections.abc import Sequence
from typing import ClassVar, Final

from . import base

PLAT_SPEC_TO_RUNTIME: Final[dict[str, str]]

class Compiler(base.Compiler):
    """
    Concrete class that implements an interface to Microsoft Visual C++,
    as defined by the CCompiler abstract class.
    """
    compiler_type: ClassVar[str]
    description: ClassVar[str]
    src_extensions: ClassVar[list[str]]
    res_extension: ClassVar[str]
    obj_extension: ClassVar[str]
    static_lib_extension: ClassVar[str]
    shared_lib_extension: ClassVar[str]
    shared_lib_format: ClassVar[str]
    static_lib_format = shared_lib_format  # pyrefly: ignore [unknown-name]
    exe_extension: ClassVar[str]
    initialized: bool
    plat_name: str | None
    def initialize(self, plat_name: str | None = None) -> None: ...
    @property
    def out_extensions(self) -> dict[str, str]: ...
    def call(self, cmd: Sequence[StrOrBytesPath], *, env=None, **kwargs) -> None: ...

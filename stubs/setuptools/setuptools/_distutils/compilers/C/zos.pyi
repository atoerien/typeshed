"""
distutils.zosccompiler

Contains the selection of the c & c++ compilers on z/OS. There are several
different c compilers on z/OS, all of them are optional, so the correct
one needs to be chosen based on the users input. This is compatible with
the following compilers:

IBM C/C++ For Open Enterprise Languages on z/OS 2.0
IBM Open XL C/C++ 1.1 for z/OS
IBM XL C/C++ V2.4.1 for z/OS 2.4 and 2.5
IBM z/OS XL C/C++
"""

from _typeshed import StrPath
from collections.abc import Iterable
from typing import ClassVar, Literal

from . import unix

class Compiler(unix.Compiler):
    src_extensions: ClassVar[list[str]]
    zos_compiler: Literal["ibm-openxl", "ibm-xlclang", "ibm-xlc"]
    def __init__(self, verbose: bool = False, force: bool = False) -> None: ...
    def runtime_library_dir_option(self, dir: str) -> str: ...
    def link(
        self,
        target_desc: str,
        objects: list[str] | tuple[str, ...],
        output_filename: str,
        output_dir: str | None = None,
        libraries: list[str] | tuple[str, ...] | None = None,
        library_dirs: list[str] | tuple[str, ...] | None = None,
        runtime_library_dirs: list[str] | tuple[str, ...] | None = None,
        export_symbols: Iterable[str] | None = None,
        debug: bool = False,
        extra_preargs: list[str] | None = None,
        extra_postargs: list[str] | None = None,
        build_temp: StrPath | None = None,
        target_lang: str | None = None,
    ) -> None: ...

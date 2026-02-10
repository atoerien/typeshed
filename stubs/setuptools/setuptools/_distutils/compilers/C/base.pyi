"""
distutils.ccompiler

Contains Compiler, an abstract base class that defines the interface
for the Distutils compiler abstraction model.
"""

from _typeshed import BytesPath, Incomplete, StrOrBytesPath, StrPath, Unused
from collections.abc import Callable, Iterable, MutableSequence, Sequence
from subprocess import _ENV
from typing import ClassVar, Final, Literal, TypeVar, overload
from typing_extensions import TypeAlias, TypeVarTuple, Unpack, deprecated

_Macro: TypeAlias = tuple[str] | tuple[str, str | None]
_StrPathT = TypeVar("_StrPathT", bound=StrPath)
_BytesPathT = TypeVar("_BytesPathT", bound=BytesPath)
_Ts = TypeVarTuple("_Ts")

class Compiler:
    """
    Abstract base class to define the interface that must be implemented
    by real compiler classes.  Also has some utility methods used by
    several compiler classes.

    The basic idea behind a compiler abstraction class is that each
    instance can be used for all the compile/link steps in building a
    single project.  Thus, attributes common to all of those compile and
    link steps -- include directories, macros to define, libraries to link
    against, etc. -- are attributes of the compiler instance.  To allow for
    variability in how individual files are treated, most of those
    attributes may be varied on a per-compilation or per-link basis.
    """
    compiler_type: ClassVar[str]
    executables: ClassVar[dict[str, Incomplete]]

    # Subclasses that rely on the standard filename generation methods
    # implemented below should override these
    src_extensions: ClassVar[list[str] | None]
    obj_extension: ClassVar[str | None]
    static_lib_extension: ClassVar[str | None]
    shared_lib_extension: ClassVar[str | None]
    static_lib_format: ClassVar[str | None]
    shared_lib_format: ClassVar[str | None]
    exe_extension: ClassVar[str | None]

    language_map: ClassVar[dict[str, str]]
    language_order: ClassVar[list[str]]
    force: bool
    verbose: bool
    output_dir: str | None
    macros: list[_Macro]
    include_dirs: list[str]
    libraries: list[str]
    library_dirs: list[str]
    runtime_library_dirs: list[str]
    objects: list[str]

    SHARED_OBJECT: Final = "shared_object"
    SHARED_LIBRARY: Final = "shared_library"
    EXECUTABLE: Final = "executable"
    def __init__(self, verbose: bool = False, force: bool = False) -> None: ...
    def add_include_dir(self, dir: str) -> None: ...
    def set_include_dirs(self, dirs: list[str]) -> None: ...
    def add_library(self, libname: str) -> None: ...
    def set_libraries(self, libnames: list[str]) -> None: ...
    def add_library_dir(self, dir: str) -> None: ...
    def set_library_dirs(self, dirs: list[str]) -> None: ...
    def add_runtime_library_dir(self, dir: str) -> None: ...
    def set_runtime_library_dirs(self, dirs: list[str]) -> None: ...
    def define_macro(self, name: str, value: str | None = None) -> None: ...
    def undefine_macro(self, name: str) -> None: ...
    def add_link_object(self, object: str) -> None: ...
    def set_link_objects(self, objects: list[str]) -> None: ...
    def detect_language(self, sources: str | list[str]) -> str | None: ...
    def find_library_file(self, dirs: Iterable[str], lib: str, debug: bool = False) -> str | None: ...
    @overload
    def has_function(
        self, funcname: str, libraries: list[str] | None = None, library_dirs: list[str] | tuple[str, ...] | None = None
    ) -> bool: ...
    @overload
    @deprecated("The `includes`, `include_dirs` parameters are deprecated.")
    def has_function(
        self,
        funcname: str,
        includes: Iterable[str] | None = None,
        include_dirs: list[str] | tuple[str, ...] | None = None,
        libraries: list[str] | None = None,
        library_dirs: list[str] | tuple[str, ...] | None = None,
    ) -> bool:
        """
        Return a boolean indicating whether funcname is provided as
        a symbol on the current platform.  The optional arguments can
        be used to augment the compilation environment.

        The libraries argument is a list of flags to be passed to the
        linker to make additional symbol definitions available for
        linking.

        The includes and include_dirs arguments are deprecated.
        Usually, supplying include files with function declarations
        will cause function detection to fail even in cases where the
        symbol is available for linking.
        """
        ...
    def library_dir_option(self, dir: str) -> str:
        """
        Return the compiler option to add 'dir' to the list of
        directories searched for libraries.
        """
        ...
    def library_option(self, lib: str) -> str:
        """
        Return the compiler option to add 'lib' to the list of libraries
        linked into the shared library or executable.
        """
        ...
    def runtime_library_dir_option(self, dir: str) -> str:
        """
        Return the compiler option to add 'dir' to the list of
        directories searched for runtime libraries.
        """
        ...
    def set_executables(self, **kwargs: str) -> None:
        """
        Define the executables (and options for them) that will be run
        to perform the various stages of compilation.  The exact set of
        executables that may be specified here depends on the compiler
        class (via the 'executables' class attribute), but most will have:
          compiler      the C/C++ compiler
          linker_so     linker used to create shared objects and libraries
          linker_exe    linker used to create binary executables
          archiver      static library creator

        On platforms with a command-line (Unix, DOS/Windows), each of these
        is a string that will be split into executable name and (optional)
        list of arguments.  (Splitting the string is done similarly to how
        Unix shells operate: words are delimited by spaces, but quotes and
        backslashes can override this.  See
        'distutils.util.split_quoted()'.)
        """
        ...
    def set_executable(self, key: str, value) -> None: ...
    def compile(
        self,
        sources: Sequence[StrPath],
        output_dir: str | None = None,
        macros: list[_Macro] | None = None,
        include_dirs: list[str] | tuple[str, ...] | None = None,
        debug: bool = False,
        extra_preargs: list[str] | None = None,
        extra_postargs: list[str] | None = None,
        depends: list[str] | tuple[str, ...] | None = None,
    ) -> list[str]:
        """
        Compile one or more source files.

        'sources' must be a list of filenames, most likely C/C++
        files, but in reality anything that can be handled by a
        particular compiler and compiler class (eg. MSVCCompiler can
        handle resource files in 'sources').  Return a list of object
        filenames, one per source filename in 'sources'.  Depending on
        the implementation, not all source files will necessarily be
        compiled, but all corresponding object filenames will be
        returned.

        If 'output_dir' is given, object files will be put under it, while
        retaining their original path component.  That is, "foo/bar.c"
        normally compiles to "foo/bar.o" (for a Unix implementation); if
        'output_dir' is "build", then it would compile to
        "build/foo/bar.o".

        'macros', if given, must be a list of macro definitions.  A macro
        definition is either a (name, value) 2-tuple or a (name,) 1-tuple.
        The former defines a macro; if the value is None, the macro is
        defined without an explicit value.  The 1-tuple case undefines a
        macro.  Later definitions/redefinitions/ undefinitions take
        precedence.

        'include_dirs', if given, must be a list of strings, the
        directories to add to the default include file search path for this
        compilation only.

        'debug' is a boolean; if true, the compiler will be instructed to
        output debug symbols in (or alongside) the object file(s).

        'extra_preargs' and 'extra_postargs' are implementation- dependent.
        On platforms that have the notion of a command-line (e.g. Unix,
        DOS/Windows), they are most likely lists of strings: extra
        command-line arguments to prepend/append to the compiler command
        line.  On other platforms, consult the implementation class
        documentation.  In any event, they are intended as an escape hatch
        for those occasions when the abstract compiler framework doesn't
        cut the mustard.

        'depends', if given, is a list of filenames that all targets
        depend on.  If a source file is older than any file in
        depends, then the source file will be recompiled.  This
        supports dependency tracking, but only at a coarse
        granularity.

        Raises CompileError on failure.
        """
        ...
    def create_static_lib(
        self,
        objects: list[str] | tuple[str, ...],
        output_libname: str,
        output_dir: str | None = None,
        debug: bool = False,
        target_lang: str | None = None,
    ) -> None:
        """
        Link a bunch of stuff together to create a static library file.
        The "bunch of stuff" consists of the list of object files supplied
        as 'objects', the extra object files supplied to
        'add_link_object()' and/or 'set_link_objects()', the libraries
        supplied to 'add_library()' and/or 'set_libraries()', and the
        libraries supplied as 'libraries' (if any).

        'output_libname' should be a library name, not a filename; the
        filename will be inferred from the library name.  'output_dir' is
        the directory where the library file will be put.

        'debug' is a boolean; if true, debugging information will be
        included in the library (note that on most platforms, it is the
        compile step where this matters: the 'debug' flag is included here
        just for consistency).

        'target_lang' is the target language for which the given objects
        are being compiled. This allows specific linkage time treatment of
        certain languages.

        Raises LibError on failure.
        """
        ...
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
    ) -> None:
        """
        Link a bunch of stuff together to create an executable or
        shared library file.

        The "bunch of stuff" consists of the list of object files supplied
        as 'objects'.  'output_filename' should be a filename.  If
        'output_dir' is supplied, 'output_filename' is relative to it
        (i.e. 'output_filename' can provide directory components if
        needed).

        'libraries' is a list of libraries to link against.  These are
        library names, not filenames, since they're translated into
        filenames in a platform-specific way (eg. "foo" becomes "libfoo.a"
        on Unix and "foo.lib" on DOS/Windows).  However, they can include a
        directory component, which means the linker will look in that
        specific directory rather than searching all the normal locations.

        'library_dirs', if supplied, should be a list of directories to
        search for libraries that were specified as bare library names
        (ie. no directory component).  These are on top of the system
        default and those supplied to 'add_library_dir()' and/or
        'set_library_dirs()'.  'runtime_library_dirs' is a list of
        directories that will be embedded into the shared library and used
        to search for other shared libraries that *it* depends on at
        run-time.  (This may only be relevant on Unix.)

        'export_symbols' is a list of symbols that the shared library will
        export.  (This appears to be relevant only on Windows.)

        'debug' is as for 'compile()' and 'create_static_lib()', with the
        slight distinction that it actually matters on most platforms (as
        opposed to 'create_static_lib()', which includes a 'debug' flag
        mostly for form's sake).

        'extra_preargs' and 'extra_postargs' are as for 'compile()' (except
        of course that they supply command-line arguments for the
        particular linker being used).

        'target_lang' is the target language for which the given objects
        are being compiled. This allows specific linkage time treatment of
        certain languages.

        Raises LinkError on failure.
        """
        ...
    def link_executable(
        self,
        objects: list[str] | tuple[str, ...],
        output_progname: str,
        output_dir: str | None = None,
        libraries: list[str] | tuple[str, ...] | None = None,
        library_dirs: list[str] | tuple[str, ...] | None = None,
        runtime_library_dirs: list[str] | tuple[str, ...] | None = None,
        debug: bool = False,
        extra_preargs: list[str] | None = None,
        extra_postargs: list[str] | None = None,
        target_lang: str | None = None,
    ) -> None: ...
    def link_shared_lib(
        self,
        objects: list[str] | tuple[str, ...],
        output_libname: str,
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
    def link_shared_object(
        self,
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
    def preprocess(
        self,
        source: StrPath,
        output_file: StrPath | None = None,
        macros: list[_Macro] | None = None,
        include_dirs: list[str] | tuple[str, ...] | None = None,
        extra_preargs: list[str] | None = None,
        extra_postargs: Iterable[str] | None = None,
    ) -> None:
        """
        Preprocess a single C/C++ source file, named in 'source'.
        Output will be written to file named 'output_file', or stdout if
        'output_file' not supplied.  'macros' is a list of macro
        definitions as for 'compile()', which will augment the macros set
        with 'define_macro()' and 'undefine_macro()'.  'include_dirs' is a
        list of directory names that will be added to the default list.

        Raises PreprocessError on failure.
        """
        ...
    @overload
    def executable_filename(self, basename: str, strip_dir: Literal[False] = False, output_dir: StrPath = "") -> str: ...
    @overload
    def executable_filename(self, basename: StrPath, strip_dir: Literal[True], output_dir: StrPath = "") -> str: ...
    def library_filename(
        self, libname: str, lib_type: str = "static", strip_dir: bool = False, output_dir: StrPath = ""
    ) -> str: ...
    @property
    def out_extensions(self) -> dict[str, str]: ...
    def object_filenames(
        self, source_filenames: Iterable[StrPath], strip_dir: bool = False, output_dir: StrPath | None = ""
    ) -> list[str]: ...
    @overload
    def shared_object_filename(self, basename: str, strip_dir: Literal[False] = False, output_dir: StrPath = "") -> str: ...
    @overload
    def shared_object_filename(self, basename: StrPath, strip_dir: Literal[True], output_dir: StrPath = "") -> str: ...
    def execute(
        self, func: Callable[[Unpack[_Ts]], Unused], args: tuple[Unpack[_Ts]], msg: str | None = None, level: int = 1
    ) -> None: ...
    @overload
    def spawn(self, cmd: Sequence[StrOrBytesPath], *, search_path: Literal[False], env: _ENV | None = None) -> None: ...
    @overload
    def spawn(
        self, cmd: MutableSequence[bytes | StrPath], *, search_path: Literal[True] = True, env: _ENV | None = None
    ) -> None: ...
    def mkpath(self, name: str, mode: int = 0o777) -> None: ...
    @overload
    def move_file(self, src: StrPath, dst: _StrPathT) -> _StrPathT | str: ...
    @overload
    def move_file(self, src: BytesPath, dst: _BytesPathT) -> _BytesPathT | bytes: ...
    def announce(self, msg: str, level: int = 1) -> None: ...
    def warn(self, msg: str) -> None: ...
    def debug_print(self, msg: str) -> None: ...

def get_default_compiler(osname: str | None = None, platform: str | None = None) -> str:
    """
    Determine the default compiler to use for the given platform.

    osname should be one of the standard Python OS names (i.e. the
    ones returned by os.name) and platform the common value
    returned by sys.platform for the platform in question.

    The default values are os.name and sys.platform in case the
    parameters are not given.
    """
    ...

compiler_class: dict[str, tuple[str, str, str]]

def show_compilers() -> None:
    """
    Print list of available compilers (used by the "--help-compiler"
    options to "build", "build_ext", "build_clib").
    """
    ...
def new_compiler(
    plat: str | None = None, compiler: str | None = None, verbose: bool = False, force: bool = False
) -> Compiler: ...
def gen_preprocess_options(macros: Iterable[_Macro], include_dirs: Iterable[str]) -> list[str]: ...
def gen_lib_options(
    compiler: Compiler, library_dirs: Iterable[str], runtime_library_dirs: Iterable[str], libraries: Iterable[str]
) -> list[str]:
    """
    Generate linker options for searching library directories and
    linking with specific libraries.  'libraries' and 'library_dirs' are,
    respectively, lists of library names (not filenames!) and search
    directories.  Returns a list of command-line options suitable for use
    with some compiler (depending on the two format strings passed in).
    """
    ...

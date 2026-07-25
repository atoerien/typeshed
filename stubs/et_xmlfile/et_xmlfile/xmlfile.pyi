import types
import xml.etree.ElementTree as ET
from collections.abc import Callable, Generator
from contextlib import _GeneratorContextManager, contextmanager
from typing import Any

class LxmlSyntaxError(Exception): ...

class _IncrementalFileWriter:
    """Replacement for _IncrementalFileWriter of lxml"""
    global_nsmap: dict[str, str]
    is_html: bool
    def __init__(self, output_file: Callable[[str], object]) -> None: ...
    @contextmanager
    def element(
        self,
        tag: str | ET._ElementCallable,
        attrib: dict[str, str] | None = None,
        nsmap: dict[str, str] | None = None,
        **_extra: str,
    ) -> Generator[None]:
        """Create a new xml element using a context manager."""
        ...
    def write(self, arg: str | ET.Element[Any]) -> None:
        """Write a string or subelement."""
        ...
    def __enter__(self) -> None: ...
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None
    ) -> None: ...

class xmlfile:
    """Context manager that can replace lxml.etree.xmlfile."""
    encoding: str
    writer_cm: _GeneratorContextManager[tuple[Callable[[str], object], str]] | None
    def __init__(
        self, output_file: ET._FileWrite, buffered: bool = False, encoding: str = "utf-8", close: bool = False
    ) -> None: ...
    def __enter__(self) -> _IncrementalFileWriter: ...
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None
    ) -> None: ...

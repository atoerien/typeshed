"""
``jsonutils`` aims to provide various helpers for working with
JSON. Currently it focuses on providing a reliable and intuitive means
of working with `JSON Lines`_-formatted files.

.. _JSON Lines: http://jsonlines.org/
"""

from collections.abc import Generator
from typing import IO, Any, overload
from typing_extensions import Self

@overload
def reverse_iter_lines(
    file_obj: IO[bytes], blocksize: int = 4096, preseek: bool = True, encoding: None = None
) -> Generator[bytes]: ...
@overload
def reverse_iter_lines(file_obj: IO[str], blocksize: int = 4096, preseek: bool = True, *, encoding: str) -> Generator[str]: ...
@overload
def reverse_iter_lines(file_obj: IO[str], blocksize: int, preseek: bool, encoding: str) -> Generator[str]: ...

class JSONLIterator:
    """
    The ``JSONLIterator`` is used to iterate over JSON-encoded objects
    stored in the `JSON Lines format`_ (one object per line).

    Most notably it has the ability to efficiently read from the
    bottom of files, making it very effective for reading in simple
    append-only JSONL use cases. It also has the ability to start from
    anywhere in the file and ignore corrupted lines.

    Args:
        file_obj (file): An open file object.
        ignore_errors (bool): Whether to skip over lines that raise an error on
            deserialization (:func:`json.loads`).
        reverse (bool): Controls the direction of the iteration.
            Defaults to ``False``. If set to ``True`` and *rel_seek*
            is unset, seeks to the end of the file before iteration
            begins.
        rel_seek (float): Used to preseek the start position of
            iteration. Set to 0.0 for the start of the file, 1.0 for the
            end, and anything in between.

    .. _JSON Lines format: http://jsonlines.org/
    """
    ignore_errors: bool
    def __init__(
        self, file_obj: IO[str], ignore_errors: bool = False, reverse: bool = False, rel_seek: float | None = None
    ) -> None: ...
    @property
    def cur_byte_pos(self) -> int:
        """A property representing where in the file the iterator is reading."""
        ...
    def __iter__(self) -> Self: ...
    def next(self) -> Any:
        """
        Yields one :class:`dict` loaded with :func:`json.loads`, advancing
        the file object by one line. Raises :exc:`StopIteration` upon reaching
        the end of the file (or beginning, if ``reverse`` was set to ``True``.
        """
        ...
    __next__ = next

__all__ = ["JSONLIterator", "reverse_iter_lines"]

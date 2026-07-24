"""
Bridge between Python file openers and GDAL VSI.

Based on _filepath.pyx.
"""

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Any, BinaryIO

from rasterio.errors import OpenerRegistrationError as OpenerRegistrationError

class FileContainer(ABC):
    """An object that can report on and open Python files."""
    @abstractmethod
    def open(self, path: str, mode: str = "r", **kwds: Any) -> BinaryIO:
        """
        Get a Python file object for a resource.

        Parameters
        ----------
        path : str
            The identifier/locator for a resource within a filesystem.
        mode : str
            Opening mode.
        kwds : dict
            Opener specific options. Encoding, etc.

        Returns
        -------
        obj
            A Python 'file' object with methods read/write, seek, tell,
            etc.
        """
        ...
    @abstractmethod
    def isdir(self, path: str) -> bool:
        """
        Test if the resource is a 'directory', a container.

        Parameters
        ----------
        path : str
            The identifier/locator for a resource within a filesystem.

        Returns
        -------
        bool
        """
        ...
    @abstractmethod
    def isfile(self, path: str) -> bool:
        """
        Test if the resource is a 'file', a sequence of bytes.

        Parameters
        ----------
        path : str
            The identifier/locator for a resource within a filesystem.

        Returns
        -------
        bool
        """
        ...
    @abstractmethod
    def ls(self, path: str) -> list[str]:
        """
        Get a 'directory' listing.

        Parameters
        ----------
        path : str
            The identifier/locator for a directory within a filesystem.

        Returns
        -------
        list of str
            List of 'path' paths relative to the directory.
        """
        ...
    @abstractmethod
    def mtime(self, path: str) -> int:
        """
        Get the mtime of a resource..

        Parameters
        ----------
        path : str
            The identifier/locator for a directory within a filesystem.

        Returns
        -------
        int
            Modification timestamp in seconds.
        """
        ...
    @abstractmethod
    def rm(self, path: str) -> None:
        """
        Remove a resource.

        Parameters
        ----------
        path : str
            The identifier/locator for a resource within a filesystem.

        Returns
        -------
        None
        """
        ...
    @abstractmethod
    def size(self, path: str) -> int:
        """
        Get the size, in bytes, of a resource..

        Parameters
        ----------
        path : str
            The identifier/locator for a resource within a filesystem.

        Returns
        -------
        int
        """
        ...

class MultiByteRangeResource(ABC):
    """An object that provides VSIFilesystemPluginReadMultiRangeCallback."""
    @abstractmethod
    def get_byte_ranges(self, offsets: list[int], sizes: list[int]) -> list[bytes]:
        """Get a sequence of bytes specified by a sequence of ranges."""
        ...

class MultiByteRangeResourceContainer(FileContainer):
    """An object that can open a MultiByteRangeResource."""
    @abstractmethod
    def open(self, path: str, **kwds: Any) -> MultiByteRangeResource:
        """Open the resource at the given path."""
        ...

# Duck-typed adapter: `obj` may be a `FileContainer` subclass or any
# object exposing the fsspec filesystem protocol (`hasattr(obj, "file_size")`).
def to_pyopener(obj: Any) -> FileContainer:
    """Adapt an object to the Pyopener interface."""
    ...

# `obj` accepts the same types as `to_pyopener` plus raw callables.
def _opener_registration(urlpath: str, obj: Any) -> AbstractContextManager[str]: ...

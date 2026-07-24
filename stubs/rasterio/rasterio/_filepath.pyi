"""
Bridge between Python file-like objects and GDAL VSI.

The functionality provided in this interface is made possible thanks to GDAL's
Plugin infrastructure. You can find more information about this below and in
GDAL's documentation here:

https://gdal.org/api/cpl.html#structVSIFilesystemPluginCallbacksStruct

.. note::

    Parts of GDAL's plugin interface use C++ features/definitions. For
    that reason this module must be compiled as C++.

The high-level idea of the plugin interface is to define a series of callbacks
for the operations GDAL may need to perform. There are two types of operations:
filesystem and file. The filesystem operations cover things like opening a file,
making directories, renaming files, etc. The file operations involve things like
reading from the file, seeking to a specific position, and getting the current
position in the file.

Filesystem Handling
*******************

This plugin currently only defines the "open" callback. The other features are
either not needed or have usable default implementations.

The entire filesystem's state is stored in a global dictionary mapping
in-memory GDAL filenames to :class:`~rasterio._filepath.FilePathBase` objects.

File Handling
*************

This plugin implements the bare minimum for reading from an open file-like
object. It does this by mapping GDAL's function calls (ex. read, seek) to
the corresponding method call on the file-like object.
"""

from typing import TypeVar

_FileT = TypeVar("_FileT")

class FilePathBase:
    """Base for a BytesIO-like class backed by a Python file-like object."""
    # Cython base for FilePath; constructor and overall surface are
    # implementation details — see `rasterio.io.FilePath` for the public API.
    def __init__(self, *args: object, **kwargs: object) -> None:
        """
        A file in an in-memory filesystem.

        Parameters
        ----------
        filelike_obj : file-like objects
            A file opened in binary mode
        filename : str
            An optional filename used internally by GDAL. If not provided then
            a unique one will be generated.
        """
        ...
    def close(self) -> None:
        """
        Mark the file as closed.

        This does not actually attempt to close the file; that is left up
        to the user.
        """
        ...
    def exists(self) -> bool:
        """
        Test if the in-memory file exists.

        Returns
        -------
        bool
            True if the in-memory file exists.
        """
        ...

# Clones any file-like object (BytesIO, MemoryFile, fsspec file, Python
# file object); the returned object has the same concrete type as `fobj`.
def clone_file_obj(fobj: _FileT) -> _FileT:
    """
    Clone a filelike object.

    Supports BytesIO, MemoryFile, fsspec files, and Python file objects.
    """
    ...

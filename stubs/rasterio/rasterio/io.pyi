"""
Classes capable of reading and writing datasets

Instances of these classes are called dataset objects.
"""

import logging
from types import TracebackType
from typing import Any, Final
from typing_extensions import Self, deprecated

from numpy.typing import DTypeLike
from rasterio._affine_types import Affine
from rasterio._filepath import FilePathBase as FilePathBase
from rasterio._io import (
    BufferedDatasetWriterBase as BufferedDatasetWriterBase,
    DatasetReaderBase as DatasetReaderBase,
    DatasetWriterBase as DatasetWriterBase,
    MemoryFileBase as MemoryFileBase,
)
from rasterio._typing import CRSInput, FileOrBytes, _OpenOption
from rasterio.transform import TransformMethodsMixin
from rasterio.windows import WindowMethodsMixin

log: Final[logging.Logger]

class DatasetReader(DatasetReaderBase, WindowMethodsMixin, TransformMethodsMixin):
    """An unbuffered data and metadata reader"""
    ...
class DatasetWriter(DatasetWriterBase, WindowMethodsMixin, TransformMethodsMixin):
    """
    An unbuffered data and metadata writer. Its methods write data
    directly to disk.
    """
    ...
class BufferedDatasetWriter(BufferedDatasetWriterBase, WindowMethodsMixin, TransformMethodsMixin):
    """
    Maintains data and metadata in a buffer, writing to disk or
    network only when `close()` is called.

    This allows incremental updates to datasets using formats that don't
    otherwise support updates, such as JPEG.
    """
    ...

class MemoryFile(MemoryFileBase):
    """
    A BytesIO-like object, backed by an in-memory file.

    This allows formatted files to be read and written without I/O.

    A MemoryFile created with initial bytes becomes immutable. A
    MemoryFile created without initial bytes may be written to using
    either file-like or dataset interfaces.

    Examples
    --------

    A GeoTIFF can be loaded in memory and accessed using the GeoTIFF
    format driver

    >>> with open('tests/data/RGB.byte.tif', 'rb') as f, MemoryFile(f) as memfile:
    ...     with memfile.open() as src:
    ...         pprint.pprint(src.profile)
    ...
    {'count': 3,
     'crs': CRS({'init': 'epsg:32618'}),
     'driver': 'GTiff',
     'dtype': 'uint8',
     'height': 718,
     'interleave': 'pixel',
     'nodata': 0.0,
     'tiled': False,
     'transform': Affine(300.0379266750948, 0.0, 101985.0,
           0.0, -300.041782729805, 2826915.0),
     'width': 791}
    """
    def __init__(
        self, file_or_bytes: FileOrBytes | None = None, dirname: str | None = None, filename: str | None = None, ext: str = ".tif"
    ) -> None:
        """
        Create a new file in memory

        Parameters
        ----------
        file_or_bytes : file-like object or bytes, optional
            File or bytes holding initial data.
        filename : str, optional
            An optional filename. A unique one will otherwise be generated.
        ext : str, optional
            An optional extension.

        Returns
        -------
        MemoryFile
        """
        ...
    def open(
        self,
        driver: str | None = None,
        width: int | None = None,
        height: int | None = None,
        count: int | None = None,
        crs: CRSInput | None = None,
        transform: Affine | None = None,
        dtype: DTypeLike | None = None,
        nodata: float | None = None,
        sharing: bool = False,
        thread_safe: bool = False,
        **kwargs: _OpenOption,
    ) -> DatasetReader | DatasetWriter:
        """
        Open the file and return a Rasterio dataset object.

        If data has already been written, the file is opened in 'r'
        mode. Otherwise, the file is opened in 'w' mode.

        Parameters
        ----------
        Note well that there is no `path` parameter: a `MemoryFile`
        contains a single dataset and there is no need to specify a
        path.

        Other parameters are optional and have the same semantics as the
        parameters of `rasterio.open()`.
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> bool | None: ...

class ZipMemoryFile(MemoryFile):
    """
    A read-only BytesIO-like object backed by an in-memory zip file.

    This allows a zip file containing formatted files to be read
    without I/O.
    """
    def __init__(self, file_or_bytes: FileOrBytes | None = None) -> None: ...
    def open(  # type: ignore[override]
        self, path: str, driver: str | None = None, sharing: bool = False, thread_safe: bool = False, **kwargs: _OpenOption
    ) -> DatasetReader:
        """
        Open a dataset within the zipped stream.

        Parameters
        ----------
        path : str
            Path to a dataset in the zip file, relative to the root of the
            archive.

        Other parameters are optional and have the same semantics as the
        parameters of `rasterio.open()`.

        Returns
        -------
        A Rasterio dataset object
        """
        ...

@deprecated("FilePath is supplanted by rasterio.open's `opener` keyword argument and will be removed in 2.0.0.")
class FilePath(FilePathBase):
    """
    A BytesIO-like object, backed by a Python file object.

    .. deprecated:: 1.4.0
       FilePath is supplanted by open's new opener keyword argument,
       and will be removed in 2.0.0.
    """
    # `filelike_obj`: any Python file-like object (BytesIO, fsspec file, etc.).
    def __init__(self, filelike_obj: Any, dirname: str | None = None, filename: str | None = None) -> None:
        """
        Create a new wrapper around the provided file-like object.

        Parameters
        ----------
        filelike_obj : file-like object
            Open file-like object. Currently only reading is supported.
        filename : str, optional
            An optional filename. A unique one will otherwise be generated.

        Returns
        -------
        PythonVSIFile
        """
        ...
    def open(
        self, driver: str | None = None, sharing: bool = False, thread_safe: bool = False, **kwargs: _OpenOption
    ) -> DatasetReader:
        """
        Open the file and return a Rasterio dataset object.

        The provided file-like object is assumed to be readable.
        Writing is currently not supported.

        Parameters are optional and have the same semantics as the
        parameters of `rasterio.open()`.

        Returns
        -------
        DatasetReader

        Raises
        ------
        IOError
            If the memory file is closed.
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> bool | None: ...

def get_writer_for_driver(driver: str) -> type[DatasetWriter | BufferedDatasetWriter] | None:
    """Return the writer class appropriate for the specified driver."""
    ...
def get_writer_for_path(path: str, driver: str | None = None) -> type[DatasetWriter | BufferedDatasetWriter] | None:
    """Return the writer class appropriate for the existing dataset."""
    ...

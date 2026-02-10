"""
distutils.archive_util

Utility functions for creating archive files (tarballs, zip files,
that sort of thing).
"""

from _typeshed import StrOrBytesPath, StrPath
from typing import Literal, overload

@overload
def make_archive(
    base_name: str,
    format: str,
    root_dir: StrOrBytesPath | None = None,
    base_dir: str | None = None,
    verbose: bool = False,
    owner: str | None = None,
    group: str | None = None,
) -> str:
    """
    Create an archive file (eg. zip or tar).

    'base_name' is the name of the file to create, minus any format-specific
    extension; 'format' is the archive format: one of "zip", "tar", "gztar",
    "bztar", "xztar", or "ztar".

    'root_dir' is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.  'base_dir' is the directory where we start archiving from;
    ie. 'base_dir' will be the common prefix of all files and
    directories in the archive.  'root_dir' and 'base_dir' both default
    to the current directory.  Returns the name of the archive file.

    'owner' and 'group' are used when creating a tar archive. By default,
    uses the current owner and group.
    """
    ...
@overload
def make_archive(
    base_name: StrPath,
    format: str,
    root_dir: StrOrBytesPath,
    base_dir: str | None = None,
    verbose: bool = False,
    owner: str | None = None,
    group: str | None = None,
) -> str:
    """
    Create an archive file (eg. zip or tar).

    'base_name' is the name of the file to create, minus any format-specific
    extension; 'format' is the archive format: one of "zip", "tar", "gztar",
    "bztar", "xztar", or "ztar".

    'root_dir' is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.  'base_dir' is the directory where we start archiving from;
    ie. 'base_dir' will be the common prefix of all files and
    directories in the archive.  'root_dir' and 'base_dir' both default
    to the current directory.  Returns the name of the archive file.

    'owner' and 'group' are used when creating a tar archive. By default,
    uses the current owner and group.
    """
    ...
def make_tarball(
    base_name: str,
    base_dir: StrPath,
    compress: Literal["gzip", "bzip2", "xz"] | None = "gzip",
    verbose: bool = False,
    owner: str | None = None,
    group: str | None = None,
) -> str: ...
def make_zipfile(base_name: str, base_dir: StrPath, verbose: bool = False) -> str: ...

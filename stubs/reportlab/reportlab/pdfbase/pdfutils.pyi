from _typeshed import Incomplete
from typing import Final, Literal

__version__: Final[str]

def makeA85Image(filename, IMG=None, detectJpeg: bool = False) -> list[Incomplete] | None: ...
def makeRawImage(filename, IMG=None, detectJpeg: bool = False) -> list[Incomplete] | None: ...
def cacheImageFile(filename, returnInMemory: bool | Literal[0, 1] = 0, IMG=None):
    """Processes image as if for encoding, saves to a file with .a85 extension."""
    ...
def preProcessImages(spec) -> None:
    r"""
    Preprocesses one or more image files.

    Accepts either a filespec ('C:\mydir\*.jpg') or a list
    of image filenames, crunches them all to save time.  Run this
    to save huge amounts of time when repeatedly building image
    documents.
    """
    ...
def cachedImageExists(filename) -> Literal[0, 1]:
    """
    Determines if a cached image already exists for a given file.

    Determines if a cached image exists which has the same name
    and equal or newer date to the given file.
    """
    ...
def readJPEGInfo(image) -> tuple[Incomplete, Incomplete, Incomplete, Incomplete] | None:
    """Read width, height and number of components from open JPEG file."""
    ...

class _fusc:
    def __init__(self, k, n) -> None: ...
    def encrypt(self, s) -> str: ...
    def decrypt(self, s) -> str: ...

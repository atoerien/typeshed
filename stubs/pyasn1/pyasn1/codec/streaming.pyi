import io
from _typeshed import Incomplete
from collections.abc import Generator

from pyasn1 import error as error
from pyasn1.type import univ as univ

class CachingStreamWrapper(io.IOBase):
    """
    Wrapper around non-seekable streams.

    Note that the implementation is tied to the decoder,
    not checking for dangerous arguments for the sake
    of performance.

    The read bytes are kept in an internal cache until
    setting _markedPosition which may reset the cache.
    """
    def __init__(self, raw) -> None: ...
    def peek(self, n): ...
    def seekable(self): ...
    def seek(self, n: int = -1, whence=0): ...
    def read(self, n: int = -1): ...
    @property
    def markedPosition(self):
        """
        Position where the currently processed element starts.

        This is used for back-tracking in SingleItemDecoder.__call__
        and (indefLen)ValueDecoder and should not be used for other purposes.
        The client is not supposed to ever seek before this position.
        """
        ...
    def tell(self): ...

def asSeekableStream(substrate): ...
def isEndOfStream(substrate) -> Generator[Incomplete]: ...
def peekIntoStream(substrate, size: int = -1) -> Generator[Incomplete]: ...
def readFromStream(substrate, size: int = -1, context=None) -> Generator[Incomplete]: ...

"""
distutils.spawn

Provides the 'spawn()' function, a front-end to various platform-
specific functions for launching another program in a sub-process.
"""

from _typeshed import StrOrBytesPath
from collections.abc import Sequence
from subprocess import _ENV

def spawn(cmd: Sequence[StrOrBytesPath], *, env: _ENV | None = None, **kwargs) -> None:
    """
    Run another program, specified as a command list 'cmd', in a new process.

    'cmd' is just the argument list for the new process, ie.
    cmd[0] is the program to run and cmd[1:] are the rest of its arguments.
    Any keyword arguments are passed through to ``subprocess.check_call``.

    Raise DistutilsExecError if running the program fails in any way; just
    return on success.
    """
    ...
def find_executable(executable: str, path: str | None = None) -> str | None:
    """
    Tries to find 'executable' in the directories listed in 'path'.

    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    ...

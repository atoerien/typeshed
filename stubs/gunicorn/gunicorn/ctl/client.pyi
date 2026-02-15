"""
Control Socket Client

Client library for connecting to gunicorn control socket.
"""

from _typeshed import Incomplete, Unused
from typing_extensions import Self

class ControlClientError(Exception):
    """Control client error."""
    ...

class ControlClient:
    """
    Client for connecting to gunicorn control socket.

    Can be used as a context manager:

        with ControlClient('/path/to/gunicorn.ctl') as client:
            result = client.send_command('show workers')
    """
    socket_path: str
    timeout: float
    def __init__(self, socket_path: str, timeout: float = 30.0) -> None:
        """
        Initialize control client.

        Args:
            socket_path: Path to the Unix socket
            timeout: Socket timeout in seconds (default 30)
        """
        ...
    def connect(self) -> None:
        """
        Connect to control socket.

        Raises:
            ControlClientError: If connection fails
        """
        ...
    def close(self) -> None:
        """Close connection."""
        ...
    def send_command(self, command: str, args: list[str] | None = None) -> dict[Incomplete, Incomplete]:
        """
        Send command and wait for response.

        Args:
            command: Command string (e.g., "show workers")
            args: Optional additional arguments

        Returns:
            Response data dictionary

        Raises:
            ControlClientError: If communication fails
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: Unused) -> None: ...

def parse_command(line: str) -> tuple[str, list[str]]:
    """
    Parse a command line into command and args.

    Args:
        line: Command line string

    Returns:
        Tuple of (command_string, args_list)
    """
    ...

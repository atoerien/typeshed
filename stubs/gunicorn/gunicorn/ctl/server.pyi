"""
Control Socket Server

Runs in the arbiter process and accepts commands via Unix socket.
Uses asyncio in a background thread to handle client connections.

Fork Safety:
    This server uses os.register_at_fork() to properly handle fork() calls.
    Before fork: the asyncio thread is stopped to prevent lock issues.
    After fork in parent: the server is restarted.
    After fork in child: references are cleared (workers don't need the control server).
"""

from gunicorn.arbiter import Arbiter
from gunicorn.ctl.handlers import CommandHandlers

class ControlSocketServer:
    """
    Control socket server running in arbiter process.

    The server runs an asyncio event loop in a background thread,
    accepting connections and dispatching commands to handlers.

    Fork safety is handled via os.register_at_fork() - the server
    automatically stops before fork and restarts after in the parent.
    """
    arbiter: Arbiter
    socket_path: str
    socket_mode: int
    handlers: CommandHandlers
    def __init__(self, arbiter: Arbiter, socket_path: str, socket_mode: int = 0o600) -> None:
        """
        Initialize control socket server.

        Args:
            arbiter: The Gunicorn arbiter instance
            socket_path: Path for the Unix socket
            socket_mode: Permission mode for socket (default 0o600)
        """
        ...
    def start(self) -> None:
        """Start server in background thread with asyncio event loop."""
        ...
    def stop(self) -> None:
        """Stop server and cleanup socket."""
        ...

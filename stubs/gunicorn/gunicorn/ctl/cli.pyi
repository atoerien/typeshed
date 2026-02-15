"""
gunicornc - Gunicorn control interface CLI

Interactive and single-command modes for controlling Gunicorn instances.
"""

from _typeshed import Incomplete

def format_workers(data: dict[str, Incomplete]) -> str:
    """Format workers output for display."""
    ...
def format_dirty(data: dict[str, Incomplete]) -> str:
    """Format dirty workers output for display."""
    ...
def format_stats(data: dict[str, Incomplete]) -> str:
    """Format stats output for display."""
    ...
def format_listeners(data: dict[str, Incomplete]) -> str:
    """Format listeners output for display."""
    ...
def format_config(data: dict[str, Incomplete]) -> str:
    """Format config output for display."""
    ...
def format_help(data: dict[str, Incomplete]) -> str:
    """Format help output for display."""
    ...
def format_all(data: dict[str, Incomplete]) -> str:
    """Format show all output for display."""
    ...
def format_response(command: str, data: dict[str, Incomplete]) -> str:
    """
    Format response data based on command.

    Args:
        command: Original command string
        data: Response data dictionary

    Returns:
        Formatted string for display
    """
    ...
def run_command(socket_path: str, command: str, json_output: bool = False) -> int:
    """
    Execute single command and exit.

    Args:
        socket_path: Path to control socket
        command: Command to execute
        json_output: If True, output raw JSON

    Returns:
        Exit code (0 for success, 1 for error)
    """
    ...
def run_interactive(socket_path: str, json_output: bool = False) -> int:
    """
    Run interactive CLI with readline support.

    Args:
        socket_path: Path to control socket
        json_output: If True, output raw JSON

    Returns:
        Exit code
    """
    ...
def main() -> int:
    """Main entry point for gunicornc CLI."""
    ...

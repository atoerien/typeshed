"""Interfaces for launching and remotely controlling web browsers."""

import sys
from abc import abstractmethod
from collections.abc import Callable, Sequence
from typing import Literal
from typing_extensions import deprecated

__all__ = ["Error", "open", "open_new", "open_new_tab", "get", "register"]

class Error(Exception): ...

def register(
    name: str, klass: Callable[[], BaseBrowser] | None, instance: BaseBrowser | None = None, *, preferred: bool = False
) -> None: ...
def get(using: str | None = None) -> BaseBrowser: ...
def open(url: str, new: int = 0, autoraise: bool = True) -> bool: ...
def open_new(url: str) -> bool: ...
def open_new_tab(url: str) -> bool: ...
def register_standard_browsers() -> None: ...

class BaseBrowser:
    """Parent class for all browsers. Do not use directly."""
    args: list[str]
    name: str
    basename: str
    def __init__(self, name: str = "") -> None: ...
    @abstractmethod
    def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...
    def open_new(self, url: str) -> bool: ...
    def open_new_tab(self, url: str) -> bool: ...

class GenericBrowser(BaseBrowser):
    """
    Class for all browsers started with a command
    and without remote functionality.
    """
    def __init__(self, name: str | Sequence[str]) -> None: ...
    def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

class BackgroundBrowser(GenericBrowser):
    """
    Class for all browsers which are to be started in the
    background.
    """
    ...

class UnixBrowser(BaseBrowser):
    """Parent class for all Unix browsers with remote functionality."""
    def open(self, url: str, new: Literal[0, 1, 2] = 0, autoraise: bool = True) -> bool: ...  # type: ignore[override]
    raise_opts: list[str] | None
    background: bool
    redirect_stdout: bool
    remote_args: list[str]
    remote_action: str
    remote_action_newwin: str
    remote_action_newtab: str

class Mozilla(UnixBrowser):
    """Launcher class for Mozilla browsers."""
    ...

if sys.version_info < (3, 12):
    class Galeon(UnixBrowser):
        """Launcher class for Galeon/Epiphany browsers."""
        raise_opts: list[str]

    class Grail(BaseBrowser):
        def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

class Chrome(UnixBrowser):
    """Launcher class for Google Chrome browser."""
    ...
class Opera(UnixBrowser):
    """Launcher class for Opera browser."""
    ...
class Elinks(UnixBrowser):
    """Launcher class for Elinks browsers."""
    ...

class Konqueror(BaseBrowser):
    """
    Controller for the KDE File Manager (kfm, or Konqueror).

    See the output of ``kfmclient --commands``
    for more information on the Konqueror remote-control interface.
    """
    def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

if sys.platform == "win32":
    class WindowsDefault(BaseBrowser):
        def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

if sys.platform == "darwin":
    if sys.version_info < (3, 13):
        @deprecated("Deprecated; removed in Python 3.13.")
        class MacOSX(BaseBrowser):
            def __init__(self, name: str) -> None: ...
            def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

    class MacOSXOSAScript(BaseBrowser):  # In runtime this class does not have `name` and `basename`
        if sys.version_info >= (3, 11):
            def __init__(self, name: str = "default") -> None: ...
        else:
            def __init__(self, name: str) -> None: ...

        def open(self, url: str, new: int = 0, autoraise: bool = True) -> bool: ...

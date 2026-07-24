"""
Sends updates to a Slack app.

Usage:
>>> from tqdm.contrib.slack import tqdm, trange
>>> for i in trange(10, token='{token}', channel='{channel}'):
...     ...

![screenshot](https://tqdm.github.io/img/screenshot-slack.png)
"""

from _typeshed import Incomplete, SupportsWrite
from collections.abc import Iterable, Mapping
from typing import TypeVar, overload
from typing_extensions import Never

from ..auto import tqdm as tqdm_auto
from .utils_worker import MonoWorker

__all__ = ["SlackIO", "tqdm_slack", "tsrange", "tqdm", "trange"]

class SlackIO(MonoWorker):
    """Non-blocking file-like IO using a Slack app."""
    client: Incomplete
    text: Incomplete
    message: Incomplete
    def __init__(self, token, channel) -> None:
        """Creates a new message in the given `channel`."""
        ...
    def write(self, s):
        """Replaces internal `message`'s text with `s`."""
        ...

_T = TypeVar("_T")

class tqdm_slack(tqdm_auto[_T]):
    """
    Standard `tqdm.auto.tqdm` but also sends updates to a Slack app.
    May take a few seconds to create (`__init__`).

    - create a Slack app with the `chat:write` scope & invite it to a
      channel: <https://api.slack.com/authentication/basics>
    - copy the bot `{token}` & `{channel}` and paste below
    >>> from tqdm.contrib.slack import tqdm, trange
    >>> for i in tqdm(iterable, token='{token}', channel='{channel}'):
    ...     ...
    """
    sio: Incomplete

    @overload
    def __init__(
        self,
        iterable: Iterable[_T],
        desc: str | None = ...,
        total: float | None = ...,
        leave: bool | None = ...,
        file: SupportsWrite[str] | None = ...,
        ncols: int | None = ...,
        mininterval: float = ...,
        maxinterval: float = ...,
        miniters: float | None = ...,
        ascii: bool | str | None = ...,
        disable: bool | None = ...,
        unit: str = ...,
        unit_scale: bool | float = ...,
        dynamic_ncols: bool = ...,
        smoothing: float = ...,
        bar_format: str | None = ...,
        initial: float = ...,
        position: int | None = ...,
        postfix: Mapping[str, object] | str | None = ...,
        unit_divisor: float = ...,
        write_bytes: bool | None = ...,
        lock_args: tuple[bool | None, float | None] | tuple[bool | None] | None = ...,
        nrows: int | None = ...,
        colour: str | None = ...,
        delay: float | None = ...,
        gui: bool = ...,
        *,
        token: str | None = None,
        channel: int | None = None,
        **kwargs,
    ) -> None: ...
    @overload
    def __init__(
        self: tqdm_slack[Never],
        iterable: None = None,
        desc: str | None = ...,
        total: float | None = ...,
        leave: bool | None = ...,
        file: SupportsWrite[str] | None = ...,
        ncols: int | None = ...,
        mininterval: float = ...,
        maxinterval: float = ...,
        miniters: float | None = ...,
        ascii: bool | str | None = ...,
        disable: bool | None = ...,
        unit: str = ...,
        unit_scale: bool | float = ...,
        dynamic_ncols: bool = ...,
        smoothing: float = ...,
        bar_format: str | None = ...,
        initial: float = ...,
        position: int | None = ...,
        postfix: Mapping[str, object] | str | None = ...,
        unit_divisor: float = ...,
        write_bytes: bool | None = ...,
        lock_args: tuple[bool | None, float | None] | tuple[bool | None] | None = ...,
        nrows: int | None = ...,
        colour: str | None = ...,
        delay: float | None = ...,
        gui: bool = ...,
        *,
        token: str | None = None,
        channel: int | None = None,
        **kwargs,
    ) -> None: ...

    def display(  # type: ignore[override]
        self, *, msg: str | None = ..., pos: int | None = ..., close: bool = ..., bar_style=..., check_delay: bool = ...
    ) -> None: ...
    def clear(self, *args, **kwargs) -> None: ...

def tsrange(*args, **kwargs) -> tqdm_slack[int]:
    """Shortcut for `tqdm.contrib.slack.tqdm(range(*args), **kwargs)`."""
    ...

tqdm = tqdm_slack
trange = tsrange

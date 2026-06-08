"""
Sends updates to a Discord bot.

Usage:
>>> from tqdm.contrib.discord import tqdm, trange
>>> for i in trange(10, token='{token}', channel_id='{channel_id}'):
...     ...

![screenshot](https://tqdm.github.io/img/screenshot-discord.png)
"""

from _typeshed import Incomplete, SupportsWrite
from collections.abc import Iterable, Mapping
from concurrent.futures import Future
from typing import NoReturn, TypeVar, overload

from requests import Session

from ..auto import tqdm as tqdm_auto
from .utils_worker import MonoWorker

__all__ = ["DiscordIO", "tqdm_discord", "tdrange", "tqdm", "trange"]

class DiscordIO(MonoWorker):
    """Non-blocking file-like IO using a Discord Bot."""
    API: str = "https://discord.com/api/v10"
    UA: str = ...
    channel_id: Incomplete
    message: Incomplete
    session: Session
    text: Incomplete
    token: Incomplete
    def __init__(self, token, channel_id) -> None:
        """Creates a new message in the given `channel_id`."""
        ...
    def write(self, s):
        """Replaces internal `message_id`'s text with `s`."""
        ...
    def delete(self) -> Future[Incomplete]:
        """Deletes internal `message_id`."""
        ...
    @property
    def message_id(self): ...

_T = TypeVar("_T")

class tqdm_discord(tqdm_auto[_T]):
    """
    Standard `tqdm.auto.tqdm` but also sends updates to a Discord Bot.
    May take a few seconds to create (`__init__`).

    - create a discord bot (not public, no requirement of OAuth2 code
      grant, only send message permissions) & invite it to a channel:
      <https://discordpy.readthedocs.io/en/latest/discord.html>
    - copy the bot `{token}` & `{channel_id}` and paste below

    >>> from tqdm.contrib.discord import tqdm, trange
    >>> for i in tqdm(iterable, token='{token}', channel_id='{channel_id}'):
    ...     ...
    """
    dio: Incomplete

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
        channel_id: str | None = None,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        token  : str, required. Discord bot token
            [default: ${TQDM_DISCORD_TOKEN}].
        channel_id  : int, required. Discord channel ID
            [default: ${TQDM_DISCORD_CHANNEL_ID}].

        See `tqdm.auto.tqdm.__init__` for other parameters.
        """
        ...
    @overload
    def __init__(
        self: tqdm_discord[NoReturn],
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
        channel_id: str | None = None,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        token  : str, required. Discord bot token
            [default: ${TQDM_DISCORD_TOKEN}].
        channel_id  : int, required. Discord channel ID
            [default: ${TQDM_DISCORD_CHANNEL_ID}].

        See `tqdm.auto.tqdm.__init__` for other parameters.
        """
        ...

    def display(  # type: ignore[override]
        self, *, msg: str | None = ..., pos: int | None = ..., close: bool = ..., bar_style=..., check_delay: bool = ...
    ) -> None: ...
    def clear(self, *args, **kwargs) -> None: ...

def tdrange(*args, **kwargs) -> tqdm_discord[int]:
    """Shortcut for `tqdm.contrib.discord.tqdm(range(*args), **kwargs)`."""
    ...

tqdm = tqdm_discord
trange = tdrange

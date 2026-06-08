"""
Sends updates to a Telegram bot.

Usage:
>>> from tqdm.contrib.telegram import tqdm, trange
>>> for i in trange(10, token='{token}', chat_id='{chat_id}'):
...     ...

![screenshot](https://tqdm.github.io/img/screenshot-telegram.gif)
"""

from _typeshed import Incomplete, SupportsWrite
from collections.abc import Iterable, Mapping
from typing import NoReturn, TypeVar, overload

from ..auto import tqdm as tqdm_auto
from .utils_worker import MonoWorker

__all__ = ["TelegramIO", "tqdm_telegram", "ttgrange", "tqdm", "trange"]

class TelegramIO(MonoWorker):
    """Non-blocking file-like IO using a Telegram Bot."""
    API: str
    token: Incomplete
    chat_id: Incomplete
    session: Incomplete
    text: Incomplete
    def __init__(self, token, chat_id) -> None:
        """Creates a new message in the given `chat_id`."""
        ...
    @property
    def message_id(self): ...
    def write(self, s: str) -> Incomplete | None:
        """Replaces internal `message_id`'s text with `s`."""
        ...
    def delete(self):
        """Deletes internal `message_id`."""
        ...

_T = TypeVar("_T")

class tqdm_telegram(tqdm_auto[_T]):
    """
    Standard `tqdm.auto.tqdm` but also sends updates to a Telegram Bot.
    May take a few seconds to create (`__init__`).

    - create a bot <https://core.telegram.org/bots#6-botfather>
    - copy its `{token}`
    - add the bot to a chat and send it a message such as `/start`
    - go to <https://api.telegram.org/bot`{token}`/getUpdates> to find out
      the `{chat_id}`
    - paste the `{token}` & `{chat_id}` below

    >>> from tqdm.contrib.telegram import tqdm, trange
    >>> for i in tqdm(iterable, token='{token}', chat_id='{chat_id}'):
    ...     ...
    """
    tgio: Incomplete

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
        chat_id: str | None = None,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        token  : str, required. Telegram token
            [default: ${TQDM_TELEGRAM_TOKEN}].
        chat_id  : str, required. Telegram chat ID
            [default: ${TQDM_TELEGRAM_CHAT_ID}].

        See `tqdm.auto.tqdm.__init__` for other parameters.
        """
        ...
    @overload
    def __init__(
        self: tqdm_telegram[NoReturn],
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
        chat_id: str | None = None,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        token  : str, required. Telegram token
            [default: ${TQDM_TELEGRAM_TOKEN}].
        chat_id  : str, required. Telegram chat ID
            [default: ${TQDM_TELEGRAM_CHAT_ID}].

        See `tqdm.auto.tqdm.__init__` for other parameters.
        """
        ...

    def display(  # type: ignore[override]
        self, *, msg: str | None = ..., pos: int | None = ..., close: bool = ..., bar_style=..., check_delay: bool = ...
    ) -> None: ...
    def clear(self, *args, **kwargs) -> None: ...
    def close(self) -> None: ...

def ttgrange(*args, **kwargs) -> tqdm_telegram[int]:
    """Shortcut for `tqdm.contrib.telegram.tqdm(range(*args), **kwargs)`."""
    ...

tqdm = tqdm_telegram
trange = ttgrange

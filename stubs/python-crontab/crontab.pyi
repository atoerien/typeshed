"""
from crontab import CronTab
import sys

# Create a new non-installed crontab
cron = CronTab(tab='')
job  = cron.new(command='/usr/bin/echo')

job.minute.during(5,50).every(5)
job.hour.every(4)

job.dow.on('SUN')
job.month.during('APR', 'JUN')
job.month.also.during('OCT', 'DEC')

job.every(2).days()
job.setall(1, 12, None, None, None)

job2 = cron.new(command='/foo/bar', comment='SomeID')
job2.every_reboot()

jobs = list(cron.find_command('bar'))
job3 = jobs[0]
job3.clear()
job3.minute.every(1)

sys.stdout.write(str(cron.render()))

job3.enable(False)

for job4 in cron.find_command('echo'):
    sys.stdout.write(job4)

for job5 in cron.find_comment('SomeID'):
    sys.stdout.write(job5)

for job6 in cron:
    sys.stdout.write(job6)

for job7 in cron:
    job7.every(3).hours()
    sys.stdout.write(job7)
    job7.every().dow()

cron.remove_all(command='/foo/bar')
cron.remove_all(comment='This command')
cron.remove_all(time='* * * * *')
cron.remove_all()

output = cron.render()

cron.write()

cron.write(filename='/tmp/output.txt')

#cron.write_to_user(user=True)

#cron.write_to_user(user='root')

# Croniter Extentions allow you to ask for the scheduled job times, make
# sure you have croniter installed, it's not a hard dependancy.

job3.schedule().get_next()
job3.schedule().get_prev()
"""

import re
import subprocess
from _typeshed import StrPath
from builtins import range as _range
from collections import OrderedDict
from collections.abc import Callable, Generator, Iterable, Iterator
from datetime import datetime
from logging import Logger
from types import TracebackType
from typing import Any, Final, Literal, Protocol, SupportsIndex, TypeAlias, TypeVar, overload, type_check_only
from typing_extensions import Self

from croniter.croniter import croniter
from cronlog import CronLog

_User: TypeAlias = str | bool | None
_K = TypeVar("_K")
_V = TypeVar("_V")

# cron_descriptor.Options class
@type_check_only
class _Options(Protocol):
    casing_type: Literal[1, 2, 3]
    verbose: bool
    day_of_week_start_index_zero: bool
    use_24hour_time_format: bool
    locale_location: StrPath | None
    locale_code: str | None
    def __init__(self) -> None: ...

__pkgname__: Final[str]
__version__: Final[str]
ITEMREX: Final[re.Pattern[str]]
SPECREX: Final[re.Pattern[str]]
DEVNULL: Final[str]
WEEK_ENUM: Final[list[str]]
MONTH_ENUM: Final[list[str | None]]
SPECIALS_CONVERSION: Final[bool]
SPECIALS: Final[dict[str, str]]
SPECIAL_IGNORE: Final[list[str]]
S_INFO: Final[list[dict[str, str | int | list[str] | list[str | None]]]]
WINOS: Final[bool]
POSIX: Final[bool]
SYSTEMV: Final[bool]
ZERO_PAD: Final[bool]
LOG: Logger
CRON_COMMAND: Final[str]
SHELL: Final[str]
current_user: Callable[[], str | None]

class Process:
    """
    Runs a program and orders the arguments for compatability.

    a. keyword args are flags and always appear /before/ arguments for bsd
    """
    env: subprocess._ENV | None
    args: tuple[str, ...]
    has_run: bool
    stdout: str | None
    stderr: str | None
    returncode: int | None
    # `posix` and `env` are known special kwargs:
    def __init__(self, cmd: str, *args: str, posix: bool = ..., env: subprocess._ENV | None = None, **flags: object) -> None: ...
    def run(self) -> Self:
        """Run this process and store whatever is returned"""
        ...
    def __int__(self) -> int: ...  # technically, it can return `None` before `run` is called
    def __eq__(self, other: object) -> bool: ...

class CronTab:
    """
    Crontab object which can access any time based cron using the standard.

    user    - Set the user of the crontab (default: None)
      * 'user' = Load from $username's crontab (instead of tab or tabfile)
      * None   = Don't load anything from any user crontab.
      * True   = Load from current $USER's crontab (unix only)
      * False  = This is a system crontab, each command has a username

    tab     - Use a string variable as the crontab instead of installed crontab
    tabfile - Use a file for the crontab instead of installed crontab
    log     - Filename for logfile instead of /var/log/syslog
    """
    lines: list[str | CronItem] | None
    crons: list[CronItem] | None
    filen: str | None
    cron_command: str
    env: OrderedVariableList[str, str] | None
    root: bool
    intab: str | None
    tabfile: str | None
    def __init__(
        self, user: _User = None, tab: str | None = None, tabfile: str | None = None, log: CronLog | str | None = None
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    @property
    def log(self) -> CronLog:
        """Returns the CronLog object for this tab (user or root tab only)"""
        ...
    @property
    def user(self) -> _User:
        """Return user's username of this crontab if applicable"""
        ...
    @property
    def user_opt(self) -> dict[str, str]: ...
    def read(self, filename: str | None = None) -> None: ...
    def append(
        self,
        item: CronItem,
        line: str = "",
        read: bool = False,
        before: str | re.Pattern[str] | list[CronItem] | tuple[CronItem, ...] | Generator[CronItem] | None = None,
    ) -> None: ...
    def write(self, filename: str | None = None, user: _User = None, errors: bool = False) -> None: ...
    def write_to_user(self, user: bool | str = True) -> None: ...
    # Usually `kwargs` are just `now: datetime | None`, but technically this can
    # work for `CronItem` subclasses, which might define other kwargs.
    def run_pending(self, *, now: datetime | None = None, **kwargs: Any) -> Iterator[str]: ...
    def run_scheduler(self, timeout: int = -1, cadence: int = 60, warp: bool = False) -> Iterator[str]: ...
    def render(self, errors: bool = False) -> str: ...
    def new(
        self,
        command: str = "",
        comment: str = "",
        user: str | None = None,
        pre_comment: bool = False,
        before: str | re.Pattern[str] | list[CronItem] | tuple[CronItem, ...] | Generator[CronItem] | None = None,
    ) -> CronItem: ...
    def find_command(self, command: str | re.Pattern[str]) -> Iterator[CronItem]: ...
    def find_comment(self, comment: str | re.Pattern[str]) -> Iterator[CronItem]: ...
    def find_time(self, *args: Any) -> Iterator[CronItem]: ...
    @property
    def commands(self) -> Iterator[str]:
        """Return a generator of all unqiue commands used in this crontab"""
        ...
    @property
    def comments(self) -> Iterator[str]:
        """Return a generator of all unique comments/Id used in this crontab"""
        ...
    # You cannot actually pass `*args`, it will raise an exception,
    # also known kwargs are added:
    def remove_all(
        self, *, command: str | re.Pattern[str] = ..., comment: str | re.Pattern[str] = ..., time: Any = ..., **kwargs: object
    ) -> int:
        """
        Removes all crons using the stated command OR that have the
        stated comment OR removes everything if no arguments specified.

           command - Remove all with this command
           comment - Remove all with this comment or ID
           time    - Remove all with this time code
        """
        ...
    def remove(self, *items: CronItem | Iterable[CronItem]) -> int:
        """Remove a selected cron from the crontab."""
        ...
    def __iter__(self) -> Iterator[CronItem]:
        """Return generator so we can track jobs after removal"""
        ...
    def __getitem__(self, i: SupportsIndex) -> CronItem: ...
    def __len__(self) -> int: ...

class CronItem:
    """
    An item which objectifies a single line of a crontab and
    May be considered to be a cron job object.
    """
    cron: CronTab | None
    user: _User
    valid: bool
    enabled: bool
    special: bool
    comment: str
    command: str | None
    last_run: datetime | None
    env: OrderedVariableList[str, str]
    pre_comment: bool
    marker: str | None
    stdin: str | None
    slices: CronSlices
    def __init__(self, command: str = "", comment: str = "", user: _User = None, pre_comment: bool = False) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    @classmethod
    def from_line(cls, line: str, user: str | None = None, cron: CronTab | None = None) -> Self: ...
    def delete(self) -> None: ...
    def set_command(self, cmd: str, parse_stdin: bool = False) -> None: ...
    def set_comment(self, cmt: str, pre_comment: bool = False) -> None: ...
    def parse(self, line: str) -> None: ...
    def enable(self, enabled: bool = True) -> bool: ...
    def is_enabled(self) -> bool: ...
    def is_valid(self) -> bool: ...
    def render(self) -> str: ...
    def every_reboot(self) -> None: ...
    def every(self, unit: int = 1) -> Every: ...
    def setall(self, *args: Any) -> None: ...
    def clear(self) -> None: ...
    def frequency(self, year: int | None = None) -> int: ...
    def frequency_per_year(self, year: int | None = None) -> int: ...
    def frequency_per_day(self) -> int: ...
    def frequency_per_hour(self) -> int: ...
    def frequency_at_year(self, year: int | None = None) -> int: ...

    @overload
    def frequency_at_month(self, year: int, month: int) -> int:
        """
        Returns the number of times this item will execute in a given month
        (defaults to this month)
        """
        ...
    @overload
    def frequency_at_month(self, year: None = None, month: None = None) -> int:
        """
        Returns the number of times this item will execute in a given month
        (defaults to this month)
        """
        ...

    @overload
    def frequency_at_day(self, year: int, month: int, day: int) -> int:
        """
        Returns the number of times this item will execute in a given day
        (defaults to today)
        """
        ...
    @overload
    def frequency_at_day(self, year: None = None, month: None = None, day: None = None) -> int:
        """
        Returns the number of times this item will execute in a given day
        (defaults to today)
        """
        ...

    @overload
    def frequency_at_hour(self, year: int, month: int, day: int, hour: int) -> int:
        """
        Returns the number of times this item will execute in a given hour
        (defaults to this hour)
        """
        ...
    @overload
    def frequency_at_hour(self, year: None = None, month: None = None, day: None = None, hour: None = None) -> int:
        """
        Returns the number of times this item will execute in a given hour
        (defaults to this hour)
        """
        ...

    def run_pending(self, now: datetime | None = None) -> int | str: ...
    def run(self) -> str: ...
    def schedule(self, date_from: datetime | None = None) -> croniter: ...
    def description(
        self,
        *,
        options: _Options | None = None,
        casing_type: Literal[1, 2, 3] = 2,
        verbose: bool = False,
        day_of_week_start_index_zero: bool = True,
        use_24hour_time_format: bool = ...,
        locale_location: StrPath | None = None,
        locale_code: str | None = ...,
    ) -> str | None:
        """
        Returns a description of the crontab's schedule (if available)

        **kw - Keyword arguments to pass to cron_descriptor (see docs)
        """
        ...
    @property
    def log(self) -> CronLog:
        """Return a cron log specific for this job only"""
        ...
    @property
    def minute(self) -> int | str:
        """Return the minute slice"""
        ...
    @property
    def minutes(self) -> int | str:
        """Same as minute"""
        ...
    @property
    def hour(self) -> int | str:
        """Return the hour slice"""
        ...
    @property
    def hours(self) -> int | str:
        """Same as hour"""
        ...
    @property
    def day(self) -> int | str:
        """Return the day slice"""
        ...
    @property
    def dom(self) -> int | str:
        """Return the day-of-the month slice"""
        ...
    @property
    def month(self) -> int | str:
        """Return the month slice"""
        ...
    @property
    def months(self) -> int | str:
        """Same as month"""
        ...
    @property
    def dow(self) -> int | str:
        """Return the day of the week slice"""
        ...
    def __len__(self) -> int: ...
    def __getitem__(self, key: int | str) -> int | str: ...
    def __lt__(self, value: object) -> bool: ...
    def __gt__(self, value: object) -> bool: ...

class Every:
    """
    Provide an interface to the job.every() method:
     Available Calls:
       minute, minutes, hour, hours, dom, doms, month, months, dow, dows

    Once run all units will be cleared (set to *) then proceeding units
    will be set to '0' and the target unit will be set as every x units.
    """
    slices: CronSlices
    unit: int
    # TODO: add generated attributes
    def __init__(self, item: CronSlices, units: int) -> None: ...
    def set_attr(self, target: int) -> Callable[[], None]:
        """Inner set target, returns function"""
        ...
    def year(self) -> None:
        """Special every year target"""
        ...

class CronSlices(list[CronSlice]):
    """
    Controls a list of five time 'slices' which reprisent:
    minute frequency, hour frequency, day of month frequency,
    month requency and finally day of the week frequency.
    """
    special: bool | None
    def __init__(self, *args: Any) -> None: ...
    def is_self_valid(self, *args: Any) -> bool:
        """Object version of is_valid"""
        ...
    @classmethod
    def is_valid(cls, *args: Any) -> bool: ...
    def setall(self, *slices: str) -> None: ...
    def clean_render(self) -> str: ...
    def render(self) -> str: ...
    def clear(self) -> None: ...
    def frequency(self, year: int | None = None) -> int: ...
    def frequency_per_year(self, year: int | None = None) -> int: ...
    def frequency_per_day(self) -> int: ...
    def frequency_per_hour(self) -> int: ...
    def frequency_at_year(self, year: int | None = None) -> int: ...

    @overload
    def frequency_at_month(self, year: int, month: int) -> int:
        """
        Returns the number of times this item will execute in given month
        (default: current month)
        """
        ...
    @overload
    def frequency_at_month(self, year: None = None, month: None = None) -> int:
        """
        Returns the number of times this item will execute in given month
        (default: current month)
        """
        ...

    @overload
    def frequency_at_day(self, year: int, month: int, day: int) -> int:
        """
        Returns the number of times this item will execute in a day
        (default: any executed day)
        """
        ...
    @overload
    def frequency_at_day(self, year: None = None, month: None = None, day: None = None) -> int:
        """
        Returns the number of times this item will execute in a day
        (default: any executed day)
        """
        ...

    @overload
    def frequency_at_hour(self, year: int, month: int, day: int, hour: int) -> int:
        """
        Returns the number of times this item will execute in a hour
        (default: any executed hour)
        """
        ...
    @overload
    def frequency_at_hour(self, year: None = None, month: None = None, day: None = None, hour: None = None) -> int:
        """
        Returns the number of times this item will execute in a hour
        (default: any executed hour)
        """
        ...

    def __eq__(self, arg: object) -> bool: ...

class SundayError(KeyError):
    """Sunday was specified as 7 instead of 0"""
    ...

class Also:
    """Link range values together (appending instead of replacing)"""
    obj: CronSlice
    def __init__(self, obj: CronSlice) -> None: ...
    # These method actually use `*args`, but pass them to `CronSlice` methods,
    # this is why they are typed as `Any`.
    def every(self, *a: Any) -> _Part:
        """Also every one of these"""
        ...
    def on(self, *a: Any) -> list[_Part]:
        """Also on these"""
        ...
    def during(self, *a: Any) -> _Part:
        """Also during these"""
        ...

_Part: TypeAlias = int | CronValue | CronRange

class CronSlice:
    """Cron slice object which shows a time pattern"""
    min: int | None
    max: int | None
    name: str | None
    enum: list[str | None] | None
    parts: list[_Part]
    def __init__(self, info: int | dict[str, Any], value: str | None = None) -> None: ...
    def __hash__(self) -> int: ...
    def parse(self, value: str | None) -> None:
        """Set values into the slice."""
        ...
    def render(self, resolve: bool = False) -> str:
        """
        Return the slice rendered as a crontab.

        resolve - return integer values instead of enums (default False)
        """
        ...
    def __eq__(self, arg: object) -> bool: ...
    def every(self, n_value: int, also: bool = False) -> _Part: ...
    # The only known kwarg, others are unused,
    # `*args`` are passed to `parse_value`, so they are `Any`
    def on(self, *n_value: Any, also: bool = False) -> list[_Part]: ...
    def during(self, vfrom: int | str, vto: int | str, also: bool = False) -> _Part: ...
    @property
    def also(self) -> Also: ...
    def clear(self) -> None: ...
    def get_range(self, *vrange: int | str | CronValue) -> list[int | CronRange]: ...
    def __iter__(self) -> Iterator[int]: ...
    def __len__(self) -> int: ...
    def parse_value(self, val: str, sunday: int | None = None) -> int | CronValue: ...
    def test_value(self, value: str, sunday: int | None = None) -> str: ...

def get_cronvalue(value: int, enums: list[str]) -> int | CronValue:
    """Returns a value as int (pass-through) or a special enum value"""
    ...

class CronValue:
    """Represent a special value in the cron line"""
    text: str
    value: int
    def __init__(self, value: str, enums: list[str]) -> None: ...
    def __lt__(self, value: object) -> bool: ...
    def __int__(self) -> int: ...

class CronRange:
    """A range between one value and another for a time range."""
    dangling: int | None
    slice: str
    cron: CronTab | None
    seq: int
    def __init__(self, vslice: str, *vrange: int | str | CronValue) -> None: ...
    # Are not set in `__init__`:
    vfrom: int | CronValue
    vto: int | CronValue
    def parse(self, value: str) -> None: ...
    def all(self) -> None: ...
    def render(self, resolve: bool = False) -> str: ...
    def range(self) -> _range: ...
    def every(self, value: int | str) -> None: ...
    def __lt__(self, value: object) -> bool: ...
    def __gt__(self, value: object) -> bool: ...
    def __int__(self) -> int: ...

class OrderedVariableList(OrderedDict[_K, _V]):
    """
    An ordered dictionary with a linked list containing
    the previous OrderedVariableList which this list depends.

    Duplicates in this list are weeded out in favour of the previous
    list in the chain.

    This is all in aid of the ENV variables list which must exist one
    per job in the chain.
    """
    job: CronItem | None
    # You cannot actually pass `*args`, it will raise an exception,
    # also known kwargs are added:
    def __init__(self, *, job: CronItem | None = None, **kw: _V) -> None: ...
    @property
    def previous(self) -> Self | None:
        """Returns the previous env in the list of jobs in the cron"""
        ...
    def all(self) -> Self:
        """
        Returns the full dictionary, everything from this dictionary
        plus all those in the chain above us.
        """
        ...
    def __getitem__(self, key: _K) -> _V: ...

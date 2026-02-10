import re
from datetime import datetime
from time import struct_time
from typing import Final, Protocol, type_check_only

TIME_MATCHER: Final[re.Pattern[str]]
MS_SEARCHER: Final[re.Pattern[str]]

@type_check_only
class _strptime_time(Protocol):
    def __call__(self, data_string: str, format: str = "%a %b %d %H:%M:%S %Y") -> struct_time: ...

def patch_strptime() -> _strptime_time:
    """
    Monkey patching _strptime to avoid problems related with non-english
    locale changes on the system.

    For example, if system's locale is set to fr_FR. Parser won't recognize
    any date since all languages are translated to english dates.
    """
    ...
def strptime(date_string: str, format: str) -> datetime: ...

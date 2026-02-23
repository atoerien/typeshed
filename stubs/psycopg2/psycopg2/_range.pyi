"""Implementation of the Range type and adaptation"""

import datetime as dt
from _typeshed import SupportsAllComparisons
from typing import Any, Generic, TypeVar, overload
from typing_extensions import Self

from psycopg2._psycopg import _type, connection, cursor

_T_co = TypeVar("_T_co", covariant=True)

class Range(Generic[_T_co]):
    __slots__ = ("_lower", "_upper", "_bounds")
    def __init__(
        self, lower: _T_co | None = None, upper: _T_co | None = None, bounds: str = "[)", empty: bool = False
    ) -> None: ...
    @property
    def lower(self) -> _T_co | None:
        """The lower bound of the range. `!None` if empty or unbound."""
        ...
    @property
    def upper(self) -> _T_co | None:
        """The upper bound of the range. `!None` if empty or unbound."""
        ...
    @property
    def isempty(self) -> bool:
        """`!True` if the range is empty."""
        ...
    @property
    def lower_inf(self) -> bool:
        """`!True` if the range doesn't have a lower bound."""
        ...
    @property
    def upper_inf(self) -> bool:
        """`!True` if the range doesn't have an upper bound."""
        ...
    @property
    def lower_inc(self) -> bool:
        """`!True` if the lower bound is included in the range."""
        ...
    @property
    def upper_inc(self) -> bool:
        """`!True` if the upper bound is included in the range."""
        ...
    def __contains__(self, x: SupportsAllComparisons) -> bool: ...
    def __bool__(self) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __lt__(self, other: Range[_T_co]) -> bool: ...
    def __le__(self, other: Range[_T_co]) -> bool: ...
    def __gt__(self, other: Range[_T_co]) -> bool: ...
    def __ge__(self, other: Range[_T_co]) -> bool: ...

def register_range(
    pgrange: str, pyrange: str | type[Range[Any]], conn_or_curs: connection | cursor, globally: bool = False
) -> RangeCaster:
    """
    Create and register an adapter and the typecasters to convert between
    a PostgreSQL |range|_ type and a PostgreSQL `Range` subclass.

    :param pgrange: the name of the PostgreSQL |range| type. Can be
        schema-qualified
    :param pyrange: a `Range` strict subclass, or just a name to give to a new
        class
    :param conn_or_curs: a connection or cursor used to find the oid of the
        range and its subtype; the typecaster is registered in a scope limited
        to this object, unless *globally* is set to `!True`
    :param globally: if `!False` (default) register the typecaster only on
        *conn_or_curs*, otherwise register it globally
    :return: `RangeCaster` instance responsible for the conversion

    If a string is passed to *pyrange*, a new `Range` subclass is created
    with such name and will be available as the `~RangeCaster.range` attribute
    of the returned `RangeCaster` object.

    The function queries the database on *conn_or_curs* to inspect the
    *pgrange* type and raises `~psycopg2.ProgrammingError` if the type is not
    found.  If querying the database is not advisable, use directly the
    `RangeCaster` class and register the adapter and typecasters using the
    provided functions.
    """
    ...

class RangeAdapter:
    """
    `ISQLQuote` adapter for `Range` subclasses.

    This is an abstract class: concrete classes must set a `name` class
    attribute or override `getquoted()`.
    """
    name: str | None = None
    adapted: Range[Any]
    def __init__(self, adapted: Range[Any]) -> None: ...
    def __conform__(self, proto) -> Self | None: ...
    def prepare(self, conn: connection | None) -> None: ...
    def getquoted(self) -> bytes: ...

class RangeCaster:
    """
    Helper class to convert between `Range` and PostgreSQL range types.

    Objects of this class are usually created by `register_range()`. Manual
    creation could be useful if querying the database is not advisable: in
    this case the oids must be provided.
    """
    adapter: type[RangeAdapter]
    range: type[Range[Any]]
    subtype_oid: int
    typecaster: _type
    array_typecaster: _type | None
    def __init__(
        self,
        pgrange: str | type[RangeAdapter],
        pyrange: str | type[Range[Any]],
        oid: int,
        subtype_oid: int,
        array_oid: int | None = None,
    ) -> None: ...
    @overload
    def parse(self, s: None, cur: cursor | None = None) -> None: ...
    @overload
    def parse(self, s: str, cur: cursor | None = None) -> Range[Any]: ...
    @overload
    def parse(self, s: str | None, cur: cursor | None = None) -> Range[Any] | None: ...

class NumericRange(Range[float]):
    """
    A `Range` suitable to pass Python numeric types to a PostgreSQL range.

    PostgreSQL types :sql:`int4range`, :sql:`int8range`, :sql:`numrange` are
    casted into `!NumericRange` instances.
    """
    ...
class DateRange(Range[dt.date]):
    """Represents :sql:`daterange` values."""
    ...
class DateTimeRange(Range[dt.datetime]):
    """Represents :sql:`tsrange` values."""
    ...
class DateTimeTZRange(Range[dt.datetime]):
    """Represents :sql:`tstzrange` values."""
    ...

class NumberRangeAdapter(RangeAdapter):
    """Adapt a range if the subtype doesn't need quotes."""
    def getquoted(self) -> bytes: ...

int4range_caster: RangeCaster
int8range_caster: RangeCaster
numrange_caster: RangeCaster
daterange_caster: RangeCaster
tsrange_caster: RangeCaster
tstzrange_caster: RangeCaster

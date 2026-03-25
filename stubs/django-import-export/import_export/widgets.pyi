from collections.abc import Mapping
from datetime import datetime
from typing import Any, ClassVar, Generic, TypeVar, overload
from typing_extensions import deprecated

from django.db.models import Model, QuerySet

def format_datetime(value: datetime, datetime_format: str) -> str: ...

class Widget:
    """A Widget handles converting between import and export representations."""
    coerce_to_string: bool
    def __init__(self, coerce_to_string: bool = True) -> None:
        """
        :param coerce_to_string: If True, :meth:`~import_export.widgets.Widget.render`
          will return a string representation of the value, otherwise the value is
          returned.
        """
        ...
    def clean(self, value: Any, row: Mapping[str, Any] | None = None, **kwargs: Any) -> Any:
        """
        Returns an appropriate python object for an imported value.
        For example, a date string will be converted to a python datetime instance.

        :param value: The value to be converted to a native type.
        :param row: A dict containing row key/value pairs.
        :param **kwargs: Optional kwargs.
        """
        ...
    @overload
    @deprecated("The 'obj' parameter is deprecated and will be removed in a future release.")
    def render(self, value: Any, obj: Model, **kwargs: Any) -> Any:
        """
        Returns an export representation of a python value.

        :param value: The python value to be rendered.
        :param obj: The model instance from which the value is taken.
          This parameter is deprecated and will be removed in a future release.

        :return: By default, this value will be a string, with ``None`` values returned
          as empty strings.
        """
        ...
    @overload
    def render(self, value: Any, obj: None = None, **kwargs: Any) -> Any:
        """
        Returns an export representation of a python value.

        :param value: The python value to be rendered.
        :param obj: The model instance from which the value is taken.
          This parameter is deprecated and will be removed in a future release.

        :return: By default, this value will be a string, with ``None`` values returned
          as empty strings.
        """
        ...

class NumberWidget(Widget):
    """Widget for converting numeric fields."""
    def is_empty(self, value: Any) -> bool: ...

class FloatWidget(NumberWidget):
    """Widget for converting float fields."""
    ...
class IntegerWidget(NumberWidget):
    """Widget for converting integer fields."""
    ...
class DecimalWidget(NumberWidget):
    """Widget for converting decimal fields."""
    ...

class CharWidget(Widget):
    """
    Widget for converting text fields.

    :param allow_blank:  If True, then :meth:`~import_export.widgets.Widget.clean`
      will return null values as empty strings, otherwise as ``None``.
    """
    allow_blank: bool
    def __init__(self, coerce_to_string: bool = True, allow_blank: bool = True) -> None: ...

class BooleanWidget(Widget):
    """
    Widget for converting boolean fields.

    The widget assumes that ``True``, ``False``, and ``None`` are all valid
    values, as to match Django's `BooleanField
    <https://docs.djangoproject.com/en/dev/ref/models/fields/#booleanfield>`_.
    That said, whether the database/Django will actually accept NULL values
    will depend on if you have set ``null=True`` on that Django field.

    Recognizes standard boolean representations. For custom boolean values,
    see :ref:`custom_boolean_handling` in the advanced usage documentation.
    """
    TRUE_VALUES: ClassVar[list[str | int | bool]]
    FALSE_VALUES: ClassVar[list[str | int | bool]]
    NULL_VALUES: ClassVar[list[str | None]]
    def __init__(self, coerce_to_string: bool = True) -> None: ...

class DateWidget(Widget):
    """
    Widget for converting date fields to Python date instances.

    Takes optional ``format`` parameter. If none is set, either
    ``settings.DATE_INPUT_FORMATS`` or ``"%Y-%m-%d"`` is used.
    """
    formats: tuple[str, ...]
    def __init__(self, format: str | None = None, coerce_to_string: bool = True) -> None: ...

class DateTimeWidget(Widget):
    """
    Widget for converting datetime fields to Python datetime instances.

    Takes optional ``format`` parameter. If none is set, either
    ``settings.DATETIME_INPUT_FORMATS`` or ``"%Y-%m-%d %H:%M:%S"`` is used.
    """
    formats: tuple[str, ...]
    def __init__(self, format: str | None = None, coerce_to_string: bool = True) -> None: ...

class TimeWidget(Widget):
    """
    Widget for converting time fields.

    Takes optional ``format`` parameter. If none is set, either
    ``settings.DATETIME_INPUT_FORMATS`` or ``"%H:%M:%S"`` is used.
    """
    formats: tuple[str, ...]
    def __init__(self, format: str | None = None, coerce_to_string: bool = True) -> None: ...

class DurationWidget(Widget):
    """Widget for converting time duration fields."""
    ...

class SimpleArrayWidget(Widget):
    """
    Widget for an Array field. Can be used for Postgres' Array field.

    :param separator: Defaults to ``','``
    """
    separator: str
    def __init__(self, separator: str | None = None, coerce_to_string: bool = True) -> None: ...

class JSONWidget(Widget):
    """
    Widget for a JSON object
    (especially required for jsonb fields in PostgreSQL database.)

    :param value: Defaults to JSON format.
    The widget covers two cases: Proper JSON string with double quotes, else it
    tries to use single quotes and then convert it to proper JSON.
    """
    ...

_ModelT = TypeVar("_ModelT", bound=Model)

class ForeignKeyWidget(Widget, Generic[_ModelT]):
    model: type[_ModelT]
    field: str
    key_is_id: bool
    use_natural_foreign_keys: bool
    def __init__(
        self,
        model: type[_ModelT],
        field: str = "pk",
        use_natural_foreign_keys: bool = False,
        key_is_id: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def get_queryset(self, value: Any, row: Mapping[str, Any], *args: Any, **kwargs: Any) -> QuerySet[_ModelT]:
        r"""
        Returns a queryset of all objects for this Model.

        Overwrite this method if you want to limit the pool of objects from
        which the related object is retrieved.

        :param value: The field's value in the dataset.
        :param row: The dataset's current row.
        :param \*args:
            Optional args.
        :param \**kwargs:
            Optional kwargs.

        As an example; if you'd like to have ForeignKeyWidget look up a Person
        by their pre- **and** lastname column, you could subclass the widget
        like so::

            class FullNameForeignKeyWidget(ForeignKeyWidget):
                def get_queryset(self, value, row, *args, **kwargs):
                    return self.model.objects.filter(
                        first_name__iexact=row["first_name"],
                        last_name__iexact=row["last_name"]
                    )
        """
        ...
    def get_instance_by_natural_key(self, value: str | bytes | bytearray) -> _ModelT: ...
    def get_instance_by_lookup_fields(self, value: Any, row: Mapping[str, Any], **kwargs: Any) -> _ModelT: ...
    def get_lookup_kwargs(self, value: Any, row: Mapping[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        r"""
        :return: the key value pairs used to identify a model instance.
          Override this to customize instance lookup.

        :param value: The field's value in the dataset.
        :param row: The dataset's current row.
        :param \**kwargs:
            Optional kwargs.
        """
        ...

class _CachedQuerySetWrapper(Generic[_ModelT]):
    """
    A wrapper around a Django QuerySet that caches its results in a dictionary
    for quick lookups.

    This class has the same 'get()' method signature as a QuerySet
    because it is intended to be used as a drop-in replacement for QuerySet
    in case of ForeignKeyWidget that calls 'get()' method for every row
    in the import dataset.
    """
    queryset: QuerySet[_ModelT]
    model: type[_ModelT]
    def __init__(self, queryset: QuerySet[_ModelT]) -> None: ...
    def get(self, **lookup_fields: Any) -> _ModelT: ...  # instance can have different fields

class CachedForeignKeyWidget(ForeignKeyWidget[_ModelT]):
    """
    A :class:`~import_export.widgets.ForeignKeyWidget` subclass that caches
    the queryset results to minimize database hits during import. The default
    :class:`~import_export.widgets.ForeignKeyWidget` makes query for each row,
    which can be inefficient for large imports. This widget fetches all related
    instances once and caches them in memory for subsequent lookups.

    Using this class has some limitations:

    - It does not support caching when ``use_natural_foreign_keys=True`` is set.

    - It calls :meth:`~import_export.widgets.ForeignKeyWidget.get_queryset` only once,
      so if the queryset depends on the row data, this widget may not work as expected.
      You must be sure that the queryset is static for all rows.
      Avoid using :class:`~import_export.widgets.CachedForeignKeyWidget`
      in the following way::

            class FullNameForeignKeyWidget(CachedForeignKeyWidget):
                def get_queryset(self, value, row, *args, **kwargs):
                    return self.model.objects.filter(
                        first_name__iexact=row["first_name"],
                        last_name__iexact=row["last_name"]
                    )

      It makes more sense to filter by static values::

            class ActiveForeignKeyWidget(CachedForeignKeyWidget):
                def get_queryset(self, value, row, *args, **kwargs):
                    return self.model.objects.filter(active=True)

    - It stores data in a hash table where the key is a tuple of the fields that
      returned by :meth:`~import_export.widgets.ForeignKeyWidget.get_lookup_kwargs`.
      You must be sure that the lookup fields are the same for all rows.
      If the lookup fields differ between rows, this widget may not work as expected.
      The following example is incorrect usage::

            class MultiColumnForeignKeyWidget(CachedForeignKeyWidget):
                def get_lookup_kwargs(self, value, row, **kwargs):
                    if row['active'] == 'yes':
                        return {self.field: value, 'active': True}
                    else:
                        return {self.field: value, 'inactive': True}

    - It performs lookup on Python side, so the filtering logic
      with non-text data types may not work::

            class MultiColumnForeignKeyWidget(CachedForeignKeyWidget):
                def get_lookup_kwargs(self, value, row, **kwargs):
                    # row['birthday'] is a string like '01-01-2000'.
                    #
                    # It won't match the instance because the birthday values
                    # in the cached instances are datetime objects, not strings.
                    return {self.field: value, 'birthday': row['birthday']}

    - It does not support complex lookups like ``__gt``, ``__lt``,
      or filtering over relationships in the ``get_lookup_kwargs()``.
      For example, the following code won't work::

            class BookForeignKeyWidget(CachedForeignKeyWidget):
                def get_lookup_kwargs(self, value, row, **kwargs):
                    return {f'{self.field}__author': value}

    :param model: The Model the ForeignKey refers to (required).
    :param field: A field on the related model used for looking up a particular
        object.
    :param use_natural_foreign_keys: Use natural key functions to identify
        related object, default to False
    """
    def get_instance_by_lookup_fields(self, value: Any, row: Mapping[str, Any], **kwargs: Any) -> _ModelT: ...

class ManyToManyWidget(Widget, Generic[_ModelT]):
    """
    Widget that converts between representations of a ManyToMany relationships
    as a list and an actual ManyToMany field.

    :param model: The model the ManyToMany field refers to (required).
    :param separator: Defaults to ``','``.
    :param field: A field on the related model. Default is ``pk``.
    """
    model: _ModelT
    separator: str
    field: str
    def __init__(self, model: _ModelT, separator: str | None = None, field: str | None = None, **kwargs: Any) -> None: ...

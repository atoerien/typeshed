from collections.abc import Callable, Iterable
from typing import Any

from django import forms
from django.db.models import QuerySet
from django.forms import Field
from django_stubs_ext import StrOrPromise

from .fields import (
    BaseCSVField,
    BaseRangeField,
    DateRangeField,
    DateTimeRangeField,
    IsoDateTimeField,
    IsoDateTimeRangeField,
    Lookup,
    LookupChoiceField,
    ModelChoiceField,
    ModelMultipleChoiceField,
    RangeField,
    TimeRangeField,
)

__all__ = [
    "AllValuesFilter",
    "AllValuesMultipleFilter",
    "BaseCSVFilter",
    "BaseInFilter",
    "BaseRangeFilter",
    "BooleanFilter",
    "CharFilter",
    "ChoiceFilter",
    "DateFilter",
    "DateFromToRangeFilter",
    "DateRangeFilter",
    "DateTimeFilter",
    "DateTimeFromToRangeFilter",
    "DurationFilter",
    "Filter",
    "IsoDateTimeFilter",
    "IsoDateTimeFromToRangeFilter",
    "LookupChoiceFilter",
    "ModelChoiceFilter",
    "ModelMultipleChoiceFilter",
    "MultipleChoiceFilter",
    "NumberFilter",
    "NumericRangeFilter",
    "OrderingFilter",
    "RangeFilter",
    "TimeFilter",
    "TimeRangeFilter",
    "TypedChoiceFilter",
    "TypedMultipleChoiceFilter",
    "UUIDFilter",
]

class Filter:
    creation_counter: int
    field_class: type[Any]  # Subclasses specify more specific field types
    field_name: str | None
    lookup_expr: str
    distinct: bool
    exclude: bool
    extra: dict[str, Any]  # Field kwargs can include various types of parameters
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        *,
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        distinct: bool = False,
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None: ...
    def get_method(self, qs: QuerySet[Any]) -> Callable[..., QuerySet[Any]]:
        """
        Return filter method based on whether we're excluding
        or simply filtering.
        """
        ...
    method: Callable[..., Any] | str | None  # Custom filter methods return various types
    label: StrOrPromise | None  # Filter label for display
    @property
    def field(self) -> Field: ...
    def filter(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...  # Filter value can be any user input type

class CharFilter(Filter):
    field_class: type[forms.CharField]

class BooleanFilter(Filter):
    field_class: type[forms.NullBooleanField]

class ChoiceFilter(Filter):
    field_class: type[Any]  # Base class for choice-based filters
    null_value: Any  # Null value can be any type (None, empty string, etc.)
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        *,
        null_value: Any = ...,  # Null value can be any type (None, empty string, etc.)
        # Inherited from Filter
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        distinct: bool = False,
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None: ...
    def filter(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...

class TypedChoiceFilter(Filter):
    field_class: type[forms.TypedChoiceField]

class UUIDFilter(Filter):
    field_class: type[forms.UUIDField]

class MultipleChoiceFilter(Filter):
    """
    This filter performs OR(by default) or AND(using conjoined=True) query
    on the selected options.

    Advanced usage
    --------------
    Depending on your application logic, when all or no choices are selected,
    filtering may be a no-operation. In this case you may wish to avoid the
    filtering overhead, particularly if using a `distinct` call.

    You can override `get_filter_predicate` to use a custom filter.
    By default it will use the filter's name for the key, and the value will
    be the model object - or in case of passing in `to_field_name` the
    value of that attribute on the model.

    Set `always_filter` to `False` after instantiation to enable the default
    `is_noop` test. You can override `is_noop` if you need a different test
    for your application.

    `distinct` defaults to `True` as to-many relationships will generally
    require this.
    """
    field_class: type[Any]  # Base class for multiple choice filters
    always_filter: bool
    conjoined: bool
    null_value: Any  # Multiple choice null values vary by implementation
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        *,
        distinct: bool = True,  # Overrides distinct default
        conjoined: bool = False,
        null_value: Any = ...,  # Multiple choice null values vary by implementation
        # Inherited from Filter
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None: ...
    def is_noop(self, qs: QuerySet[Any], value: Any) -> bool:
        """
        Return `True` to short-circuit unnecessary and potentially slow
        filtering.
        """
        ...
    def filter(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...
    def get_filter_predicate(self, v: Any) -> dict[str, Any]: ...  # Predicate value can be any filter input type

class TypedMultipleChoiceFilter(MultipleChoiceFilter):
    field_class: type[forms.TypedMultipleChoiceField]  # More specific than parent MultipleChoiceField

class DateFilter(Filter):
    field_class: type[forms.DateField]

class DateTimeFilter(Filter):
    field_class: type[forms.DateTimeField]

class IsoDateTimeFilter(DateTimeFilter):
    """
    Uses IsoDateTimeField to support filtering on ISO 8601 formatted datetimes.

    For context see:

    * https://code.djangoproject.com/ticket/23448
    * https://github.com/encode/django-rest-framework/issues/1338
    * https://github.com/carltongibson/django-filter/pull/264
    """
    field_class: type[IsoDateTimeField]

class TimeFilter(Filter):
    field_class: type[forms.TimeField]

class DurationFilter(Filter):
    field_class: type[forms.DurationField]

class QuerySetRequestMixin:
    """
    Add callable functionality to filters that support the ``queryset``
    argument. If the ``queryset`` is callable, then it **must** accept the
    ``request`` object as a single argument.

    This is useful for filtering querysets by properties on the ``request``
    object, such as the user.

    Example::

        def departments(request):
            company = request.user.company
            return company.department_set.all()

        class EmployeeFilter(filters.FilterSet):
            department = filters.ModelChoiceFilter(queryset=departments)
            ...

    The above example restricts the set of departments to those in the logged-in
    user's associated company.
    """
    queryset: QuerySet[Any] | None
    def __init__(self, *, queryset: QuerySet[Any] | None) -> None: ...
    def get_request(self) -> Any: ...  # Request can be HttpRequest or other request types
    def get_queryset(self, request: Any) -> QuerySet[Any]: ...  # Request parameter accepts various request types
    @property
    def field(self) -> Field: ...

class ModelChoiceFilter(QuerySetRequestMixin, ChoiceFilter):
    field_class: type[ModelChoiceField]  # More specific than parent ChoiceField
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        *,
        # Inherited from QuerySetRequestMixin
        queryset: QuerySet[Any] | None = None,
        # Inherited from ChoiceFilter
        null_value: Any = ...,  # Null value can be any type (None, empty string, etc.)
        # Inherited from Filter
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        distinct: bool = False,
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None: ...

class ModelMultipleChoiceFilter(QuerySetRequestMixin, MultipleChoiceFilter):
    field_class: type[ModelMultipleChoiceField]  # More specific than parent MultipleChoiceField
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        *,
        # Inherited from QuerySetRequestMixin
        queryset: QuerySet[Any] | None = None,
        # Inherited from MultipleChoiceFilter
        distinct: bool = True,  # Overrides distinct default
        conjoined: bool = False,
        null_value: Any = ...,  # Multiple choice null values vary by implementation
        # Inherited from Filter
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None: ...

class NumberFilter(Filter):
    field_class: type[forms.DecimalField]
    def get_max_validator(self) -> Any:
        """Return a MaxValueValidator for the field, or None to disable."""
        ...
    @property
    def field(self) -> Field: ...

class NumericRangeFilter(Filter):
    field_class: type[RangeField]
    lookup_expr: str
    def filter(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...

class RangeFilter(Filter):
    field_class: type[RangeField]
    lookup_expr: str
    def filter(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...

class DateRangeFilter(ChoiceFilter):
    choices: list[tuple[str, str]] | None
    filters: dict[str, Filter] | None
    def __init__(
        self,
        choices: list[tuple[str, str]] | None = None,
        filters: dict[str, Filter] | None = None,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        *,
        # Inherited from ChoiceFilter
        null_value: Any = ...,  # Null value can be any type (None, empty string, etc.)
        # Inherited from Filter
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        distinct: bool = False,
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None: ...  # Uses args/kwargs for choice and filter configuration
    def filter(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...

class DateFromToRangeFilter(RangeFilter):
    field_class: type[DateRangeField]

class DateTimeFromToRangeFilter(RangeFilter):
    field_class: type[DateTimeRangeField]

class IsoDateTimeFromToRangeFilter(RangeFilter):
    field_class: type[IsoDateTimeRangeField]

class TimeRangeFilter(RangeFilter):
    field_class: type[TimeRangeField]

class AllValuesFilter(ChoiceFilter):
    @property
    def field(self) -> Field: ...

class AllValuesMultipleFilter(MultipleChoiceFilter):
    @property
    def field(self) -> Field: ...

class BaseCSVFilter(Filter):
    """Base class for CSV type filters, such as IN and RANGE."""
    base_field_class: type[BaseCSVField] = ...
    field_class: type[Any]  # Base class for CSV-based filters

class BaseInFilter(BaseCSVFilter): ...

class BaseRangeFilter(BaseCSVFilter):
    base_field_class: type[BaseRangeField] = ...

class LookupChoiceFilter(Filter):
    """
    A combined filter that allows users to select the lookup expression from a dropdown.

    * ``lookup_choices`` is an optional argument that accepts multiple input
      formats, and is ultimately normalized as the choices used in the lookup
      dropdown. See ``.get_lookup_choices()`` for more information.

    * ``field_class`` is an optional argument that allows you to set the inner
      form field class used to validate the value. Default: ``forms.CharField``

    ex::

        price = django_filters.LookupChoiceFilter(
            field_class=forms.DecimalField,
            lookup_choices=[
                ('exact', 'Equals'),
                ('gt', 'Greater than'),
                ('lt', 'Less than'),
            ]
        )
    """
    field_class: type[forms.CharField]
    outer_class: type[LookupChoiceField] = ...
    empty_label: StrOrPromise | None
    lookup_choices: list[tuple[str, StrOrPromise]] | None
    def __init__(
        self,
        field_name: str | None = None,
        lookup_choices: list[tuple[str, StrOrPromise]] | None = None,
        field_class: type[Field] | None = None,
        *,
        empty_label: StrOrPromise = ...,
        # Inherited from Filter
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        distinct: bool = False,
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None: ...
    @classmethod
    def normalize_lookup(cls, lookup: str | tuple[str, StrOrPromise]) -> tuple[str, StrOrPromise]:
        """
        Normalize the lookup into a tuple of ``(lookup expression, display value)``

        If the ``lookup`` is already a tuple, the tuple is not altered.
        If the ``lookup`` is a string, a tuple is returned with the lookup
        expression used as the basis for the display value.

        ex::

            >>> LookupChoiceFilter.normalize_lookup(('exact', 'Equals'))
            ('exact', 'Equals')

            >>> LookupChoiceFilter.normalize_lookup('has_key')
            ('has_key', 'Has key')
        """
        ...
    def get_lookup_choices(self) -> list[tuple[str, StrOrPromise]]:
        """
        Get the lookup choices in a format suitable for ``django.forms.ChoiceField``.
        If the filter is initialized with ``lookup_choices``, this value is normalized
        and passed to the underlying ``LookupChoiceField``. If no choices are provided,
        they are generated from the corresponding model field's registered lookups.
        """
        ...
    @property
    def field(self) -> Field: ...
    lookup_expr: str
    def filter(self, qs: QuerySet[Any], lookup: Lookup) -> QuerySet[Any]: ...

class OrderingFilter(BaseCSVFilter, ChoiceFilter):
    """
    Enable queryset ordering. As an extension of ``ChoiceFilter`` it accepts
    two additional arguments that are used to build the ordering choices.

    * ``fields`` is a mapping of {model field name: parameter name}. The
      parameter names are exposed in the choices and mask/alias the field
      names used in the ``order_by()`` call. Similar to field ``choices``,
      ``fields`` accepts the 'list of two-tuples' syntax that retains order.
      ``fields`` may also just be an iterable of strings. In this case, the
      field names simply double as the exposed parameter names.

    * ``field_labels`` is an optional argument that allows you to customize
      the display label for the corresponding parameter. It accepts a mapping
      of {field name: human readable label}. Keep in mind that the key is the
      field name, and not the exposed parameter name.

    Additionally, you can just provide your own ``choices`` if you require
    explicit control over the exposed options. For example, when you might
    want to disable descending sort options.

    This filter is also CSV-based, and accepts multiple ordering params. The
    default select widget does not enable the use of this, but it is useful
    for APIs.
    """
    # Inherits CSV field behavior for comma-separated ordering.
    # BaseCSVFilter constructs a custom ConcreteCSVField class that derives
    # from BaseCSVField.
    field_class: type[BaseCSVField]
    descending_fmt: str
    param_map: dict[str, str] | None
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        *,
        fields: dict[str, str] | Iterable[str] | Iterable[tuple[str, str]] = ...,
        field_labels: dict[str, StrOrPromise] = ...,
        # Inherited from ChoiceFilter
        null_value: Any = ...,  # Null value can be any type (None, empty string, etc.)
        # Inherited from Filter
        label: StrOrPromise | None = None,
        method: Callable[..., Any] | str | None = None,  # Filter methods can return various types
        distinct: bool = False,
        exclude: bool = False,
        **kwargs: Any,  # Field kwargs stored as extra (required, help_text, etc.)
    ) -> None:
        """
        ``fields`` may be either a mapping or an iterable.
        ``field_labels`` must be a map of field names to display labels
        """
        ...
    def get_ordering_value(self, param: str) -> str: ...
    def filter(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...
    @classmethod
    def normalize_fields(cls, fields: Any) -> list[str]:
        """Normalize the fields into an ordered map of {field name: param name}"""
        ...
    def build_choices(self, fields: Any, labels: dict[str, StrOrPromise] | None) -> list[tuple[str, str]]: ...

class FilterMethod:
    """
    This helper is used to override Filter.filter() when a 'method' argument
    is passed. It proxies the call to the actual method on the filter's parent.
    """
    f: Filter
    def __init__(self, filter_instance: Filter) -> None: ...
    def __call__(self, qs: QuerySet[Any], value: Any) -> QuerySet[Any]: ...
    @property
    def method(self) -> Callable[..., Any]:
        """Resolve the method on the parent filterset."""
        ...

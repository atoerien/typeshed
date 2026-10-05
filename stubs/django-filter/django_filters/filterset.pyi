from collections import OrderedDict
from collections.abc import Sequence
from enum import Enum
from typing import Any, ClassVar

from django.db import models
from django.db.models import Model, QuerySet
from django.forms import Form
from django.http import HttpRequest, QueryDict

from .filters import Filter

def remote_queryset(field: models.Field[Any, Any]) -> QuerySet[Any]:
    """
    Get the queryset for the other side of a relationship. This works
    for both `RelatedField`s and `ForeignObjectRel`s.
    """
    ...

class UnknownFieldBehavior(Enum):
    RAISE = "raise"
    WARN = "warn"
    IGNORE = "ignore"

class FilterSetOptions:
    model: type[Model] | None
    fields: Sequence[str] | dict[str, Sequence[str]] | str | None
    exclude: Sequence[str] | None
    filter_overrides: dict[type[models.Field[Any, Any]], dict[str, Any]]  # Field override mapping
    form: type[Form]
    unknown_field_behavior: UnknownFieldBehavior
    def __init__(self, options: Any | None = None) -> None: ...  # Meta options can be various configuration types

class FilterSetMetaclass(type):
    # Class attrs vary by definition
    def __new__(cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> FilterSetMetaclass: ...

    # Class attrs vary by definition
    @classmethod
    def get_declared_filters(cls, bases: tuple[type, ...], attrs: dict[str, Any]) -> OrderedDict[str, Filter]: ...

# Django field types vary widely - Any allows mapping all field types to their filters
FILTER_FOR_DBFIELD_DEFAULTS: dict[type[models.Field[Any, Any]], dict[str, Any]]

class BaseFilterSet:
    FILTER_DEFAULTS: ClassVar[dict[type[models.Field[Any, Any]], dict[str, Any]]] = ...  # Field type mapping
    is_bound: bool
    base_filters: OrderedDict[str, Filter]
    declared_filters: OrderedDict[str, Filter]
    data: QueryDict | dict[str, Any] | None  # Filter input data values vary
    queryset: QuerySet[Any] | None  # Base queryset for any model type
    request: HttpRequest | None
    form_prefix: str | None
    filters: OrderedDict[str, Filter]
    def __init__(
        self,
        data: QueryDict | dict[str, Any] | None = None,  # Filter data values vary
        queryset: QuerySet[Any] | None = None,  # Base queryset for any model
        *,
        request: HttpRequest | None = None,
        prefix: str | None = None,
    ) -> None: ...
    def is_valid(self) -> bool:
        """Return True if the underlying form has no errors, or False otherwise."""
        ...
    @property
    def errors(self) -> dict[str, list[str]]:
        """Return an ErrorDict for the data provided for the underlying form."""
        ...
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]:
        """
        Filter the queryset with the underlying form's `cleaned_data`. You must
        call `is_valid()` or `errors` before calling this method.

        This method should be overridden if additional filtering needs to be
        applied to the queryset before it is cached.
        """
        ...
    @property
    def qs(self) -> QuerySet[Any]: ...  # Filtered queryset of any model
    def get_form_class(self) -> type[Form]:
        """
        Returns a django Form suitable of validating the filterset data.

        This method should be overridden if the form class needs to be
        customized relative to the filterset instance.
        """
        ...
    @property
    def form(self) -> Form: ...
    @classmethod
    def get_fields(cls) -> dict[str, models.Field[Any, Any]]:
        """
        Resolve the 'fields' argument that should be used for generating filters on the
        filterset. This is 'Meta.fields' sans the fields in 'Meta.exclude'.
        """
        ...
    @classmethod
    def get_filter_name(cls, field_name: str, lookup_expr: str) -> str:
        """
        Combine a field name and lookup expression into a usable filter name.
        Exact lookups are the implicit default, so "exact" is stripped from the
        end of the filter name.
        """
        ...
    @classmethod
    def get_filters(cls) -> OrderedDict[str, Filter]:
        """
        Get all filters for the filterset. This is the combination of declared and
        generated filters.
        """
        ...
    @classmethod
    def handle_unrecognized_field(cls, field_name: str, message: str) -> None: ...
    @classmethod
    def filter_for_field(
        cls, field: models.Field[Any, Any], field_name: str, lookup_expr: str | None = None
    ) -> Filter: ...  # Accepts any Django field type
    @classmethod
    def filter_for_lookup(
        cls, field: models.Field[Any, Any], lookup_type: str  # Field type varies by model
    ) -> tuple[type[Filter], dict[str, Any]]: ...

class FilterSet(BaseFilterSet, metaclass=FilterSetMetaclass): ...

def filterset_factory(
    model: type[Model], filterset: FilterSetMetaclass = ..., fields: Sequence[str] | dict[str, Sequence[str]] | str | None = None
) -> type[FilterSet]: ...

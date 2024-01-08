from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Type, Optional, Tuple
from django.http import HttpRequest
from django.core.paginator import Page, Paginator
from django_filters import FilterSet, CharFilter
from django.forms.widgets import NumberInput
from django.db.models import F, Q, CharField, QuerySet
from django.db.models.functions import Lower
from django.core.exceptions import FieldDoesNotExist
from .. import config
from ..forms import DashboardForm
from ..types import ValueData
from .base import Component, value_render_encoder
from typing import Any, Dict, List, Type, Optional, Tuple, Literal,Union
from django_filters import FilterSet

@dataclass
class FilterData:
    form: Dict[str, Any]
    dependents: List[str] = field(default_factory=list)

class TableFilterSet(FilterSet):
    global_search = CharFilter(
        method='filter_global_search',
        widget=NumberInput(attrs={'placeholder': 'Global Search'}),  # Use NumberInput or another widget
        label='',
    )

    def filter_global_search(self, queryset, name, value):
        model_fields = [f.name for f in queryset.model._meta.get_fields()]
        q_list = Q()

        for field in model_fields:
            q_list |= Q(**{f"{field}__icontains": value})

        return queryset.filter(q_list)

class TableFilterProcessor:
    @staticmethod
    def filter(qs: QuerySet, filters: Dict[str, Any]) -> QuerySet:
        filter_set = TableFilterSet(data=filters, queryset=qs)
        return filter_set.qs

    @staticmethod
    def sort(qs: QuerySet, fields: List[Any], filters: Dict[str, Any], force_lower: bool) -> QuerySet:
        orders = []

        for o in range(len(fields)):
            order_index = filters.get(f"order[{o}][column]")
            if order_index is not None:
                field = fields[int(order_index)]
                try:
                    django_field = qs.model._meta.get_field(field)
                except FieldDoesNotExist:
                    django_field = None

                if force_lower and django_field and isinstance(django_field, CharField):
                    field = Lower(field)
                else:
                    field = F(field)

                ordered_field = (
                    field.desc(nulls_last=True)
                    if filters.get(f"order[{o}][dir]") == "desc"
                    else field.asc(nulls_last=True)
                )
                orders.append(ordered_field)

        if orders:
            qs = qs.order_by(*orders)

        return qs

    @staticmethod
    def count(qs: QuerySet) -> int:
        return qs.count()

@dataclass
class Filter(Component):
    template_name: Optional[str] = None
    method: Optional[Literal["get", "post"]] = "get"
    filterset_class: Optional[Type[FilterSet]] = None  # Added filterset_class attribute

    def __init__(self, form: Type[DashboardForm], **kwargs):
        super().__init__(**kwargs)
        self.form = form
        self.filterset_class = None  # Initialize filterset_class to None

    def __post_init__(self):
        default_css_classes = config.Config().DASHBOARDS_COMPONENT_CLASSES["Filter"]

        if self.css_classes and isinstance(self.css_classes, str):
            self.css_classes = {"filter": self.css_classes}

        if isinstance(default_css_classes, dict) and isinstance(self.css_classes, dict):
            default_css_classes.update(self.css_classes)

        self.css_classes = default_css_classes

        if not self.filterset_class:
            raise ConfigurationError("Filter set class must be specified for Filter Component")

    def get_filterset(self) -> Type[FilterSet]:
        return self.filterset_class  # Use filterset_class attribute instead of TableFilterSet

    def get_value(self, request: HttpRequest = None, call_deferred=False, filters: Optional[Dict[str, Any]] = None) -> ValueData:
        filter_set = self.get_filterset()(data=filters, queryset=QuerySet())  # Pass an empty queryset
        queryset = filter_set.qs

        filter_data = FilterData(
            form=asdict(filter_set.form, dict_factory=value_render_encoder),
            dependents=self.dependents,
        )

        value = asdict(filter_data, dict_factory=value_render_encoder)

        return value

    @classmethod
    def filter_data(cls, data: Union[QuerySet, List], filters: Dict[str, Any]) -> Union[List, QuerySet]:
        return TableFilterProcessor.filter(data, filters)

    @classmethod
    def sort_data(cls, data: Union[QuerySet, List], filters: Dict[str, Any]) -> Union[List, QuerySet]:
        force_lower = cls._meta.force_lower
        fields = list(cls._meta.columns)
        return TableFilterProcessor.sort(data, fields, filters, force_lower)

    @classmethod
    def count_data(cls, data: Union[QuerySet, List]) -> int:
        return TableFilterProcessor.count(data)

    @staticmethod
    def apply_paginator(data: Union[QuerySet, List], start: int, length: int) -> Tuple[Page, int]:
        paginator = Paginator(data, length)
        page_number = (int(start) / int(length)) + 1
        return paginator.get_page(page_number), paginator.count

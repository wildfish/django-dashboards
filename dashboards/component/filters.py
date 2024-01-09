from typing import Any, Dict, List, Literal, Type

from django import forms
from django.http import HttpRequest

from django_filters import (
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    DateFilter,
    FilterSet,
    NumberFilter,
)

from .base import Component, ValueData


# Example non-ORM data for filtering
EXAMPLE_NON_ORM_DATA = {
    "char_field": "example",
    "date_field": "2022-01-01",
    "number_field": 42,
    "boolean_field": True,
    "choice_field": "option1",
}


class DashboardForm(FilterSet):
    char_filter = CharFilter(
        field_name="char_field", lookup_expr="icontains", label="Char Filter"
    )
    date_filter = DateFilter(
        field_name="date_field", lookup_expr="exact", label="Date Filter"
    )
    number_filter = NumberFilter(
        field_name="number_field", lookup_expr="exact", label="Number Filter"
    )
    boolean_filter = BooleanFilter(
        field_name="boolean_field", lookup_expr="exact", label="Boolean Filter"
    )
    choice_filter = ChoiceFilter(
        field_name="choice_field",
        choices=[("option1", "Option 1"), ("option2", "Option 2")],
        label="Choice Filter",
    )


class FilterComponent(Component):
    filter_fields: Type[FilterSet] = DashboardForm
    method: Literal["get", "post"] = "get"
    dependents: List[str] = []
    data_for_filters: Any = None

    def _get_non_orm_data(self) -> Any:
        return EXAMPLE_NON_ORM_DATA

    def _filter_non_orm_data_with_django_filters(
        self, data: Any, filter_set: FilterSet
    ) -> Any:
        print("Before filtering - data:", data)
        filtered_queryset = filter_set.filter(data)
        print("After filtering - filtered_queryset:", filtered_queryset)
        return filtered_queryset.qs

    def _process_form_data(self, cleaned_data: Dict[str, Any]) -> None:
        pass

    def get_value(
        self,
        request: HttpRequest = None,
        call_deferred=False,
        filters: dict[str, Any] | None = None,
    ) -> ValueData:
        if request.method == "POST":
            form = self.filter_fields(data=request.POST)
            if form.is_valid():
                self._process_form_data(form.cleaned_data)
            else:
                pass

        filter_data = request.GET if request else {}
        dynamic_filterset = self.filter_fields(data=filter_data)
        non_orm_data = self._get_non_orm_data()
        filtered_data = self._filter_non_orm_data_with_django_filters(
            non_orm_data, dynamic_filterset
        )

        return filtered_data

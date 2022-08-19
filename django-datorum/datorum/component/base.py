from dataclasses import dataclass
from typing import Callable, List, Optional, Type, Union

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from datorum.forms import DatorumFilterForm, DatorumModelFilterForm
from datorum.types import ValueData


@dataclass
class Component:
    template: str
    value: Optional[ValueData] = None
    width: Optional[int] = None
    defer: Optional[Callable] = None
    filter_form: Optional[Type[Union[DatorumFilterForm, DatorumModelFilterForm]]] = None
    dependents: Optional[List[str]] = None

    # attrs below can be set, but are inferred when fetching components from the dashboard class.
    key: Optional[str] = None
    group: Optional[str] = None
    group_width: Optional[str] = None
    render_type: Optional[str] = None

    # attrs below should not be changed
    dependent_components: Optional[List["Component"]] = None

    @property
    def is_deferred(self) -> bool:
        return True if self.defer else False

    def for_render(self, request: HttpRequest) -> ValueData:
        if self.is_deferred and self.defer:
            return self.defer(request)
        return self.value

    def has_form(self):
        return True if self.filter_form else False

    def __str__(self):
        context = {
            "component": self,
            "rendered_value": self.value,
            "htmx": self.is_deferred,
        }

        return mark_safe(render_to_string("datorum/components/component.html", context))

    def __repr__(self):
        return f"{self.key}={self.value}"

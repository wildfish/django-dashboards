from dataclasses import dataclass
from typing import Callable, Optional, Type, Union

from django.http import HttpRequest

from datorum.forms import DatorumFilterForm, DatorumModelFilterForm
from datorum.types import ValueData


@dataclass
class Component:
    template: str
    value: Optional[ValueData] = None
    width: Optional[int] = None
    defer: Optional[Callable] = None
    filter_form: Optional[Type[Union[DatorumFilterForm, DatorumModelFilterForm]]] = None

    # attrs below can be set, but are inferred when fetching components from the dashboard class.
    key: Optional[str] = None
    group: Optional[str] = None
    group_width: Optional[str] = None
    render_type: Optional[str] = None

    @property
    def is_deferred(self) -> bool:
        return True if self.defer else False

    def for_render(self, request: HttpRequest) -> ValueData:
        if self.is_deferred and self.defer:
            return self.defer(request)
        return self.value

    def has_form(self):
        return True if self.filter_form else False

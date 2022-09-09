from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Callable, Optional, Type, Union

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe

from datorum.forms import DatorumFilterForm, DatorumModelFilterForm
from datorum.types import ValueData


@dataclass
class CTA:
    href: str
    text: str


@dataclass
class Component:
    template: str
    value: Optional[ValueData] = None
    width: Optional[int] = 12
    defer: Optional[Callable[[HttpRequest], ValueData]] = None
    filter_form: Optional[Type[Union[DatorumFilterForm, DatorumModelFilterForm]]] = None
    dependents: Optional[list[str]] = None
    cta: Optional[CTA] = None
    css_classes: Optional[list[str]] = None

    # attrs below can be set, but are inferred when fetching components from the dashboard class.
    key: Optional[str] = None
    dashboard_class: Optional[str] = None
    tab: Optional[str] = None
    group: Optional[str] = None
    group_width: Optional[str] = None
    render_type: Optional[str] = None
    serializable: bool = True

    # attrs below should not be changed
    dependent_components: Optional[list["Component"]] = None

    @property
    def is_deferred(self) -> bool:
        return True if self.defer else False

    def for_render(self, request: HttpRequest, call_deferred=False) -> ValueData:
        if self.is_deferred and self.defer and call_deferred:
            value = self.defer(request)
        else:
            value = self.value

        if is_dataclass(value):
            value = asdict(value, dict_factory=dataclass_encoder)

        return value

    def has_form(self):
        return True if self.filter_form else False

    def get_absolute_url(self):
        return reverse(
            "datorum:dashboard_component", args=[self.dashboard_class, self.key]
        )

    def __str__(self):
        context = {
            "component": self,
            "rendered_value": self.value,
            "htmx": self.is_deferred,
        }

        return mark_safe(render_to_string("datorum/components/component.html", context))

    def __repr__(self):
        return f"{self.key}={self.value}"


def dataclass_encoder(data):
    def encode(o):
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        return o

    return dict((k, encode(v)) for k, v in data)

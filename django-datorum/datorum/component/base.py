import json
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Callable, List, Optional, Type, Union

from django.core.serializers.json import DjangoJSONEncoder
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
    width: Optional[int] = None
    defer: Optional[Callable[[HttpRequest], ValueData]] = None
    filter_form: Optional[Type[Union[DatorumFilterForm, DatorumModelFilterForm]]] = None
    dependents: Optional[List[str]] = None
    cta: Optional[CTA] = None

    # attrs below can be set, but are inferred when fetching components from the dashboard class.
    key: Optional[str] = None
    dashboard_class: Optional[str] = None
    group: Optional[str] = None
    group_width: Optional[str] = None
    render_type: Optional[str] = None
    render_json: bool = False

    # attrs below should not be changed
    dependent_components: Optional[List["Component"]] = None

    @property
    def is_deferred(self) -> bool:
        return True if self.defer else False

    def for_render(self, request: HttpRequest) -> ValueData:
        if self.is_deferred and self.defer:
            value = self.defer(request)
        else:
            value = self.value

        if self.render_json:
            value = json.dumps(value, cls=ComponentEncoder)

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


class ComponentEncoder(DjangoJSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)

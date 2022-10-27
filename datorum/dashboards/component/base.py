from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any, Callable, Dict, Optional

from django.db.models import QuerySet
from django.http import HttpRequest
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe

from ..types import ValueData


@dataclass
class Component:
    template_name: Optional[str] = None
    value: Optional[ValueData] = None
    defer: Optional[Callable[..., ValueData]] = None
    defer_url: Optional[Callable[..., str]] = None
    dependents: Optional[list[str]] = None

    # attrs below can be set, but are inferred when fetching components from the dashboard class.
    key: Optional[str] = None
    dashboard: Optional[ValueData] = None
    render_type: Optional[str] = None
    serializable: bool = True

    # replicated on LayoutBase TODO need to handle this better
    icon: Optional[str] = None  # html string .e.g <i class="fa-up"></i>
    css_classes: Optional[str] = None
    width: Optional[int] = 6
    poll_rate: Optional[int] = None  # In seconds, TODO make default a setting
    trigger_on: Optional[str] = None

    # attrs below should not be changed
    dependent_components: Optional[list["Component"]] = None

    @property
    def is_deferred(self) -> bool:
        return True if self.defer or self.defer_url else False

    @property
    def dashboard_class(self):
        return self.dashboard.class_name()

    def htmx_poll_rate(self):
        if self.poll_rate:
            return f"every {self.poll_rate}s"

    def htmx_trigger_on(self):
        if self.trigger_on:
            return f"{self.trigger_on} from:body, "

        return ""

    def get_value(
        self,
        request: HttpRequest = None,
        call_deferred=False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> ValueData:
        if self.is_deferred and self.defer and call_deferred:
            value = self.defer(
                request=request, dashboard=self.dashboard, filters=filters
            )
        else:
            if callable(self.value):
                value = self.value(
                    request=request, dashboard=self.dashboard, filters=filters
                )
            else:
                value = self.value

        if is_dataclass(value):
            value = asdict(value, dict_factory=value_render_encoder)

        return value

    def render(
        self, context: Context, htmx: Optional[bool] = None, call_deferred: bool = False
    ) -> str:
        request = context.get("request")
        if request:
            filters = request.GET.dict()
        else:
            filters = {}

        context = {
            "request": request,
            "component": self,
            "rendered_value": self.get_value(
                request=request, call_deferred=call_deferred, filters=filters
            ),
            "htmx": self.is_deferred if htmx is None else htmx,
        }

        return mark_safe(
            render_to_string("datorum/dashboards/components/component.html", context)
        )

    def get_absolute_url(self):
        """
        Get the absolute or fetch url to be called when a component is deferred.
        """
        kwargs = {
            "app_label": self.dashboard.Meta.app_label,
            "dashboard": self.dashboard_class,
            "component": self.key,
        }

        if hasattr(self.dashboard, "object"):
            kwargs[self.dashboard._meta.lookup_kwarg] = getattr(
                self.dashboard.object, self.dashboard._meta.lookup_field
            )

        if self.defer_url:
            url = self.defer_url(reverse_kwargs=kwargs)
        else:
            url = reverse("datorum.dashboards:dashboard_component", kwargs=kwargs)

        return url

    def __str__(self):
        return self.render(context=Context({}))

    def __repr__(self):
        return f"{self.key}={self.value}"


def value_render_encoder(data) -> dict:
    def encode(o):
        if is_dataclass(o):
            return asdict(o)
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, QuerySet):
            return list(o)
        return o

    return dict((k, encode(v)) for k, v in data)

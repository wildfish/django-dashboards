from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

from django.db.models import QuerySet
from django.http import HttpRequest
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from dashboards import config

from ..types import ValueData


if TYPE_CHECKING:
    from ..dashboard import Dashboard


@dataclass
class CTA:
    href: Optional[Union[str, Callable]] = None
    dashboard: Optional[str] = None

    def get_href(self, obj) -> Optional[str]:
        """
        Get CTA, first trying a dashboard by module path if not here as a str or callable.
        """
        if self.dashboard:
            dashboard_class = import_string(self.dashboard)
            if obj:
                lookup = getattr(obj, dashboard_class._meta.lookup_field)
                return reverse_lazy(
                    f"dashboards:{dashboard_class.get_slug()}_detail",
                    args=(lookup,),
                )
            else:
                return reverse_lazy(f"dashboards:{dashboard_class.get_slug()}")
        elif callable(self.href):
            return self.href(obj)

        return self.href


@dataclass
class Component:
    template_name: Optional[str] = None
    value: Optional[ValueData] = None
    defer: Optional[Callable[..., ValueData]] = None
    defer_url: Optional[Callable[..., str]] = None
    defer_loading_template_name: Optional[str] = "dashboards/components/loading.html"
    dependents: Optional[List[str]] = None
    cta: Optional[CTA] = None

    # attrs below can be set, but are inferred when fetching components from the dashboard class.
    key: Optional[str] = None
    verbose_name: Optional[str] = None
    dashboard: Optional["Dashboard"] = None
    object: Optional[Any] = None
    render_type: Optional[str] = None
    serializable: bool = True

    # replicated on LayoutBase TODO need to handle this better
    icon: Optional[str] = None  # html string .e.g <i class="fa-up"></i>
    css_classes: Optional[Union[str, Dict[str, str]]] = None
    grid_css_classes: Optional[str] = config.Config().DASHBOARDS_DEFAULT_GRID_CSS
    poll_rate: Optional[int] = None  # In seconds, TODO make default a setting
    trigger_on: Optional[str] = None

    # attrs below should not be changed
    dependent_components: Optional[list["Component"]] = None

    def __post_init__(self):
        default_css_classes = config.Config().DASHBOARDS_COMPONENT_CLASSES.get(
            self.__class__.__name__, None
        )

        # if nothing passed in set to default
        if self.css_classes is None:
            self.css_classes = default_css_classes

        # if passed in css is a dict, use defaults for missing classes
        elif isinstance(self.css_classes, dict):
            if isinstance(default_css_classes, dict):
                default_css_classes.update(self.css_classes)
            else:
                # if no default value just set it to be what is passed in
                default_css_classes = self.css_classes

            self.css_classes = default_css_classes

    @property
    def is_deferred(self) -> bool:
        return True if self.defer or self.defer_url else False

    @property
    def dashboard_class(self):
        if self.dashboard:
            return self.dashboard.class_name()
        return None

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
            serializable = getattr(self.defer, "serialize", None)
            if serializable:
                self.defer = serializable

            if callable(self.defer):
                value = self.defer(request=request, object=self.object, filters=filters)
            else:
                value = self.defer
        else:
            serializable = getattr(self.value, "serialize", None)
            if serializable:
                self.value = serializable

            if callable(self.value):
                value = self.value(request=request, object=self.object, filters=filters)
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
            filters = (
                request.GET.dict() if request.method == "GET" else request.POST.dict()
            )
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
            render_to_string("dashboards/components/component.html", context)
        )

    def get_absolute_url(self):
        """
        Get the absolute or fetch url to be called when a component is deferred.
        """
        if not self.dashboard:
            raise Exception("Dashboard is not set on Component")

        # <str:app_label>/<str:dashboard>/<str:component>/
        args = [
            self.dashboard._meta.app_label,
            self.dashboard_class,
            self.key,
        ]

        # if this is for an object then add lookup param to args
        if self.object:
            # <str:app_label>/<str:dashboard>/<str:lookup>/<str:component>/
            args.insert(2, getattr(self.object, self.dashboard._meta.lookup_field))

        if self.defer_url:
            url = self.defer_url(reverse_args=args)
        else:
            url = reverse("dashboards:dashboard_component", args=args)

        return url

    def template_id(self):
        return slugify(self.get_absolute_url())

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

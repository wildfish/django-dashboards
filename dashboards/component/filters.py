from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional, Type

from django.http import HttpRequest
from django.urls import reverse
from django.db import models
from django_filters import FilterSet, CharFilter

from .. import config
from ..forms import DashboardForm
from ..types import ValueData
from .base import Component, value_render_encoder


@dataclass
class FilterData:
    action: str
    form: Dict[str, Any]
    method: str
    dependents: Optional[List[str]] = None


@dataclass
class Filter(Component):
    template_name: Optional[str] = None
    model: Optional[Type[models.Model]] = None
    method: Literal["get", "post"] = "get"
    submit_url: Optional[str] = None
    filter_fields: Optional[Dict[str, Any]] = None
    form: Optional[Type[DashboardForm]] = None  # Add this line

    def __post_init__(self):
        default_css_classes = config.Config().DASHBOARDS_COMPONENT_CLASSES["Filter"]

        if self.css_classes and isinstance(self.css_classes, str):
            self.css_classes = {"filter": self.css_classes}

        if isinstance(default_css_classes, dict) and isinstance(self.css_classes, dict):
            default_css_classes.update(self.css_classes)

        self.css_classes = default_css_classes

    def get_submit_url(self):
        if not self.dashboard:
            raise Exception("Dashboard is not set on Filter Component")

        if self.submit_url:
            return self.submit_url

        args = [
            self.dashboard._meta.app_label,
            self.dashboard_class,
            self.key,
        ]

        if self.object:
            args.insert(2, getattr(self.object, self.dashboard._meta.lookup_field))

        return reverse("dashboards:filter_component", args=args)

    def get_filter_form(self) -> Type[FilterSet]:
        class DynamicFilterSet(FilterSet):
            class Meta:
                model = self.model

        for field_name, field_config in self.filter_fields.items():
            DynamicFilterSet.base_filters[field_name] = CharFilter(**field_config)

        return DynamicFilterSet
def get_value(
    self,
    request: HttpRequest = None,
    call_deferred=False,
    filters: Optional[Dict[str, Any]] = None,
) -> ValueData:
    if not self.model or not self.filter_fields or not self.form:  # Add form check
        raise NotImplementedError(
            "Model, filter_fields, and form must be specified for Filter Component"
        )

    filter_form = self.get_filter_form()

    # Apply filter data to the form
    filter_instance = filter_form(request.GET, queryset=self.model.objects.all())
    queryset = filter_instance.qs

    filter_data = FilterData(
        method=self.method,
        form=asdict(filter_instance.form, dict_factory=value_render_encoder),
        action=self.get_submit_url(),
        dependents=self.dependents,
    )

    value = asdict(filter_data, dict_factory=value_render_encoder)

    return value
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Type

from django.http import HttpRequest
from django.urls import reverse
from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Page, Paginator
from django.db.models import CharField, F, Q, QuerySet
from django.db.models.functions import Lower
from django_filters import FilterSet, CharFilter

from .. import config
from ..forms import DashboardForm
from ..types import ValueData
from .base import Component, value_render_encoder

class ConfigurationError(Exception):
    pass

class FilterData:
    def __init__(self, action, form, method, dependents=None):
        self.action = action
        self.form = form
        self.method = method
        self.dependents = dependents

class DynamicFilterSet(FilterSet):
    pass  #  we can  define any specific filters

class SampleFilterSet(FilterSet):
    # This is a placeholder for the FilterSet. 
    sample_filter = CharFilter(field_name='sample_field', lookup_expr='icontains')

class Filter(Component):
    filter_fields: Type[FilterSet] = SampleFilterSet
    form: Type[DashboardForm] = DashboardForm
    method: str = "get"
    submit_url: str = None
    dependents: List[str] = None

    def __init__(self, filter_fields=None, form=None, method=None, submit_url=None, dependents=None, **kwargs):
        super().__init__(**kwargs)
        self.filter_fields = filter_fields or self.filter_fields
        self.form = form or self.form
        self.method = method or self.method
        self.submit_url = submit_url or self.submit_url
        self.dependents = dependents or self.dependents

        self._set_default_css_classes()

    def _set_default_css_classes(self):
        default_css_classes = config.Config().DASHBOARDS_COMPONENT_CLASSES["Filter"]
        if isinstance(self.css_classes, str):
            self.css_classes = {"filter": self.css_classes}

        if isinstance(default_css_classes, dict) and isinstance(self.css_classes, dict):
            default_css_classes.update(self.css_classes)

        self.css_classes = default_css_classes

    def get_submit_url(self):
        if not self.dashboard:
            raise Exception("Dashboard is not set on Filter Component")

        return self.submit_url or self._default_submit_url()

    def _default_submit_url(self):
        args = [self.dashboard._meta.app_label, self.dashboard_class, self.key]
        if self.object:
            args.insert(2, getattr(self.object, self.dashboard._meta.lookup_field))
        return reverse("dashboards:filter_component", args=args)

    def get_filter_form(self, data: Dict[str, Any]) -> DashboardForm:
        form = self.form(data)
        if not form.is_valid():
            raise ValueError("Invalid data provided to the form.")
        return form

    def get_filterset(self) -> Type[FilterSet]:
        if not self.filter_fields:
            raise ConfigurationError("FilterSet class must be specified for Filter Component")
        return self.filter_fields

    def get_value(
        self,
        request: HttpRequest = None,
        call_deferred=False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> ValueData:
        if not self.form or not self.filter_fields:
            raise ConfigurationError("Form and filter_fields must be specified for Filter Component")

        filter_form_data = {}   # to populate the  data from the form
        filter_form = self.get_filter_form(filter_form_data)
        filter_set = self.get_filterset()(data=filter_form_data, queryset=QuerySet())  # Initialize with an empty queryset

        filter_data = FilterData(
            method=self.method,
            form=asdict(filter_form, dict_factory=value_render_encoder),
            action=self.get_submit_url(),
            dependents=self.dependents,
        )

        return asdict(filter_data, dict_factory=value_render_encoder)

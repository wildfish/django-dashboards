from dataclasses import dataclass
from typing import List, Optional

from django.http import HttpRequest
from django.urls import reverse

from datorum.forms import DatorumForm
from datorum.utils import get_dashboard

from .base import Component


@dataclass
class Form(Component):
    form: DatorumForm = None
    dependants: Optional[List[str]] = None
    template: str = "datorum/components/form/form.html"

    def get_absolute_url(self):
        return reverse("datorum:form_component", args=[self.dashboard_class, self.key])

    def get_dependant_components(self, dashboard):
        components = [
            component
            for component in dashboard.get_components()
            if component.key in self.dependants
        ]

        return components

    def get_form(self, dashboard, request: HttpRequest) -> DatorumForm:
        form = self.form(dashboard=dashboard, data=request.GET or None)
        return form

    def for_render(self, request: HttpRequest) -> DatorumForm:
        dashboard = get_dashboard(self.dashboard_class, request=request)
        form = self.get_form(dashboard=dashboard, request=request)

        return form

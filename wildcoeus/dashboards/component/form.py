from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Type

from django.http import HttpRequest

from ..forms import DashboardForm
from ..types import ValueData
from .base import Component, value_render_encoder


@dataclass
class FormData:
    action: list[str]
    form: list[dict[str, Any]]
    method: str
    dependents: Optional[list[str]] = None


@dataclass
class Form(Component):
    template_name: str = "wildcoeus/dashboards/components/form/form.html"
    form: Optional[Type[DashboardForm]] = None
    method: str = "get"

    def get_form(self, request: HttpRequest = None) -> DashboardForm:
        if not self.form:
            raise NotImplementedError(
                f"No form configured for Form Component {self.__class__.__name__}"
            )

        data = None

        if request:
            if request.method == "POST":
                data = request.POST
            elif request.GET:
                data = request.GET

        form = self.form(
            app_label=self.dashboard.Meta.app_label if self.dashboard else "",
            dashboard_class=self.dashboard_class,
            key=self.key,
            data=data,
        )
        return form

    def get_value(
        self,
        request: HttpRequest = None,
        call_deferred=False,
        filters: Optional[Dict[str, Any]] = None,
    ) -> ValueData:
        form = self.get_form(request=request)
        form_data = FormData(
            method=self.method,
            form=form,
            action=form.get_submit_url(),
            dependents=self.dependents,
        )
        value = asdict(form_data, dict_factory=value_render_encoder)

        return value

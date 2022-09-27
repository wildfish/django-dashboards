from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Type

from django.http import HttpRequest

from datorum.forms import DatorumForm
from datorum.types import ValueData

from .base import Component, value_render_encoder


@dataclass
class FormData:
    action: list[str]
    form: list[dict[str, Any]]
    method: str
    dependents: Optional[list[str]] = None


@dataclass
class Form(Component):
    template: str = "datorum/components/form/form.html"
    form: Optional[Type[DatorumForm]] = None
    method: str = "get"

    def get_form(self, request: HttpRequest = None) -> DatorumForm:
        if not self.form:
            raise NotImplementedError(
                f"No form configured for Form Component {self.__class__.__name__}"
            )

        if request and request.method == "POST":
            data = request.POST
        elif request:
            data = request.GET or None
        else:
            data = None

        form = self.form(dashboard_class=self.dashboard_class, key=self.key, data=data)
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

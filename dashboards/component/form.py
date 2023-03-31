from dataclasses import asdict, dataclass
from typing import Any, Dict, Literal, Optional, Type

from django.http import HttpRequest
from django.urls import reverse

from .. import config
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
    template_name: str = "dashboards/components/form/form.html"
    form: Optional[Type[DashboardForm]] = None
    method: Literal["get", "post"] = "get"
    trigger: Literal["change", "submit"] = "change"
    submit_url: Optional[str] = None

    def __post_init__(self):
        default_css_classes = config.Config().DASHBOARDS_COMPONENT_CLASSES["Form"]
        # make sure css_classes is a dict as this is what form template requires
        if self.css_classes and isinstance(self.css_classes, str):
            # if sting assume this is form class
            self.css_classes = {"form": self.css_classes}

        # update defaults with any css classes which have been passed in
        if isinstance(default_css_classes, dict) and isinstance(self.css_classes, dict):
            default_css_classes.update(self.css_classes)

        self.css_classes = default_css_classes

    def get_submit_url(self):
        """url the form sends data to on Submit"""
        if not self.dashboard:
            raise Exception("Dashboard is not set on Form Component")

        # if it has been passed in use that, otherwise generate based on component
        if self.submit_url:
            return self.submit_url

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

        return reverse("dashboards:form_component", args=args)

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

        form = self.form(data=data)
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
            action=self.get_submit_url(),
            dependents=self.dependents,
        )
        value = asdict(form_data, dict_factory=value_render_encoder)

        return value

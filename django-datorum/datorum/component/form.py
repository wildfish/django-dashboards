from dataclasses import dataclass
from typing import Optional, Type

from django.http import HttpRequest

from datorum.forms import DatorumForm

from .base import Component


@dataclass
class Form(Component):
    form: Optional[Type[DatorumForm]] = None
    template: str = "datorum/components/form/form.html"
    method: str = "get"
    serializable: bool = False

    def get_absolute_url(self):
        return self.get_form().get_submit_url()

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
        self, request: HttpRequest = None, call_deferred: bool = False
    ) -> DatorumForm:
        form = self.get_form(request=request)

        return form

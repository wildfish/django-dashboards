from dataclasses import dataclass

from django.http import HttpRequest

from datorum.forms import DatorumForm

from .base import Component


@dataclass
class Form(Component):
    form: DatorumForm = None
    template: str = "datorum/components/form/form.html"
    method: str = "get"

    def get_absolute_url(self):
        return self.get_form().get_submit_url()

    def get_form(self, request: HttpRequest = None) -> DatorumForm:
        if request and request.method == "POST":
            data = request.POST
        elif request:
            data = request.GET or None
        else:
            data = None

        form = self.form(dashboard_class=self.dashboard_class, key=self.key, data=data)
        return form

    def for_render(self, request: HttpRequest, call_deferred: bool = False) -> DatorumForm:
        form = self.get_form(request=request)

        return form

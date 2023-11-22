import asyncio

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView

import httpx
from demo.kitchensink.dashboards import DemoDashboard, DynamicDashboard

from dashboards.views import ComponentView


class StandardView(TemplateView):
    template_name = "demo/standard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = DemoDashboard()

        return context


class TabbedView(TemplateView):
    template_name = "demo/tabbed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tabs = [DemoDashboard(), DynamicDashboard(request=self.request)]
        context["tabs"] = tabs
        context["initial_tab"] = tabs[0]
        # you'd need to combine the media for each tab, for ease just use the first dashboards media here
        context["dashboard"] = tabs[0]
        return context


class CustomComponentView(ComponentView):
    def get(self, request: HttpRequest, *args, **kwargs):
        return HttpResponse("Simple response")


class NoTemplateComponentDeferView(ComponentView):
    def get(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard(request=request)
        component = self.get_partial_component(dashboard=dashboard)

        # Call the value direct to response, which is essentially what
        # ComponentView does minus applying the template.
        return HttpResponse(component.get_value(request=request, call_deferred=True))


class SyncComponentView(ComponentView):
    def get(self, request: HttpRequest, *args, **kwargs):
        status = ["200", "302", "400", "404", "500"]
        responses = [httpx.get(f"https://postman-echo.com/status/{s}") for s in status]

        return HttpResponse(
            "Fetched an API Sync<br/>"
            + "<hr/>".join([str(r.status_code) for r in responses])
        )


class AsyncComponentView(ComponentView):
    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Needed prior to 4.1 for CBV
        """
        view = super().as_view(**initkwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine
        return view

    async def get(self, request: HttpRequest, *args, **kwargs):
        async with httpx.AsyncClient() as client:
            status = ["200", "302", "400", "404", "500"]
            responses = await asyncio.gather(
                *[client.get(f"https://postman-echo.com/status/{s}") for s in status]
            )

        return HttpResponse(
            "Fetched an API Async<br/>"
            + "<hr/>".join([str(r.status_code) for r in responses])
        )

    async def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

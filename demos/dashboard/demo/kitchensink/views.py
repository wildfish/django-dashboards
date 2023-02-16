import asyncio

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView

import httpx
from demo.kitchensink.dashboards import DemoDashboard

from wildcoeus.dashboards.views import ComponentView


class NormalView(TemplateView):
    template_name = "wildcoeus/dashboards/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = DemoDashboard()

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
        responses = [httpx.get(f"https://httpbin.org/status/{s}") for s in status]

        return HttpResponse(
            "Sync<br/>" + "<hr/>".join([str(r.status_code) for r in responses])
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
                *[client.get(f"https://httpbin.org/status/{s}") for s in status]
            )

        return HttpResponse(
            "Async<br/>" + "<hr/>".join([str(r.status_code) for r in responses])
        )

    async def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

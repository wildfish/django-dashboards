=====
Aysnc
=====

While there is no direct support for Async views currently, it is possible to create a view which would support
async components.

.. image:: _images/async_component.gif
   :alt: Demo Dashboard

You first need a to create your own Async compatible component view, for example from our demo (TODO LINK)
we have:

::

    import asyncio

    from django.http import HttpRequest, HttpResponse
    from django.utils.decorators import classonlymethod

    import httpx

    from dashboards.views import ComponentView


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


In this case, the view simply returns an async fetch of some httpbin responses.

In your urls.py you can now add the async component, the path can be anything as can the reverse name, but the
url must append ``COMPONENT_PATTERN``.

::

    # urls.py
    from django.urls import path

    from .views import AsyncComponentView

    from dashboards.urls import COMPONENT_PATTERN


    urlpatterns = [
        ...
        path(
            "asynccomponent/" + COMPONENT_PATTERN,
            AsyncComponentView.as_view(),
            name="async-component",
        ),
        ...

You can now point a component to the alternate async component view by setting an alternate ``defer_url`` on
any component:

::

    # views.py
    from django.urls import reverse

    from dashboards.component import Text
    from dashboards.dashboard import Dashboard


    class AsyncComponentDashboard(Dashboard):
        async_httpbin = Text(
            defer_url=lambda reverse_args: reverse(
                "async-component", args=reverse_args
            ),
        )

You can also mix and match with standard component defers in once dashboard.
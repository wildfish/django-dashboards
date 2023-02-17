===============
Views & Routing
===============

By default any ``Dashboard`` registered will have a generic view and url routing created for it as
long as you have included ``include('wildcoeus.dashboards.urls')`` in your ``urls.py``
and ``WILDCOEUS_INCLUDE_DASHBOARD_VIEWS = True`` (defualt) in your ``settings.py``

For example if you added the following dashboard to the app ``test``:

::

    class DemoDashboard(Dashboard):
        example = Text(value="Rendered on load")

        class Meta:
            name = "Demo"


and included in your route urls:

::

    # urls.py

    path('dashboards/', include('wildcoeus.dashboards.urls')),


The dashboard will then be available at ``/dashboard/test/demodashboard/``, or using ``reverse``:

::

    # view.py

    reverse("wildcoeus.dashboards:test_demodashboard")
    # reverse("<namespace>:<app_label>_<slug_dashboard_class_name>")

You can also provide a namespace as per Django's urls:

::

    # urls.py

    path("dashboards/", include("wildcoeus.dashboards.urls", "customnamespace"))

    # view.py

    reverse("customnamespace:test_demodashboard")


Adding your own routes
----------------------

If you decide not to use the dynamic Dashboard routing & views, you can add your own.
Either by creating a route to the built in `DashboardView`:

::

    # urls.py

    path(
        "",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboard),
        name="demo-dashboard",
    ),

or including your Dashboard in a normal view:

::

    # urls.py
    from django.urls import path

    from .views import (
        NormalView,
    )

    path(
        "normal/",
        NormalView.as_view(),
        name="normal",
    ),

    # views.py

    from django.views.generic import TemplateView
    from . import DemoDashboard

    class NormalView(TemplateView):
        template_name = "..."

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["dashboard"] = DemoDashboard()
            return context

Please note there are caveats to adding your own routes:

* We'd recommend you also disable ``WILDCOEUS_INCLUDE_DASHBOARD_VIEWS`` to avoid duplicate views. Noting that you will still be leveraging the component and form fetch views included in the package.
* If you decide not to use ``DashboardView`` any permissions_classes will not be applied.


Custom component views
----------------------

Wildcoeus comes bundled with URLs to handle deferred components, however, if need arises you can also add your own. For example:


::

    # urls.py
    from django.urls import path

    from .views import (
        NoTemplateComponentDeferView,
        CustomComponentView,
    )

    from wildcoeus.dashboards.urls import COMPONENT_PATTERN
    from wildcoeus.dashboards.views import DashboardView

    path(
        "customcomponent/" + COMPONENT_PATTERN,
        CustomComponentView.as_view(),
        name="custom-component",
    ),
    path(
        "notemplatecomponentdefer/" + COMPONENT_PATTERN,
        NoTemplateComponentDeferView.as_view(),
        name="custom-component-defer",
    ),


    # views.py

    from django.http import HttpRequest, HttpResponse

    from wildcoeus.dashboards.views import ComponentView


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


    # dashboards.py

    class CustomComponentDashboard(Dashboard):
        custom_response = Text(
            defer_url=lambda reverse_args: reverse(
                "custom-component", args=reverse_args
            ),
        )

        no_template_response_defer = Text(
            defer=lambda **kwargs: "Simple Response Via Defer",
            defer_url=lambda reverse_args: reverse(
                "custom-component-defer", args=reverse_args
            ),
        )

A use case for this is :doc:`Async components <async>` .
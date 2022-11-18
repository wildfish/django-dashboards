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

    path(
        "normal/",
        NormalView.as_view(),
        name="normal",
    ),

    # views.py

    class NormalView(TemplateView):
        template_name = "..."

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["dashboard"] = DemoDashboard()
            return context

Please note there are caveats to adding your own routes:

* We'd recommend you also disable ``WILDCOEUS_INCLUDE_DASHBOARD_VIEWS`` to avoid duplicate views. Noting that you will still be leveraging the component and form fetch views included in the package.
* If you decide not to use ``DashboardView`` any permissions_classes will not be applied.

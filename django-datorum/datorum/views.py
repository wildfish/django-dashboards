from typing import Optional

from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.views.generic import TemplateView

from datorum.component import Component
from datorum.dashboard import Dashboard
from datorum.registry import registry


class DashboardView(TemplateView):
    """
    Dashboards base.

    By default, datorum/as_grid.html will be used, which uses a standard 12 grid layout.

    Returns either a
        - standard template: all components
        - partial template (for HTMX): single component (via param key)
        - json for (Ajax): single component (via param key)
    """

    dashboard_class: Optional[Dashboard] = None
    template_name: str = "datorum/dashboard.html"

    def get(self, request, *args, **kwargs):
        self.dashboard = self.get_dashboard()

        context = self.get_context_data(**{"dashboard": self.dashboard})

        # Render to template
        return self.render_to_response(context)

    def get_dashboard_kwargs(self):
        kwargs = {}
        return kwargs

    def get_dashboard(self):
        return self.dashboard_class(**self.get_dashboard_kwargs())

    def dispatch(self, request, *args, **kwargs):
        has_permissions = self.get_dashboard().has_permissions(request=self.request)
        if not has_permissions:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class ComponentView(TemplateView):
    template_name: str = "datorum/components/partial.html"

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def get(self, request, *args, **kwargs):
        self.dashboard = self.get_dashboard()
        self.component = self.get_partial_component()

        if self.is_ajax():
            # Return json, calling the deferred value.
            return JsonResponse(self.component.defer(self.request), safe=False)
        else:
            context = self.get_context_data(
                **{"component": self.component, "dashboard": self.dashboard}
            )

            return self.render_to_response(context)

    def get_dashboard(self):
        try:
            dashboards = registry.get_all_dashboards()
            dashboard = dashboards[self.kwargs["dashboard"]]
        except KeyError:
            raise Http404(f"Dashboard {self.kwargs['dashboard']} does not exist")

        if not dashboard.has_permissions(request=self.request):
            raise PermissionDenied()

        return dashboard

    def get_partial_component(self):
        if hasattr(self, "dashboard"):
            dashboard = self.dashboard
        else:
            dashboard = self.get_dashboard()

        for component in dashboard.get_components(with_layout=False):
            if component.key == self.kwargs["component"]:
                return component

        raise Http404(
            f"Component {self.kwargs['component']} does not exist in dashboard {self.kwargs['dashboard']}"
        )

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
    partial_template_name: str = "datorum/components/partial.html"
    partial_component: Optional[Component] = None

    def get(self, request, *args, **kwargs):
        self.dashboard = self.get_dashboard()
        self.partial_component = self.get_partial_component()

        if self.is_ajax() and self.partial_component:
            # Return json, calling the deferred value.
            return JsonResponse(self.partial_component.defer(self.request), safe=False)
        else:
            context = self.get_context_data(
                **{"component": self.partial_component, "dashboard": self.dashboard}
            )

            # Render to template, either partial of full.
            return self.render_to_response(context)

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def get_dashboard_kwargs(self):
        kwargs = {}
        return kwargs

    def get_dashboard(self):
        return self.dashboard_class(**self.get_dashboard_kwargs())

    def get_partial_component(self):
        """
        Partial component decides if we are only fetching one component & which is the case if we are using
        an HTMX or Ajax call.
        """
        key = self.request.GET.get("key")
        if self.request.htmx and key or self.is_ajax():
            dashboard = (
                self.dashboard if hasattr(self, "dashboard") else self.get_dashboard()
            )
            for component in dashboard.get_components(with_layout=False):
                if component.key == key:
                    return component
        return

    def dispatch(self, request, *args, **kwargs):
        has_permissions = self.get_dashboard().has_permissions(request=self.request)
        if not has_permissions:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        """
        Render partial when a htmx is in use.
        """
        names = super().get_template_names()
        if self.partial_component:
            return [self.partial_template_name]
        return names


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
        for component in self.dashboard.get_components():
            if component.key == self.kwargs["component"]:
                return component

        raise Http404(
            f"Component {self.kwargs['component']} does not exist in dashboard {self.kwargs['dashboard']}"
        )

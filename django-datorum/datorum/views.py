from typing import Optional

from django.http import JsonResponse
from django.views.generic import TemplateView

from datorum.component import Component
from datorum.dashboard import Dashboard


class DashboardView(TemplateView):
    """
    Dashboards base.

    By default, datorum/as_grid.html will be used, which uses a standard 12 grid layout.

    Returns either a
        - standard template: all components
        - partial template (for HTMX): single component (via param key)
        - json for (Ajax): single component (via param key)
    """

    dashboard: Optional[Dashboard] = None
    template_name: str = "datorum/as_grid.html"
    partial_template_name: str = "datorum/components/partial.html"
    partial_component: Optional[Component] = None

    def get(self, request, *args, **kwargs):
        dashboard = None
        self.partial_component = self.get_partial_component()

        if not self.partial_component:
            dashboard = self.dashboard(request=self.request)

        context = self.get_context_data(
            **{"component": self.partial_component, "dashboard": dashboard}
        )

        if self.is_ajax() and self.partial_component:
            # Return json, calling the deferred value.
            return JsonResponse(self.partial_component.defer(self.request), safe=False)
        else:
            # Render to template, either partial of full.
            print(dir(self.render_to_response(context)))
            return self.render_to_response(context)

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def get_partial_component(self):
        """
        Partial component decides if we are only fetching one component & which is the case if we are using
        an HTMX or Ajax call.
        """
        key = self.request.GET.get("key")
        if self.request.htmx and key or self.is_ajax():
            for component in self.dashboard(request=self.request).get_components(
                with_layout=False
            ):
                if component.key == key:
                    return component
        return

    def get_template_names(self):
        """
        Render partial when a htmx is in use.
        """
        names = super().get_template_names()
        if self.partial_component:
            return [self.partial_template_name]
        return names

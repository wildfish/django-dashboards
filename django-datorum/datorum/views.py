import json
from typing import Optional

from datorum.dashboard import Dashboard
from datorum.utils import get_dashboard
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """
    Dashboard view, allows a single Dashboard to be auto rendered.
    """

    dashboard_class: Optional[Dashboard] = None
    template_name: str = "datorum/dashboard.html"

    def get(self, request, *args, **kwargs):
        self.dashboard = self.get_dashboard()

        context = self.get_context_data(**{"dashboard": self.dashboard})

        return self.render_to_response(context)

    def get_dashboard_kwargs(self):
        kwargs = {}
        return kwargs

    def get_dashboard(self):
        return self.dashboard_class(**self.get_dashboard_kwargs())

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        has_permissions = self.get_dashboard().has_permissions(request=self.request)
        if not has_permissions:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class ComponentView(TemplateView):
    """
    Component view, partial rendering of a single component to support HTMX calls.
    """

    template_name: str = "datorum/components/partial.html"

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def get(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard()
        component = self.get_partial_component(dashboard)

        if self.is_ajax() and component:
            # Return json, calling the deferred value.
            return HttpResponse(
                json.dumps(component.for_render(self.request, call_deferred=True)),
                content_type="application/json",
            )
        else:
            context = self.get_context_data(
                **{"component": component, "dashboard": dashboard}
            )

            return self.render_to_response(context)

    def get_dashboard(self):
        return get_dashboard(self.kwargs["dashboard"], request=self.request)

    def get_partial_component(self, dashboard):
        for component in dashboard.get_components():
            if component.key == self.kwargs["component"]:
                return component

        raise Http404(
            f"Component {self.kwargs['component']} does not exist in dashboard {self.kwargs['dashboard']}"
        )


class FormComponentView(ComponentView):
    """
    Form Component view, partial rendering of dependant components to support HTMX calls.
    """

    template_name: str = "datorum/components/partial.html"

    # todo: temp fix as currently failing as not passed through form. remove once csrf_token passed in post
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        dashboard = self.get_dashboard()
        component = self.get_partial_component(dashboard)

        return component.get_absolute_url()

    def get(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard()
        component = self.get_partial_component(dashboard)
        dependant_components = component.dependent_components

        if self.is_ajax():
            response = []
            for c in dependant_components:
                # Return json, calling deferred value on dependant components.
                response.append(c.for_render(self.request))
            return HttpResponse(response, content_type="application/json")
        else:
            context = self.get_context_data(
                **{
                    "dependants": dependant_components,
                    "dashboard": dashboard,
                    "component": component,
                }
            )

            return self.render_to_response(context)

    def post(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard()
        component = self.get_partial_component(dashboard)
        form = component.get_form(request=request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())

        return self.get(request, *args, **kwargs)

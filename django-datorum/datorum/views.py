import json
from typing import Optional

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from datorum.dashboard import Dashboard
from datorum.exceptions import DashboardNotFoundError
from datorum.utils import get_dashboard_class


class DashboardObjectMixin:
    dashboard_class: Optional[Dashboard] = None

    def get_dashboard_kwargs(self):
        kwargs = {}
        if self.dashboard_class:
            kwargs[self.dashboard_class._meta.lookup_kwarg] = self.kwargs.get(
                self.dashboard_class._meta.lookup_kwarg
            )

        return kwargs

    def get_dashboard(self, request):
        has_permissions = self.dashboard_class.has_permissions(request=request)
        if not has_permissions:
            raise PermissionDenied()

        return self.dashboard_class(**self.get_dashboard_kwargs())


class DashboardView(DashboardObjectMixin, TemplateView):
    """
    Dashboard view, allows a single Dashboard to be auto rendered.
    """

    template_name: str = "datorum/dashboard.html"

    def get(self, request, *args, **kwargs):
        self.dashboard = self.get_dashboard(request)
        context = self.get_context_data(**{"dashboard": self.dashboard})
        return self.render_to_response(context)


class ComponentView(DashboardObjectMixin, TemplateView):
    """
    Component view, partial rendering of a single component to support HTMX calls.
    """

    template_name: str = "datorum/components/partial.html"

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def get_dashboard(self, request):
        try:
            self.dashboard_class = get_dashboard_class(
                self.kwargs["app_label"], self.kwargs["dashboard"]
            )
        except DashboardNotFoundError as e:
            raise Http404(str(e))

        return super().get_dashboard(request)

    def get(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard(request)
        component = self.get_partial_component(dashboard)

        if self.is_ajax() and component:
            filters = request.GET.dict()
            # Return json, calling the deferred value.
            return HttpResponse(
                json.dumps(
                    component.get_value(
                        request=self.request, call_deferred=True, filters=filters
                    )
                ),
                content_type="application/json",
            )
        else:
            context = self.get_context_data(
                **{"component": component, "dashboard": dashboard}
            )

            return self.render_to_response(context)

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

    def get(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard(request)
        component = self.get_partial_component(dashboard)
        dependant_components = component.dependent_components

        if self.is_ajax():
            response = []
            filters = request.GET.dict()
            for c in dependant_components:
                # Return json, calling deferred value on dependant components.
                response.append(c.get_value(request=self.request, filters=filters))
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
        dashboard = self.get_dashboard(request)
        component = self.get_partial_component(dashboard)
        form = component.get_form(request=request)
        if form.is_valid():
            form.save()
            if self.is_ajax():
                return HttpResponse({"success": True}, content_type="application/json")

            return HttpResponseRedirect(component.get_absolute_url())

        return self.get(request, *args, **kwargs)

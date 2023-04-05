import json
from typing import TYPE_CHECKING, Callable, Dict, Optional, Protocol, Type

from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpRequest, HttpResponse
from django.views import View
from django.views.generic import TemplateView

from typing_extensions import TypeAlias

from dashboards.dashboard import Dashboard
from dashboards.exceptions import DashboardNotFoundError
from dashboards.utils import get_dashboard_class


class HasValueProtocol(Protocol):
    dashboard_class: Type[Dashboard]
    kwargs: Dict
    get_dashboard_context: Callable


if TYPE_CHECKING:
    mixin_class: TypeAlias = View
else:
    mixin_class: TypeAlias = object


class DashboardObjectMixin(mixin_class):
    dashboard_class: Optional[Dashboard] = None

    def is_ajax(self):
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def is_htmx(self):
        return self.request.headers.get("hx-request") == "true"

    def dispatch(self: TemplateView, request, *args, **kwargs):
        if not self.dashboard_class:
            try:
                self.dashboard_class = get_dashboard_class(
                    self.kwargs["app_label"], self.kwargs["dashboard"]
                )
            except DashboardNotFoundError as e:
                raise Http404(str(e))

        has_perm = self.dashboard_class.has_permissions(request=request, handle=True)
        # if has perm is not a bool, it's the result of a permission.handle_no_permission
        if not isinstance(has_perm, bool):
            return has_perm
        # else it is a bool, but False, the permission was not handled to assume PermissionDenied
        elif not has_perm:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)

    def get_dashboard_context(self, **context):
        """kwargs passed to dashboard class"""
        if not self.dashboard_class:
            raise Exception("Dashboard class not set on view")

        # extract lookup value from kwargs and assign to key set on meta
        if (
            self.dashboard_class._meta.lookup_kwarg
            and self.dashboard_class._meta.lookup_kwarg
        ):
            context[self.dashboard_class._meta.lookup_kwarg] = self.kwargs.get(
                self.dashboard_class._meta.lookup_kwarg
            )

        return context

    def get_dashboard(self: HasValueProtocol, **kwargs) -> Dashboard:
        context = self.get_dashboard_context(**kwargs)
        return self.dashboard_class(**context)


class DashboardView(DashboardObjectMixin, TemplateView):
    """
    Dashboard view, allows a single Dashboard to be auto rendered.
    """

    template_name: str = "dashboards/dashboard.html"
    partial_template_name: str = "dashboards/dashboard_partial.html"

    def get(self, request, *args, **kwargs):
        dashboard = self.get_dashboard(request=request)
        context = self.get_context_data(**{"dashboard": dashboard})
        return self.render_to_response(context)

    def get_template_names(self):
        if self.is_htmx():  # a certain check
            return [self.partial_template_name]
        else:
            return [self.template_name]


class ComponentView(DashboardObjectMixin, TemplateView):
    """
    Component view, partial rendering of a single component to support HTMX calls.
    """

    template_name: str = "dashboards/components/partial.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard(request=request)
        component = self.get_partial_component(dashboard)

        if self.is_ajax() and component:
            filters = (
                request.GET.dict() if request.method == "GET" else request.POST.dict()
            )

            # Return json, calling the deferred value.
            return HttpResponse(
                json.dumps(
                    component.get_value(
                        request=self.request, call_deferred=True, filters=filters
                    ),
                    cls=DjangoJSONEncoder,
                ),
                content_type="application/json",
            )
        else:
            context = self.get_context_data(
                **{"component": component, "dashboard": dashboard}
            )

            return self.render_to_response(context)

    def post(self, *args, **kwargs):
        """
        Allow post, for Ajax post requests i.e post based filtered
        """
        return self.get(*args, **kwargs)

    def get_partial_component(self, dashboard):
        if not self.dashboard_class:
            raise Exception("Dashboard class not set on view")

        for component in dashboard.get_components():
            if component.key == self.kwargs["component"]:
                return component

        raise Http404(
            f"Component {self.kwargs['component']} does not exist in dashboard {self.dashboard_class.class_name()}"
        )


class FormComponentView(ComponentView):
    """
    Form Component view, partial rendering of dependant components to support HTMX calls.
    """

    def post(self, request: HttpRequest, *args, **kwargs):
        dashboard = self.get_dashboard(request=request)
        component = self.get_partial_component(dashboard)
        form = component.get_form(request=request)
        if form.is_valid():
            form.save()
            if self.is_ajax():
                return HttpResponse(
                    {"success": True, "form": form.asdict()},
                    content_type="application/json",
                )

            # return HttpResponseRedirect(component.get_absolute_url())

        return self.get(request, *args, **kwargs)

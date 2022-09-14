from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpRequest

from datorum.registry import registry


def get_dashboard(dashboard_class: str, request: HttpRequest, check_permission=True):
    try:
        dashboards = registry.get_all_dashboards()
        dashboard = dashboards[dashboard_class]
    except KeyError:
        raise Http404(f"Dashboard {dashboard_class} does not exist")

    if check_permission and not dashboard.has_permissions(request=request):
        raise PermissionDenied()

    return dashboard

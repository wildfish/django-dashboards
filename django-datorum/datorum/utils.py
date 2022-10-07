from datorum.registry import registry

from .exceptions import DashboardNotFoundError


def get_dashboard_class(app_label: str, dashboard_class: str):
    try:
        dashboard = registry.get_by_classname(app_label, dashboard_class)
    except IndexError:
        raise DashboardNotFoundError(
            f"Dashboard {dashboard_class} not found in registry"
        )

    return dashboard

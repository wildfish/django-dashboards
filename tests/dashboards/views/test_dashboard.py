from django.core.exceptions import PermissionDenied
from django.http import Http404

import pytest

from dashboards.views import DashboardView


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test_get(rf, dashboard):
    request = rf.get("/")
    view = DashboardView(dashboard_class=dashboard)
    view.setup(request=request)
    response = view.get(request)

    assert response.status_code == 200
    assert list(response.context_data.keys()) == ["dashboard", "view"]
    assert isinstance(response.context_data["dashboard"], dashboard)


def test_get_template_names__default(rf, dashboard):
    view = DashboardView(dashboard_class=dashboard)
    view.setup(rf.get("/"))

    assert view.get_template_names() == ["dashboards/dashboard.html"]


def test_get_dashboard__dashboard_class_defined(rf, dashboard):
    request = rf.get("/")
    view = DashboardView(dashboard_class=dashboard)
    view.setup(request)

    assert view.get_dashboard(request=request)


def test_get_dashboard__dashboard_class_not_defined__found(rf, dashboard):
    request = rf.get("/")
    view = DashboardView()
    view.setup(
        request,
        app_label=dashboard._meta.app_label,
        dashboard="testdashboard",
    )

    assert view.dispatch(view.request, *view.args, **view.kwargs)


def test_get_dashboard__dashboard_class_not_defined__not_found(rf, dashboard):
    request = rf.get("/")
    view = DashboardView()
    view.setup(
        request,
        app_label=dashboard._meta.app_label,
        dashboard="DashboardA",
    )

    with pytest.raises(Http404):
        assert view.dispatch(view.request, *view.args, **view.kwargs)


@pytest.mark.django_db
def test_model_dashboard__object_is_set(rf, model_dashboard, user):
    request = rf.get("/")
    request.htmx = False
    view = DashboardView(dashboard_class=model_dashboard)
    view.setup(request, lookup=user.pk)

    assert view.get(request).context_data["dashboard"].object == user


@pytest.mark.django_db
def test_admin_only_dashboard__no_permission(rf, admin_dashboard, user):
    request = rf.get("/")
    request.user = user
    request.htmx = False
    view = DashboardView(dashboard_class=admin_dashboard)
    view.setup(request)

    with pytest.raises(PermissionDenied):
        view.dispatch(request)


@pytest.mark.django_db
def test_admin_only_dashboard__with_permission(rf, admin_dashboard, staff):
    request = rf.get("/")
    request.user = staff
    request.htmx = False
    view = DashboardView(dashboard_class=admin_dashboard)
    view.setup(request)

    assert view.dispatch(request).status_code == 200

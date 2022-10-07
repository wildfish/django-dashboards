from django.core.exceptions import PermissionDenied

import pytest

from datorum.views import DashboardView


pytest_plugins = [
    "datorum.tests.fixtures",
]


def test_view__admin_only__no_permission(rf, django_user_model, admin_dashboard):
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)

    request = rf.get("/")
    request.user = user
    request.htmx = False
    view = DashboardView(dashboard_class=admin_dashboard)
    view.setup(request)
    with pytest.raises(PermissionDenied):
        view.dispatch(request)


def test_view__admin_only__passes(rf, django_user_model, admin_dashboard):
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(
        username=username, password=password, is_staff=True
    )

    request = rf.get("/")
    request.user = user
    request.htmx = False
    view = DashboardView(dashboard_class=admin_dashboard)
    view.setup(request)

    assert view.dispatch(request).status_code == 200

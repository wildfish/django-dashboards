from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

import pytest

from dashboards import permissions
from dashboards.dashboard import Dashboard, ModelDashboard


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.mark.django_db
def test_dashboard__get_dashboard_permissions__permissions_set(admin_dashboard):
    assert admin_dashboard.get_dashboard_permissions() == [permissions.IsAdminUser()]


@pytest.mark.django_db
def test_dashboard__get_dashboard_permissions__no_permissions_set__uses_default(
    dashboard, settings
):
    settings.DASHBOARDS_DEFAULT_PERMISSION_CLASSES = [
        "dashboards.permissions.IsAdminUser"
    ]
    assert dashboard.get_dashboard_permissions() == [permissions.IsAdminUser()]


@pytest.mark.django_db
def test_dashboard__has_permission_fails_for_non_user__not_handled(user, rf):
    class TestDashboard(Dashboard):
        class Meta:
            name = "Test Dashboard"
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = AnonymousUser()
    dashboard = TestDashboard(request=request)

    assert dashboard.has_permissions(request=request, handle=False) is False


@pytest.mark.django_db
def test_dashboard__has_permission_fails_for_non_user__handled(user, rf):
    class TestDashboard(Dashboard):
        class Meta:
            name = "Test Dashboard"
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = AnonymousUser()
    dashboard = TestDashboard(request=request)

    has_perm = dashboard.has_permissions(request=request, handle=True)
    assert not isinstance(has_perm, bool)
    assert isinstance(has_perm, HttpResponseRedirect)
    assert has_perm.url == "/accounts/login/?next=/"


@pytest.mark.django_db
def test_dashboard__has_permission_fails_for_non_admin__not_handled(user, rf):
    class TestDashboard(Dashboard):
        class Meta:
            name = "Test Dashboard"
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = user
    dashboard = TestDashboard(request=request)

    assert dashboard.has_permissions(request=request, handle=False) is False


@pytest.mark.django_db
def test_dashboard__has_permission_fails_for_non_admin__handled(user, rf):
    class TestDashboard(Dashboard):
        class Meta:
            name = "Test Dashboard"
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = user
    dashboard = TestDashboard(request=request)

    with pytest.raises(PermissionDenied):
        assert dashboard.has_permissions(request=request, handle=True)


@pytest.mark.django_db
def test_dashboard__has_permission_passes_for_authenticated_user(user, rf):
    class TestDashboard(Dashboard):
        class Meta:
            name = "Test Dashboard"
            app_label = "app1"
            permission_classes = [permissions.IsAuthenticated]

    request = rf.get("/")
    request.user = user
    dashboard = TestDashboard(request=request)

    assert dashboard.has_permissions(request) is True


@pytest.mark.django_db
def test_model_dashboard__has_permission_fails_for_non_admin__not_handled(user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = user
    lookup = user.pk
    dashboard = TestModelDashboard(request=request, lookup=lookup)

    assert dashboard.has_permissions(request=request, handle=False) is False


@pytest.mark.django_db
def test_model_dashboard__has_permission_fails_for_non_admin__handled(user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = user
    lookup = user.pk
    dashboard = TestModelDashboard(request=request, lookup=lookup)

    with pytest.raises(PermissionDenied):
        assert dashboard.has_permissions(request=request, handle=True) is False


@pytest.mark.django_db
def test_model_dashboard__has_permission_fails_for_non_user__handled(user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = AnonymousUser()
    lookup = user.pk
    dashboard = TestModelDashboard(request=request, lookup=lookup)

    has_perm = dashboard.has_permissions(request=request, handle=True)
    assert not isinstance(has_perm, bool)
    assert isinstance(has_perm, HttpResponseRedirect)
    assert has_perm.url == "/accounts/login/?next=/"


@pytest.mark.django_db
def test_model_dashboard__has_permission_fails_for_non_user__not_handled(user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    request = rf.get("/")
    request.user = AnonymousUser()
    lookup = user.pk
    dashboard = TestModelDashboard(request=request, lookup=lookup)

    assert dashboard.has_permissions(request=request, handle=False) is False


@pytest.mark.django_db
def test_model_dashboard__has_permission_passes_for_authenticated_user(user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"
            permission_classes = [permissions.IsAuthenticated]

    request = rf.get("/")
    request.user = user
    lookup = user.pk
    dashboard = TestModelDashboard(request=request, lookup=lookup)

    assert dashboard.has_permissions(request) is True

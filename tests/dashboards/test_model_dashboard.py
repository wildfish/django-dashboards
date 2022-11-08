from django.contrib.auth.models import User
from django.http.response import Http404

import pytest

from wildcoeus.dashboards import permissions
from wildcoeus.dashboards.dashboard import ModelDashboard


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test__get_object__missing_kwargs__raises_exceptiobn(model_dashboard, rf):
    request = rf.get("/")
    with pytest.raises(AttributeError):
        model_dashboard(request=request).get_object()


@pytest.mark.django_db
def test__get_object__missing_model_404(model_dashboard, rf):
    request = rf.get("/")
    with pytest.raises(Http404):
        model_dashboard(request=request, lookup="1").get_object()


@pytest.mark.django_db
def test__get_object(model_dashboard, user, rf):
    request = rf.get("/")
    lookup = user.pk
    assert model_dashboard(request=request, lookup=lookup).object == user


@pytest.mark.django_db
def test__get_object__change_lookup_field(model_dashboard, user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"
            lookup_field = "username"

    request = rf.get("/")
    lookup = user.username
    dashboard = TestModelDashboard(request=request, lookup=lookup)

    assert dashboard.get_object() == user


@pytest.mark.django_db
def test__get_object__change_lookup_kwarg(user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"
            lookup_kwarg = "username"
            lookup_field = "username"

    request = rf.get("/")
    lookup = user.username
    dashboard = TestModelDashboard(request=request, username=lookup)

    assert dashboard.get_object() == user


@pytest.mark.django_db
def test__get_queryset(model_dashboard, user, rf):
    request = rf.get("/")
    lookup = user.pk
    qs = model_dashboard(request=request, lookup=lookup).get_queryset()
    assert qs.model == model_dashboard._meta.model
    assert user in qs


@pytest.mark.django_db
def test__get_queryset__no_model__raises_exception(user, rf):
    class TestModelDashboard(ModelDashboard):
        class Meta:
            name = "Test Model Dashboard"
            model = None
            app_label = "app1"

    request = rf.get("/")
    lookup = user.pk
    dashboard = TestModelDashboard(request=request, lookup=lookup)

    with pytest.raises(AttributeError):
        dashboard.get_queryset()


@pytest.mark.django_db
def test_model_dashboard__get_absolute_url(model_dashboard, user, rf):
    request = rf.get("/")
    lookup = user.pk

    dashboard = model_dashboard(request=request, lookup=lookup)

    assert dashboard.get_absolute_url() == f"/app1/testmodeldashboard/{lookup}/"


@pytest.mark.django_db
def test_model_dashboard__get_urls(model_dashboard, user, rf):
    request = rf.get("/")
    lookup = user.pk
    urls = model_dashboard(request=request, lookup=lookup).get_urls()
    assert len(urls) == 1
    assert urls[0].name == "app1_testmodeldashboard_dashboard_detail"
    assert (
        str(urls[0].pattern)
        == f"app1/testmodeldashboard/<str:{model_dashboard._meta.lookup_kwarg}>/"
    )


@pytest.mark.django_db
def test_model_dashboard__has_permission_fails_for_non_admin(user, rf):
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

    assert dashboard.has_permissions(request) is False


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

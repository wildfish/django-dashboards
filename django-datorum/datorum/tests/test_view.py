from django.http import Http404
from django.test.utils import override_settings

import pytest

from datorum.views import ComponentView, DashboardView

from . import urls


pytest_plugins = [
    "datorum.tests.fixtures",
]


def test_view__get_template_names__default(rf, dashboard):
    view = DashboardView(dashboard_class=dashboard)
    view.setup(rf.get("/"))

    assert view.get_template_names() == ["datorum/dashboard.html"]


@override_settings(ROOT_URLCONF=urls)
def test_view__get_template_names__partial(rf, dashboard):
    view = ComponentView(dashboard_class=dashboard)
    view.setup(rf.get("/app1/TestDashboard/component_1/"))

    assert view.get_template_names() == ["datorum/components/partial.html"]


@override_settings(ROOT_URLCONF=urls)
def test_view__get_partial__htmx__component_found(rf, dashboard):
    request = rf.get("/app1/TestDashboard/component_1/")
    request.htmx = True
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        app_label=dashboard.Meta.app_label,
        dashboard="TestDashboard",
        component="component_1",
    )

    actual_dashboard = dashboard(request=request)
    assert (
        view.get_partial_component(actual_dashboard)
        == actual_dashboard.components["component_1"]
    )


@override_settings(ROOT_URLCONF=urls)
def test_view__get_partial__component_not_found(rf, dashboard):
    request = rf.get("/app1/TestDashboard/component_10/")
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        app_label=dashboard.Meta.app_label,
        dashboard="TestDashboard",
        component="component_10",
    )

    with pytest.raises(Http404):
        view.get_partial_component(dashboard(request=request))


@override_settings(ROOT_URLCONF=urls)
def test_view__get__json(rf, dashboard, snapshot):
    request = rf.get("/app1/TestDashboard/component_2/")
    request.htmx = False
    request.headers = {"x-requested-with": "XMLHttpRequest"}
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        app_label=dashboard.Meta.app_label,
        dashboard="TestDashboard",
        component="component_2",
    )

    snapshot.assert_match(view.get(request).content)


@override_settings(ROOT_URLCONF=urls)
def test_view__get__partial_template(rf, dashboard, snapshot):
    request = rf.get("/app1/TestDashboard/component_2/")
    request.htmx = True
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        app_label=dashboard.Meta.app_label,
        dashboard="TestDashboard",
        component="component_2",
    )

    snapshot.assert_match(view.get(request).rendered_content)


@override_settings(ROOT_URLCONF=urls)
def test_view__get__all(rf, dashboard, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = DashboardView(dashboard_class=dashboard)
    view.setup(request)

    snapshot.assert_match(view.get(request).rendered_content)


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=urls)
def test_view__with_model(rf, model_dashboard, user, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = DashboardView(dashboard_class=model_dashboard)
    view.setup(request, lookup=user.pk)

    assert view.get(request).context_data["dashboard"].object == user


@pytest.mark.django_db
@override_settings(ROOT_URLCONF=urls)
def test_component_view__with_model(rf, model_dashboard, user, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = ComponentView(dashboard_class=model_dashboard)
    view.setup(
        request,
        app_label=model_dashboard.Meta.app_label,
        dashboard=model_dashboard.__name__,
        lookup=user.pk,
        component="component_1",
    )
    snapshot.assert_match(view.get(request).rendered_content)

    snapshot.assert_match(view.get(request).rendered_content)
    assert view.get(request).context_data["dashboard"].object == user

from django.http import Http404
from django.test.utils import override_settings

import pytest

from datorum.views import ComponentView, DashboardView

from . import urls


pytest_plugins = [
    "datorum.tests.fixtures",
]


def test_view__get_template_names__default(rf, test_dashboard):
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(rf.get("/"))

    assert view.get_template_names() == ["datorum/dashboard.html"]


@override_settings(ROOT_URLCONF=urls)
def test_view__get_template_names__partial(rf, test_dashboard):
    view = ComponentView()
    view.setup(rf.get("/TestDashboard/component_1/"))

    assert view.get_template_names() == ["datorum/components/partial.html"]


@override_settings(ROOT_URLCONF=urls)
def test_view__get_partial__htmx__component_found(rf, test_dashboard):
    request = rf.get("/TestDashboard/component_1/")
    request.htmx = True
    view = ComponentView()
    view.setup(request, dashboard="TestDashboard", component="component_1")

    assert view.get_partial_component() == test_dashboard.component_1


@override_settings(ROOT_URLCONF=urls)
def test_view__get_partial__component_not_found(rf, test_dashboard):
    request = rf.get("/TestDashboard/component_10/")
    view = ComponentView()
    view.setup(request, dashboard="TestDashboard", component="component_10")

    with pytest.raises(Http404):
        view.get_partial_component()


@override_settings(ROOT_URLCONF=urls)
def test_view__get__json(rf, test_dashboard, snapshot):
    request = rf.get("/TestDashboard/component_2/")
    request.htmx = False
    request.headers = {"x-requested-with": "XMLHttpRequest"}
    view = ComponentView()
    view.setup(request, dashboard="TestDashboard", component="component_2")

    snapshot.assert_match(view.get(request).content)


@override_settings(ROOT_URLCONF=urls)
def test_view__get__partial_template(rf, test_dashboard, snapshot):
    request = rf.get("/TestDashboard/component_2/")
    request.htmx = True
    view = ComponentView()
    view.setup(request, dashboard="TestDashboard", component="component_2")

    snapshot.assert_match(view.get(request).rendered_content)


@override_settings(ROOT_URLCONF=urls)
def test_view__get__all(rf, test_dashboard, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(request)

    snapshot.assert_match(view.get(request).rendered_content)

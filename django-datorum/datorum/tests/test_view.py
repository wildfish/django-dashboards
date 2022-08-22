from django.test.utils import override_settings

from datorum.views import DashboardView

from . import urls


pytest_plugins = [
    "datorum.tests.fixtures",
]


def test_view__get_template_names__default(rf, test_dashboard):
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(rf.get("/"))

    assert view.get_template_names() == ["datorum/dashboard.html"]


def test_view__get_template_names__partial(rf, test_dashboard):
    view = DashboardView(dashboard_class=test_dashboard)
    view.partial_component = test_dashboard.component_1
    view.setup(rf.get("?key=component_1"))

    assert view.get_template_names() == ["datorum/components/partial.html"]


def test_view__get_partial__htmx__component_found(rf, test_dashboard):
    request = rf.get("/?key=component_1")
    request.htmx = True
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(request)

    assert view.get_partial_component() == test_dashboard.component_1


def test_view__get_partial__htmx__component_not_found(rf, test_dashboard):
    request = rf.get("/?key=component_10")
    request.htmx = True
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(request)

    assert not view.get_partial_component()


def test_view__get_partial__not_htmx__component_not_found(rf, test_dashboard):
    request = rf.get("/?key=component_1")
    request.htmx = False
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(request)

    assert not view.get_partial_component()


def test_view__get__json(rf, test_dashboard, snapshot):
    request = rf.get("/?key=component_2")
    request.htmx = False
    request.headers = {"x-requested-with": "XMLHttpRequest"}
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(request)

    snapshot.assert_match(view.get(request).content)


def test_view__get__partial_template(rf, test_dashboard, snapshot):
    request = rf.get("/?key=component_2")
    request.htmx = True
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(request)

    snapshot.assert_match(view.get(request).rendered_content)


@override_settings(ROOT_URLCONF=urls)
def test_view__get__all(rf, test_dashboard, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = DashboardView(dashboard_class=test_dashboard)
    view.setup(request)

    snapshot.assert_match(view.get(request).rendered_content)

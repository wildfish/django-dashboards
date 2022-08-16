from datorum.views import DashboardView


pytest_plugins = [
    "datorum.tests.fixtures",
]


def test_view__get_template_names__default(rf, test_dashboard):
    view = DashboardView(dashboard=test_dashboard)
    view.setup(rf.get("/"))

    assert view.get_template_names() == ["datorum/as_grid.html"]


def test_view__get_template_names__partial(rf, test_dashboard):
    view = DashboardView(dashboard=test_dashboard)
    view.partial_component = test_dashboard.component_1
    view.setup(rf.get("?key=component_1"))

    assert view.get_template_names() == ["datorum/components/partial.html"]

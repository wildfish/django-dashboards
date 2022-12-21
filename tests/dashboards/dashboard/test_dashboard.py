import pytest

from tests.dashboards.app1.dashboards import TestDashboard, TestModelDashboard
from wildcoeus.dashboards.component import Text
from wildcoeus.dashboards.dashboard import Dashboard


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test__get_attributes_order(dashboard, snapshot):
    snapshot.assert_match(dashboard.components.keys())


def test__get_attributes_order__with_parent(complex_dashboard, snapshot):
    snapshot.assert_match(complex_dashboard.components.keys())


def test__get_components__no_layout(dashboard, rf):
    request = rf.get("/")
    assert dashboard(request=request).get_components() == [
        dashboard.components["component_1"],
        dashboard.components["component_2"],
        dashboard.components["component_3"],
    ]


def test__get_components__with_parent__no_layout(complex_dashboard, rf):
    request = rf.get("/")

    assert complex_dashboard(request=request).get_components() == [
        complex_dashboard.components["component_1"],
        complex_dashboard.components["component_2"],
        complex_dashboard.components["component_3"],
        complex_dashboard.components["component_4"],
        complex_dashboard.components["component_5"],
        complex_dashboard.components["component_6"],
        complex_dashboard.components["component_7"],
    ]


@pytest.mark.django_db
def test_dashboard__get_absolute_url(dashboard, rf):
    request = rf.get("/")
    assert dashboard(request=request).get_absolute_url() == "/app1/testdashboard/"


@pytest.mark.django_db
def test_dashboard__with_get_FOO_methods(dashboard, rf):
    class TestDashboardSingle(Dashboard):
        component_value = Text()
        component_defer = Text()

        def get_component_value_value(self):
            return "Foo"

        def get_component_defer_defer(self):
            return "Bar"

    request = rf.get("/")

    assert (
        TestDashboardSingle(request=request).components["component_value"].value()
        == "Foo"
    )
    assert (
        TestDashboardSingle(request=request).components["component_value"].defer is None
    )
    assert (
        TestDashboardSingle(request=request).components["component_defer"].defer()
        == "Bar"
    )
    assert (
        TestDashboardSingle(request=request).components["component_defer"].value is None
    )


@pytest.mark.parametrize(
    "dashboard_class",
    [
        {"klass": TestDashboard, "expected": "testdashboard"},
        {"klass": TestModelDashboard, "expected": "testmodeldashboard"},
    ],
)
def test_dashboard__class_name_method(dashboard_class):
    assert dashboard_class["klass"].class_name() == dashboard_class["expected"]


@pytest.mark.parametrize(
    "dashboard_class",
    [
        {"klass": TestDashboard, "expected": "app1_testdashboard"},
        {"klass": TestModelDashboard, "expected": "app1_testmodeldashboard"},
    ],
)
def test_dashboard__get_slug_method(dashboard_class):
    assert dashboard_class["klass"].get_slug() == dashboard_class["expected"]


def test_dashboard__str(dashboard, rf):
    request = rf.get("/")

    assert str(dashboard(request)) == "Test Dashboard"


# def test_dashboard__render__template_name(dashboard, rf, snapshot):
#     request = rf.get("/")
#     d = dashboard(request)
#     snapshot.assert_match(d.render(request, template_name="foo.html"))


# More tests to add here re layout

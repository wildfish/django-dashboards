import pytest


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


# More tests to add here re layout

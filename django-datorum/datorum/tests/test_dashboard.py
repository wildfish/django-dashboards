pytest_plugins = [
    "datorum.tests.fixtures",
]


def test__get_attributes_order(dashboard, snapshot):
    snapshot.assert_match(dashboard.get_attributes_order())


def test__get_attributes_order__with_parent(complex_dashboard, snapshot):
    snapshot.assert_match(complex_dashboard.get_attributes_order())


def test__get_components__no_layout(dashboard):
    assert dashboard.get_components() == [
        dashboard.component_1,
        dashboard.component_2,
    ]


def test__get_components__with_parent__no_layout(complex_dashboard):
    assert complex_dashboard.get_components() == [
        complex_dashboard.component_3,
        complex_dashboard.component_2,
        complex_dashboard.component_4,
        complex_dashboard.component_5,
        complex_dashboard.component_6,
        complex_dashboard.component_1,
    ]


# More tests to add here re layout

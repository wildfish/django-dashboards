pytest_plugins = [
    "datorum.tests.fixtures",
]


def test__get_attributes_order(test_dashboard, snapshot):
    snapshot.assert_match(test_dashboard.get_attributes_order())


def test__get_attributes_order__with_parent(test_complex_dashboard, snapshot):
    snapshot.assert_match(test_complex_dashboard.get_attributes_order())


def test__get_components__no_layout(test_dashboard):
    assert test_dashboard.get_components(with_layout=False) == [
        test_dashboard.component_1,
        test_dashboard.component_2,
    ]


def test__get_components__with_parent__no_layout(test_complex_dashboard):
    assert test_complex_dashboard.get_components(with_layout=False) == [
        test_complex_dashboard.component_3,
        test_complex_dashboard.component_2,
        test_complex_dashboard.component_4,
        test_complex_dashboard.component_1,
    ]


# More tests to add here re layout

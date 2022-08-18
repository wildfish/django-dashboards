import pytest

from datorum.component import Text
from datorum.dashboard import Dashboard


@pytest.fixture
def test_dashboard():
    class TestDashboard(Dashboard):
        component_1 = Text(value="value")
        component_2 = Text(defer=lambda _: "value")

    return TestDashboard


@pytest.fixture
def test_complex_dashboard(test_dashboard):
    class TestComplexDashboard(test_dashboard):
        component_3 = Text(defer=lambda _: "value")
        component_2 = Text(defer=lambda _: "value")
        component_4 = Text(value="value")

    return TestComplexDashboard

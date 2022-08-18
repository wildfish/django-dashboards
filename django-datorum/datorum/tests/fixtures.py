import pytest
import strawberry

from datorum.component import Text
from datorum.dashboard import Dashboard
from datorum.schema import DashboardQuery


@pytest.fixture
def test_dashboard():
    class TestDashboard(Dashboard):
        component_1 = Text(value="value")
        component_2 = Text(defer=lambda _: "value")

        class Meta:
            name = "Test Dashboard"

    return TestDashboard


@pytest.fixture
def test_complex_dashboard(test_dashboard):
    class TestComplexDashboard(test_dashboard):
        component_3 = Text(defer=lambda _: "value")
        component_2 = Text(defer=lambda _: "value")
        component_4 = Text(value="value")

        class Meta:
            name = "Test Complex Dashboard"

    return TestComplexDashboard


@pytest.fixture
def schema():
    return strawberry.Schema(query=DashboardQuery)

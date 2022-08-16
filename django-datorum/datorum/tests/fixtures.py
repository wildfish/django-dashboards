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

    return TestDashboard


@pytest.fixture
def schema():
    return strawberry.Schema(query=DashboardQuery)

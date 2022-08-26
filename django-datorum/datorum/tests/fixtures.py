import pytest
import strawberry

from datorum import permissions
from datorum.component import HTML, Chart, Table, Text
from datorum.component.chart import ChartData
from datorum.component.table import TableData
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
        component_4 = HTML(value="<div></div>")
        component_5 = Table(
            value=TableData(headers=["a", "b"], rows=[{"a": "Value", "b": "Value b"}])
        )
        component_6 = Chart(
            value=ChartData(data=[ChartData.Trace(x=["a"], y=["b"])], layout={})
        )

        class Meta:
            name = "Test Complex Dashboard"

    return TestComplexDashboard


@pytest.fixture
def test_admin_dashboard():
    class TestAdminDashboard(Dashboard):
        permission_classes = [permissions.IsAdminUser]
        component_1 = Text(value="admin value")

        class Meta:
            name = "Test Admin Dashboard"

    return TestAdminDashboard


@pytest.fixture
def schema():
    return strawberry.Schema(query=DashboardQuery)

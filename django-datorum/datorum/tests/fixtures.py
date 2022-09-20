import pytest
import strawberry

from datorum import permissions
from datorum.component import Chart, Table, Text
from datorum.component.chart import ChartData
from datorum.component.layout import ComponentLayout, Div
from datorum.component.table import TableData
from datorum.dashboard import Dashboard
from datorum.schema import DashboardQuery


@pytest.fixture
def dashboard():
    class TestDashboard(Dashboard):
        component_1 = Text(value="value")
        component_2 = Text(defer=lambda _: "value")

        class Meta:
            name = "Test Dashboard"

    return TestDashboard


@pytest.fixture
def complex_dashboard(dashboard):
    class TestComplexDashboard(dashboard):
        component_3 = Text(defer=lambda _: "value")
        component_2 = Text(defer=lambda _: "value")
        component_4 = Text(value="<div></div>", mark_safe=True)
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
def admin_dashboard():
    class TestAdminDashboard(Dashboard):
        permission_classes = [permissions.IsAdminUser]
        component_1 = Text(value="admin value")

        class Meta:
            name = "Test Admin Dashboard"

    return TestAdminDashboard


@pytest.fixture
def schema():
    return strawberry.Schema(query=DashboardQuery)


@pytest.fixture
def dashboard_with_layout(dashboard):
    class TestDashboardWithLayout(dashboard):
        class Meta:
            name = "Test Dashboard with Layout"

        class Layout:
            components = ComponentLayout(
                Div(
                    Div(
                        "component_1",
                        css_classes="css_style",
                        width=99,
                    ),
                    Div(
                        "component_2",
                        css_classes="css_style",
                    ),
                ),
            )

    return TestDashboardWithLayout

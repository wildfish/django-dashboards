from unittest.mock import patch

from django.contrib.auth.models import User

import pytest
import strawberry

from wildcoeus.dashboards import permissions
from wildcoeus.dashboards.component import Chart, Table, Text
from wildcoeus.dashboards.component.chart import ChartData
from wildcoeus.dashboards.component.layout import ComponentLayout, Div
from wildcoeus.dashboards.component.table import TableData
from wildcoeus.dashboards.dashboard import Dashboard, ModelDashboard
from wildcoeus.dashboards.registry import registry
from wildcoeus.dashboards.schema import DashboardQuery


@pytest.fixture(autouse=True)
def mock_random_ms_delay():
    with patch(
        "wildcoeus.dashboards.templatetags.wildcoeus.random.randint"
    ) as random_ms_delay:
        random_ms_delay.return_value = 1
        yield random_ms_delay


@pytest.fixture
def dashboard():
    class TestDashboard(Dashboard):
        component_1 = Text(value="value")
        component_2 = Text(defer=lambda **kwargs: "value")
        component_3 = Text(value=lambda **kwargs: "value from callable")

        class Meta:
            name = "Test Dashboard"
            app_label = "app1"

    registry.register(TestDashboard)
    return TestDashboard


@pytest.fixture
def complex_dashboard(dashboard):
    class TestComplexDashboard(dashboard):
        component_4 = Text(defer=lambda **kwargs: "value")
        component_3 = Text(defer=lambda **kwargs: "value")
        component_5 = Text(value="<div></div>", mark_safe=True)
        component_6 = Table(
            value=TableData(data=[{"a": "Value", "b": "Value b"}]), columns=["a", "b"]
        )
        component_7 = Chart(
            value=ChartData(data=[ChartData.Trace(x=["a"], y=["b"])], layout={})
        )

        class Meta:
            name = "Test Complex Dashboard"
            app_label = "app1"

    registry.register(TestComplexDashboard)
    return TestComplexDashboard


@pytest.fixture
def admin_dashboard():
    class TestAdminDashboard(Dashboard):
        component_1 = Text(value="admin value")

        class Meta:
            name = "Test Admin Dashboard"
            app_label = "app1"
            permission_classes = [permissions.IsAdminUser]

    registry.register(TestAdminDashboard)
    return TestAdminDashboard


@pytest.fixture
def model_dashboard():
    class TestModelDashboard(ModelDashboard):
        component_1 = Text(value="value")

        class Meta:
            name = "Test Model Dashboard"
            model = User
            app_label = "app1"

    registry.register(TestModelDashboard)
    return TestModelDashboard


@pytest.fixture
def schema():
    return strawberry.Schema(query=DashboardQuery)


@pytest.fixture
def dashboard_with_layout(dashboard):
    class TestDashboardWithLayout(dashboard):
        class Meta:
            name = "Test Dashboard with Layout"
            app_label = "app1"

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

    registry.register(TestDashboardWithLayout)
    return TestDashboardWithLayout


@pytest.fixture
def user():
    user = User.objects.create(
        username="tester", is_active=True, email="tester@test.com"
    )
    user.set_password("password")
    user.save()
    return user

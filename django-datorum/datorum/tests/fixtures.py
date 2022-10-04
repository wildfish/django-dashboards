from django.contrib.auth.models import User

import pytest
import strawberry

from datorum import permissions
from datorum.component import Chart, Table, Text
from datorum.component.chart import ChartData
from datorum.component.layout import ComponentLayout, Div
from datorum.component.table import TableData
from datorum.dashboard import Dashboard, ModelDashboard
from datorum.registry import registry
from datorum.schema import DashboardQuery


@pytest.fixture
def dashboard():
    class TestDashboard(Dashboard):
        component_1 = Text(value="value")
        component_2 = Text(defer=lambda **kwargs: "value")

        class Meta:
            name = "Test Dashboard"
            app_label = "app1"

    registry.register(TestDashboard)
    return TestDashboard


@pytest.fixture
def complex_dashboard(dashboard):
    class TestComplexDashboard(dashboard):
        component_3 = Text(defer=lambda **kwargs: "value")
        component_2 = Text(defer=lambda **kwargs: "value")
        component_4 = Text(value="<div></div>", mark_safe=True)
        component_5 = Table(
            value=TableData(headers=["a", "b"], data=[{"a": "Value", "b": "Value b"}])
        )
        component_6 = Chart(
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
        permission_classes = [permissions.IsAdminUser]
        component_1 = Text(value="admin value")

        class Meta:
            name = "Test Admin Dashboard"
            app_label = "app1"

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

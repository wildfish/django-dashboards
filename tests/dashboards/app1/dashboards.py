import json

from django import forms
from django.contrib.auth.models import User

from wildcoeus.dashboards import permissions
from wildcoeus.dashboards.component import Chart, Form, Table, Text
from wildcoeus.dashboards.component.layout import HR, ComponentLayout, Div
from wildcoeus.dashboards.component.table import TableSerializer
from wildcoeus.dashboards.dashboard import Dashboard, ModelDashboard
from wildcoeus.dashboards.forms import DashboardForm
from wildcoeus.dashboards.registry import registry


class TestDashboard(Dashboard):
    component_1 = Text(value="value")
    component_2 = Text(defer=lambda **kwargs: "value")
    component_3 = Text(value=lambda **kwargs: "value from callable")

    class Meta:
        name = "Test Dashboard"


class TestTableSerializer(TableSerializer):
    class Meta:
        columns = {"a": "A", "b": "B"}

    def get_data(self, *args, **kwargs):
        return [{"a": "Value", "b": "Value b"}]


class TestComplexDashboard(TestDashboard):
    component_4 = Text(defer=lambda **kwargs: "value")
    component_3 = Text(defer=lambda **kwargs: "value")
    component_5 = Text(value="<div></div>", mark_safe=True)
    component_6 = Table(value=TestTableSerializer)
    component_7 = Chart(
        value=lambda **kwargs: json.dumps(
            dict(data=[dict(x=["a"], y=["b"])], layout={})
        )
    )

    class Meta:
        name = "Test Complex Dashboard"


class TestAdminDashboard(Dashboard):
    component_1 = Text(value="admin value")

    class Meta:
        name = "Test Admin Dashboard"
        permission_classes = [permissions.IsAdminUser]


class TestModelDashboard(ModelDashboard):
    component_1 = Text(value="value")

    class Meta:
        name = "Test Model Dashboard"
        model = User
        app_label = "app1"
        include_in_graphql = False


class TestFilterDashboard(Dashboard):
    class TestForm(DashboardForm):
        country = forms.ChoiceField(
            choices=(
                ("all", "All"),
                ("one", "one"),
                ("two", "two"),
            )
        )

        def save(self):
            return

    filter_component = Form(
        form=TestForm,
        method="get",
        dependents=["dependent_component_1", "dependent_component_2"],
    )
    dependent_component_1 = Text(
        value=lambda **k: f"filter={k['filters'].get('filter_form')}"
    )
    dependent_component_2 = Text(
        value=lambda **k: f"filter={k['filters'].get('filter_form')}"
    )
    non_dependent_component_3 = Text(value="A value")

    class Meta:
        name = "Test Filter Dashboard"


class TestDashboardWithLayout(TestDashboard):
    class Meta:
        name = "Test Dashboard with Layout"

    class Layout:
        components = ComponentLayout(
            HR(),
            Div(
                Div(
                    "component_1",
                    css_classes="css_style",
                ),
                Div(
                    "component_2",
                    css_classes="css_style",
                ),
            ),
        )


class TestNoMetaDashboard(Dashboard):
    component_1 = Text(value="value")


registry.register(TestDashboard)
registry.register(TestFilterDashboard)
registry.register(TestAdminDashboard)
registry.register(TestComplexDashboard)
registry.register(TestDashboardWithLayout)
registry.register(TestModelDashboard)
registry.register(TestNoMetaDashboard)

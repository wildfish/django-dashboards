from datorum.component import CTA, Chart, Form, Map, Stat, Table, Text
from datorum.component.layout import HR
from datorum.component.layout import HTML
from datorum.component.layout import HTML as LayoutHTML
from datorum.component.layout import (Card, ComponentLayout, Div, Header, Tab,
                                      TabContainer)
from datorum.component.table import TableData
from datorum.dashboard import Dashboard, ModelDashboard
from datorum.permissions import IsAdminUser
from django.urls import reverse_lazy

from demo.demo_app.data import DashboardData, VehicleData
from demo.demo_app.forms import AnimalForm, ExampleForm, VehicleTypeFilterForm
from demo.demo_app.models import Vehicle


class DemoDashboardOne(Dashboard):
    link = CTA(
        href=reverse_lazy("datorum:dashboards:demodashboardonecustom_dashboard"),
        text="Find out more!",
        width=3,
    )
    text_example = Text(
        value="Rendered on load",
        width=6,
    )
    html_example = Text(
        value="<strong>HTML also rendered on load</strong>", mark_safe=True
    )
    calculated_example = Text(defer=lambda **kwargs: "Deferred text")
    form_example = Form(
        form=AnimalForm,
        method="get",
        dependents=["chart_example", "stacked_chart_example"],
        width=4,
    )
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data, width=4)
    stacked_chart_example = Chart(defer=DashboardData.fetch_stacked_bar_chart_data, width=4)
    bubble_chart_example = Chart(defer=DashboardData.fetch_bubble_chart_data)
    filter_form = Form(
        form=ExampleForm,
        method="get",
        dependents=["line_chart_example", "stat_three"],
        width=12,
    )
    line_chart_example = Chart(
        defer=DashboardData.fetch_scatter_chart_data,
    )
    stat_three = Stat(
        defer=lambda **kwargs: {
            "text": "33%",
            "sub_text": kwargs.get('filters', {}).get("country", "all"),
        }
    )
    stat_one = Stat(value={"text": "100%", "sub_text": "increase"})
    stat_two = Stat(value={"text": "88%", "sub_text": "increase"})
    free_text_example = Text(defer=DashboardData.fetch_html, mark_safe=True)
    gauge_one = Chart(defer=DashboardData.fetch_gauge_chart_data)
    gauge_two = Chart(defer=DashboardData.fetch_gauge_chart_data_two)
    table_example = Table(defer=DashboardData.fetch_table_data)
    table_example_not_deferred = Table(
        value=TableData(
            headers=[],
            rows=[
                {
                    "id": 1,
                    "name": "Oli Bob",
                    "progress": 12,
                    "gender": "male",
                    "rating": 1,
                    "col": "red",
                    "dob": "19/02/1984",
                    "car": 1,
                }
            ],
        )
    )
    scatter_map_example = Map(defer=DashboardData.fetch_scatter_map_data)
    choropleth_map_example = Map(defer=DashboardData.fetch_choropleth_map_data)

    class Meta:
        name = "Dashboard One"


class DemoDashboardOneCustom(DemoDashboardOne):
    template_name = "demo/custom.html"


class DemoDashboardOneVary(DemoDashboardOne):
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data, width=12)
    calculated_example = Text(
        defer=lambda **kwargs: "some calculated text", width=3
    )
    table_example = Table(defer=DashboardData.fetch_table_data, width=12)

    class Meta:
        name = "Dashboard One Vary"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            Header(heading="Header", size=2, width=12),
            HTML(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec vestibulum orci. Sed ac eleifend "
                "diam. Duis quis congue ex. Mauris at bibendum est, nec bibendum ipsum. Lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit.",
                width=12,
            ),
            Card("text_example", "html_example", width=4),
            Card(
                Div("stat_one"),
                Div("stat_two"),
                Div("stat_three"),
            ),
            HR(width=12),
            Header(heading="Tab Example", size=3, width=12),
            TabContainer(
                Tab(
                    "Calculated Example",
                    Card("calculated_example"),
                    Card("chart_example"),
                    width=12,
                ),
                Tab(
                    "Table Example",
                    Card("table_example"),
                    Card("gauge_two"),
                    width=12,
                ),
                width=12,
            ),
        )


class DemoDashboardAdmin(Dashboard):
    permission_classes = [IsAdminUser]
    admin_text = Text(value="Admin Only Text")
    scatter_map_example = Map(defer=DashboardData.fetch_scatter_map_data)
    choropleth_map_example = Map(defer=DashboardData.fetch_choropleth_map_data)

    class Meta:
        name = "Admin Dashboard"


class VehicleOverviewDashboard(Dashboard):
    filter_form = Form(
        form=VehicleTypeFilterForm,
        method="get",
        dependents=[
            "no_vehicles",
            "in_use",
            "available",
            "requires_service",
            "vehicles",
        ],
        width=3,
    )
    no_vehicles = Stat(defer=VehicleData.fetch_vehicle_count, href="?type=c1", width=4)
    in_use = Stat(defer=VehicleData.fetch_in_use_count, width=4)
    available = Stat(defer=VehicleData.fetch_out_of_service_count, width=4)
    requires_service = Stat(defer=VehicleData.fetch_service_count, width=4)
    map = Map(defer=VehicleData.fetch_current_locations, width=12)
    vehicles = Table(defer=VehicleData.fetch_vehicles, width=12)

    class Meta:
        name = "Vehicle Dashboard"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            HTML(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec vestibulum orci. Sed ac eleifend "
                "diam. Duis quis congue ex. Mauris at bibendum est, nec bibendum ipsum. Lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit.",
                width=12,
            ),
            "filter_form",
            Div(
                Card("no_vehicles", width=3),
                Card("in_use", width=3),
                Card("available", width=3),
                Card("requires_service", width=3),
                css_classes="dashboard-container",
                width=12,
            ),
            Card(
                "map",
                "vehicles",
                width=12,
            ),
        )


class VehicleDetailDashboard(ModelDashboard):
    vehicle_details = Stat(defer=VehicleData.fetch_vehicle_details, width=6)
    map = Map(defer=VehicleData.fetch_last_route, width=6)

    class Meta(Dashboard.Meta):
        name = "Vehicle Detail Dashboard"
        model = Vehicle

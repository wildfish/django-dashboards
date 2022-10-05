from random import randint

from django.urls import reverse_lazy

from datorum.component import CTA, Chart, Form, Map, Stat, Table, Text
from datorum.component.layout import (
    HR,
    HTML,
    Card,
    ComponentLayout,
    Div,
    Header,
    Tab,
    TabContainer,
)
from datorum.component.table import TableData, TablePaging
from datorum.component.text import CTAData
from datorum.dashboard import Dashboard
from datorum.permissions import IsAdminUser
from datorum.registry import registry

from demo.kitchensink.components import SSEChart, SSEStat
from demo.kitchensink.data import DashboardData
from demo.kitchensink.forms import AnimalForm, ExampleForm


class DemoDashboardOne(Dashboard):
    link = CTA(
        value=CTAData(
            href=reverse_lazy("datorum:dashboards:kitchensink_demodashboardonecustom"),
            text="Find out more!",
        ),
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
        dependents=["chart_example", "stacked_chart_example", "stat_three"],
        width=4,
    )
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data, width=4)
    stacked_chart_example = Chart(
        defer=DashboardData.fetch_stacked_bar_chart_data, width=4
    )
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
            "sub_text": kwargs.get("filters", {}).get("country", "all"),
        }
    )
    stat_one = Stat(value={"text": "100%", "sub_text": "increase"})
    stat_two = Stat(value={"text": "88%", "sub_text": "increase"})
    free_text_example = Text(defer=DashboardData.fetch_html, mark_safe=True)
    gauge_one = Chart(defer=DashboardData.fetch_gauge_chart_data)
    gauge_two = Chart(defer=DashboardData.fetch_gauge_chart_data_two)
    table_example = Table(
        page_size=5,
        columns=[
            {"data": "id", "title": "ID"},
            {"data": "name", "title": "Name"},
            {"data": "progress", "title": "Progress"},
            {"data": "gender", "title": "Gender"},
            {"data": "dob", "title": "DOB"},
        ],
        defer=DashboardData.fetch_table_data,
    )
    table_example_not_deferred = Table(
        page_size=1,
        columns=[
            {"data": "id", "title": "ID"},
            {"data": "name", "title": "Name"},
            {"data": "progress", "title": "Progress"},
            {"data": "gender", "title": "Gender"},
            {"data": "dob", "title": "DOB"},
        ],
        value=TableData(
            data=[
                {
                    "id": 1,
                    "name": "Oli Bob",
                    "progress": 12,
                    "gender": "male",
                    "rating": 1,
                    "col": "red",
                    "dob": "19/02/1984",
                    "car": 1,
                },
                {
                    "id": 2,
                    "name": "Bob Oli",
                    "progress": 2,
                    "gender": "male",
                    "rating": 5,
                    "col": "blue",
                    "dob": "21/04/1995",
                    "car": 0,
                },
            ],
            paging=TablePaging(page_size=1, page=1, page_count=2),
        ),
    )
    scatter_map_example = Map(defer=DashboardData.fetch_scatter_map_data)
    choropleth_map_example = Map(defer=DashboardData.fetch_choropleth_map_data)

    class Meta:
        name = "Basic"


class DemoDashboardOneCustom(DemoDashboardOne):
    template_name = "demo/custom.html"

    class Meta:
        name = "Custom Template"


class DemoDashboardOneVary(DemoDashboardOne):
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data, width=12)
    calculated_example = Text(defer=lambda **kwargs: "some calculated text", width=3)
    table_example = Table(defer=DashboardData.fetch_table_data, width=12)

    class Meta:
        name = "With Layout"

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
        name = "Admin Only"


class SSEDashboard(Dashboard):
    """
    Example of dashboard with Server send events, see README for more details.
    """

    standard_stat = Stat(
        defer=lambda *args, **kwargs: {
            "text": f"{randint(1, 100)}%",
            "sub_text": "Via poll",
        },
        poll_rate=3,
    )
    sse_stat = SSEStat()
    standard_chart = Chart(defer=DashboardData.fetch_sse_chart_data, poll_rate=None)
    sse_chart = SSEChart(defer=DashboardData.fetch_sse_chart_data)

    class Meta:
        name = "SSE Example"


# register the dashboards
registry.register(DemoDashboardOne)
registry.register(DemoDashboardOneCustom)
registry.register(DemoDashboardOneVary)
registry.register(DemoDashboardAdmin)
registry.register(SSEDashboard)

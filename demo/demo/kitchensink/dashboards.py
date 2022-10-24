from random import randint

from django.http import HttpRequest
from django.urls import reverse, reverse_lazy

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
from datorum.component.text import CTAData, StatData
from datorum.dashboard import Dashboard
from datorum.permissions import IsAdminUser
from datorum.registry import registry
from plotly.io._orca import psutil

from demo.kitchensink.components import SharedComponent, SSEChart, SSEStat
from demo.kitchensink.data import DashboardData
from demo.kitchensink.forms import AnimalForm, ExampleForm

from faker import Faker

fake = Faker()


class DemoDashboard(Dashboard):
    link = CTA(
        value=CTAData(
            href=reverse_lazy(
                "datorum:dashboards:kitchensink_demodashboardcustomtemplate"
            ),
            text="Find out more!",
        ),
        width=3,
    )
    text_example = Text(
        value="Rendered on load",
        width=3,
    )
    html_example = Text(
        value="<strong>HTML also rendered on load</strong>", mark_safe=True, width=3
    )
    calculated_example = Text(defer=lambda **kwargs: "Deferred text", width=3)
    form_example = Form(
        form=AnimalForm,
        method="get",
        dependents=["chart_example", "stacked_chart_example", "stat_three"],
        width=3,
    )
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data, width=3)
    stacked_chart_example = Chart(
        defer=DashboardData.fetch_stacked_bar_chart_data, width=3, poll_rate=5
    )
    bubble_chart_example = Chart(defer=DashboardData.fetch_bubble_chart_data, width=3)
    filter_form = Form(
        form=ExampleForm,
        method="get",
        dependents=["line_chart_example", "stat_three"],
        width=3,
    )
    line_chart_example = Chart(defer=DashboardData.fetch_scatter_chart_data, width=9)
    stat_one = Stat(value={"text": "100%", "sub_text": "increase"}, width=4)
    stat_two = Stat(value={"text": "88%", "sub_text": "increase"}, width=4)
    stat_three = Stat(
        defer=lambda **kwargs: {
            "text": "33%",
            "sub_text": kwargs.get("filters", {}).get("country", "all"),
        },
        width=4,
    )
    gauge_one = Chart(defer=DashboardData.fetch_gauge_chart_data)
    gauge_two = Chart(defer=DashboardData.fetch_gauge_chart_data_two)
    free_text_example = Text(defer=DashboardData.fetch_html, mark_safe=True, width=12)
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


class DemoDashboardCustomTemplate(DemoDashboard):
    class Meta:
        name = "Custom Template"
        template_name = "demo/custom.html"


class DemoDashboardWithLayout(DemoDashboard):
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
            Card("text_example", "html_example", width=3),
            Card(
                Div("stat_one"),
                Div("stat_two"),
                Div("stat_three"),
                width=9,
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


class AdminDashboard(Dashboard):
    admin_text = Text(value="Admin Only Text")
    scatter_map_example = Map(defer=DashboardData.fetch_scatter_map_data)
    choropleth_map_example = Map(defer=DashboardData.fetch_choropleth_map_data)

    class Meta:
        name = "Admin Only"
        permission_classes = [IsAdminUser]


class DynamicDashboard(Dashboard):
    """
    Example of a dashboard which leverages init to create components and share calculations
    between components for performance.
    """

    def __init__(self, request: HttpRequest, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)

        # Generated components
        for r in range(1, 3):
            self.components[f"dynamic_component_{r}"] = Text(
                value=f"Rendered Dynamically via __init__: {r}", width=6
            )

        # Components with shared seed data
        hdd = psutil.disk_usage("/")
        self.components["total_disk"] = Stat(
            value=StatData(
                text=str(round(hdd.total / (2**30))), sub_text="Total disk size GiB"
            )
        )
        self.components["used_disk"] = Stat(
            value=StatData(
                text=str(round(hdd.used / (2**30))), sub_text="Used disk size GiB"
            )
        )
        self.components["free_disk"] = Stat(
            value=StatData(
                text=str(round(hdd.free / (2**30))), sub_text="Free disk size GiB"
            )
        )

        # Component which is deferred, note however, each defer function is partially loaded so init
        # would be called again for that component, which is worth considering in any code added here.
        self.components["defer_also_works"] = Text(
            defer=lambda **k: "Deferred via init"
        )

        # Apply a change such as width or css to already defined components
        change_width_for = ["width_test_one", "width_test_two"]
        for component in change_width_for:
            self.components[component].width = 3
            self.components[component].css_classes = "dynamic"

        # drop a component depending on user
        if request.user.is_staff:
            self.components["component_only_for_admin"] = Text(
                value="Only for admin users"
            )

        # change the layout
        layout = request.GET.get("layout")
        if layout == "div":
            self.components["layout_swap"] = CTA(
                value=CTAData(
                    href=self.get_absolute_url() + f"?layout=card",
                    text="Swap back to Cards",
                )
            )
            self.Layout.components = ComponentLayout(
                *[Div(k, width=3) for k, c in self.components.items()]
            )
        else:
            self.components["layout_swap"] = CTA(
                value=CTAData(
                    href=self.get_absolute_url() + f"?layout=div",
                    text="Swap to Fixed Divs",
                )
            )
            self.Layout.components = None

        # Reorder fields
        self.components = {
            k: v for k, v in sorted(self.components.items(), key=lambda c: c[1].width)
        }

    standard_field = Text(value=f"Standard field", width=6)
    width_test_one = Text(value="Width Changed 1")
    width_test_two = Text(value="Width Changed 2")
    value_from_method = Text(width=6)
    defer_from_method = Text(width=6)
    stat_shared = SharedComponent()

    def get_value_from_method_value(self, **kwargs):
        return f"I am defined as a FOO value."

    def get_defer_from_method_defer(self, **kwargs):
        request = kwargs["request"]
        return f"hello {request.user} I am defined as a FOO defer."

    class Meta:
        name = "Dynamic Example"


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
    standard_chart = Chart(defer=DashboardData.fetch_sse_chart_data)
    sse_chart = SSEChart(defer=DashboardData.fetch_sse_chart_data, poll_rate=10)

    class Meta:
        name = "SSE Example"


class CustomComponentDashboard(Dashboard):
    """
    Example of dashboard with components that use a different defer fetching url.

    For the async example, while this will run with runserver, use daphne
    for production or to see the demo working fully

        daphne demo.asgi:application

    """

    # Simplistic example which calls it's own view, which in this case just
    # subclassed ComponentView for a simple response, i.e value/defer is not used.
    custom_response = Text(
        defer_url=lambda reverse_kwargs: reverse(
            "kitchensink:custom-component", kwargs=reverse_kwargs
        ),
    )

    # Simplistic example which calls it's own view, but refers back to defer via the
    # component.
    custom_response_defer = Text(
        defer=lambda **kwargs: "Simple Response Via Defer",
        defer_url=lambda reverse_kwargs: reverse(
            "kitchensink:custom-component-defer", kwargs=reverse_kwargs
        ),
    )

    # Example in which third party is called via sync.
    sync_httpbin = Text(
        defer_url=lambda reverse_kwargs: reverse(
            "kitchensink:sync-component", kwargs=reverse_kwargs
        ),
    )

    # Example in which third party is called via async.
    async_httpbin = Text(
        defer_url=lambda reverse_kwargs: reverse(
            "kitchensink:async-component", kwargs=reverse_kwargs
        ),
    )

    class Meta:
        name = "Custom Component Fetch"


# register the dashboards
registry.register(DemoDashboard)
registry.register(DemoDashboardCustomTemplate)
registry.register(DemoDashboardWithLayout)
registry.register(AdminDashboard)
registry.register(DynamicDashboard)
registry.register(SSEDashboard)
registry.register(CustomComponentDashboard)

from enum import Enum
from random import randint

from django.http import HttpRequest
from django.urls import reverse, reverse_lazy

import psutil
from demo.kitchensink.charts import (
    ExampleBubbleChartSerializer,
    ExampleChartSerializer,
    ExampleGaugeChartSerializer,
    ExampleMapSerializer,
    ExampleStackedChartSerializer,
)
from demo.kitchensink.components import (
    Gauge,
    GaugeData,
    SharedComponent,
    SSEChart,
    SSEStat,
)
from demo.kitchensink.data import DashboardData, UsersThisWeek
from demo.kitchensink.forms import MedalForm
from demo.kitchensink.tables import ExampleTableSerializer
from faker import Faker

from dashboards import config
from dashboards.component import CTA, BasicTable, Chart, Form, Map, Stat, Table, Text
from dashboards.component.layout import (
    HR,
    HTML,
    Card,
    ComponentLayout,
    Div,
    Header,
    Tab,
    TabContainer,
)
from dashboards.component.text import StatData
from dashboards.dashboard import Dashboard
from dashboards.permissions import IsAdminUser
from dashboards.registry import registry


class Grid(Enum):
    """define css classes here for grid layout"""

    DEFAULT = config.Config().DASHBOARDS_DEFAULT_GRID_CSS
    ONE = "span-12"
    DOUBLE = "span-9"
    TWO = "span-6"
    THREE = "span-4"
    FOUR = "span-3"
    FIVE = "span-2"


fake = Faker()


class DemoDashboard(Dashboard):
    link = Text(
        value="Find out more!",
        cta=CTA(
            href=reverse_lazy("dashboards:kitchensink_demodashboardcustomtemplate"),
        ),
        grid_css_classes=Grid.TWO.value,
    )
    text_example = Text(
        value="Rendered on load",
        grid_css_classes=Grid.TWO.value,
        template_name="demo/one.html",
    )
    html_example = Text(
        value="<strong>HTML also rendered on load</strong>",
        mark_safe=True,
        grid_css_classes=Grid.THREE.value,
    )
    calculated_example = Text(
        defer=lambda **kwargs: "Deferred text",
        grid_css_classes=Grid.THREE.value,
        trigger_on="click",
    )
    form_example = Form(
        form=MedalForm,
        method="get",
        dependents=["chart_example", "stacked_chart_example"],
        grid_css_classes=Grid.THREE.value,
    )
    chart_example = Chart(
        value=ExampleChartSerializer,
        grid_css_classes=Grid.TWO.value,
    )
    stacked_chart_example = Chart(
        defer=ExampleStackedChartSerializer,
        grid_css_classes=Grid.TWO.value,
    )
    bubble_chart_example = Chart(
        defer=ExampleBubbleChartSerializer,
        grid_css_classes=Grid.ONE.value,
    )
    stat_one = Stat(
        defer=UsersThisWeek,
        icon="<i data-feather='users'></i>",
        grid_css_classes=Grid.TWO.value,
    )
    stat_two = Stat(
        value=StatData(text="88%", sub_text="decrease", change_by_text="12%"),
        icon="<i data-feather='users'></i>",
        grid_css_classes=Grid.TWO.value,
    )
    gauge_one = Chart(
        defer=ExampleGaugeChartSerializer,
        poll_rate=5,
        grid_css_classes=Grid.TWO.value,
    )
    gauge_svg = Gauge(
        value=GaugeData(
            title="SVG Gauge",
            value=55,
        ),
        grid_css_classes=Grid.TWO.value,
    )
    free_text_example = Text(
        defer=DashboardData.fetch_html, mark_safe=True, grid_css_classes=Grid.ONE.value
    )
    table_example = Table(
        page_size=5,
        value=ExampleTableSerializer,
        grid_css_classes=Grid.TWO.value,
    )
    table_example_not_deferred = BasicTable(
        value=ExampleTableSerializer,
        grid_css_classes=Grid.TWO.value,
    )
    scatter_map_example = Map(
        defer=DashboardData.fetch_scatter_map_data, grid_css_classes=Grid.TWO.value
    )
    choropleth_map_example = Map(
        defer=ExampleMapSerializer, grid_css_classes=Grid.TWO.value
    )

    class Meta:
        name = "Basic"


class DemoDashboardCustomTemplate(DemoDashboard):
    class Meta:
        name = "Custom Template"
        template_name = "demo/custom.html"


class DemoDashboardWithLayout(DemoDashboard):
    calculated_example = Text(
        defer=lambda **kwargs: "some calculated text", grid_css_classes=Grid.THREE.value
    )
    table_example = Table(defer=ExampleTableSerializer, grid_css_classes=Grid.ONE.value)

    class Meta:
        name = "With Layout"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            Header(heading="Header", size=1),
            HTML(
                "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec vestibulum orci. Sed ac eleifend "
                "diam. Duis quis congue ex. Mauris at bibendum est, nec bibendum ipsum. Lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit.</p>",
            ),
            Card("text_example", "html_example", grid_css_classes=Grid.TWO.value),
            Card(
                Div("stat_one"),
                Div("stat_two"),
                Div("stat_three"),
                heading="Grouped Stats",
                footer="footer text",
                grid_css_classes=Grid.TWO.value,
            ),
            HR(),
            Header(heading="Tab Example", size=3),
            HTML(
                "<p>Like other deferred components, we only render what is in view, so other tabs only load on click."
            ),
            TabContainer(
                Tab(
                    "Calculated Example",
                    Card("calculated_example"),
                    Card("chart_example"),
                    grid_css_classes=Grid.ONE.value,
                ),
                Tab(
                    "Table Example",
                    Card("table_example"),
                    Card("gauge_two"),
                    grid_css_classes=Grid.ONE.value,
                ),
                grid_css_classes=Grid.ONE.value,
            ),
        )


class AdminDashboard(Dashboard):
    admin_text = Text(value="Admin Only Text")
    scatter_map_example = Map(defer=DashboardData.fetch_scatter_map_data)
    choropleth_map_example = Map(defer=ExampleMapSerializer)

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
                value=f"Rendered Dynamically via __init__: {r}",
                grid_css_classes=Grid.TWO.value,
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
            self.components[component].grid_css_classes = Grid.ONE.value
            self.components[component].css_classes = "dynamic"

        # drop a component depending on user
        if request.user.is_staff:
            self.components["component_only_for_admin"] = Text(
                value="Only for admin users"
            )

        # change the layout
        layout = request.GET.get("layout")
        if layout == "div":
            self.components["layout_swap"] = Text(
                value="Swap back to Cards",
                cta=CTA(
                    href=self.get_absolute_url() + "?layout=card",
                ),
            )
            self.Layout.components = ComponentLayout(
                *[
                    Div(k, grid_css_classes=Grid.THREE.value)
                    for k, c in self.components.items()
                ]
            )
        else:
            self.components["layout_swap"] = Text(
                value="Swap to Fixed Divs",
                cta=CTA(
                    href=self.get_absolute_url() + "?layout=div",
                ),
            )
            self.Layout.components = None

    standard_field = Text(value="Standard field", grid_css_classes=Grid.TWO.value)
    width_test_one = Text(value="Width Changed 1")
    width_test_two = Text(value="Width Changed 2")
    value_from_method = Text(grid_css_classes=Grid.TWO.value)
    defer_from_method = Text(grid_css_classes=Grid.TWO.value)
    stat_shared = SharedComponent()

    def get_value_from_method_value(self, **kwargs):
        return "I am defined as a FOO value."

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
        grid_css_classes="span-6",
    )
    sse_stat = SSEStat(grid_css_classes="span-6")
    standard_chart = Chart(
        defer=DashboardData.fetch_sse_chart_data, grid_css_classes="span-6"
    )
    sse_chart = SSEChart(
        defer=DashboardData.fetch_sse_chart_data,
        poll_rate=10,
        grid_css_classes="span-6",
    )

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
        defer_url=lambda reverse_args: reverse(
            "kitchensink:custom-component", args=reverse_args
        ),
        grid_css_classes=Grid.TWO.value,
    )

    # Simplistic example which calls it's own view, but refers back to defer via the
    # component.
    custom_response_defer = Text(
        defer=lambda **kwargs: "Simple Response Via Defer",
        defer_url=lambda reverse_args: reverse(
            "kitchensink:custom-component-defer", args=reverse_args
        ),
        grid_css_classes=Grid.TWO.value,
    )

    # Example in which third party is called via sync.
    sync_httpbin = Text(
        defer_url=lambda reverse_args: reverse(
            "kitchensink:sync-component", args=reverse_args
        ),
        grid_css_classes=Grid.TWO.value,
    )

    # Example in which third party is called via async.
    async_httpbin = Text(
        defer_url=lambda reverse_args: reverse(
            "kitchensink:async-component", args=reverse_args
        ),
        grid_css_classes=Grid.TWO.value,
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

from datorum.component import CTA, Chart, Form, Map, Stat, Table, Text
from datorum.component.table import TableData
from datorum.dashboard import Dashboard
from datorum.layout import HTML, HR, Card, Div, Header, LayoutComponent, Tab, TabContainer
from datorum.permissions import IsAdminUser
from django.urls import reverse_lazy

from demo.demo_app.data import DashboardData
from demo.demo_app.forms import AnimalForm, ExampleForm
from demo.demo_app.style import H1


class DemoDashboardOne(Dashboard):
    link = CTA(
        href=reverse_lazy("datorum:dashboards:demodashboardonecustom_dashboard"),
        text="Find out more!",
    )
    text_example = Text(
        value="<p>Rendered on load</p>",
        cta=CTA(
            href=reverse_lazy("datorum:dashboards:demodashboardonecustom_dashboard"),
            text="Find out more!",
        ),
        css_classes=[H1],
        mark_safe=True,
    )
    html_example = Text(value="<strong>HTML also rendered on load</strong>", mark_safe=True)
    calculated_example = Text(defer=lambda _: "Deferred text")
    form_example = Form(
        form=AnimalForm,
        method="get",
        dependents=["chart_example", "stacked_chart_example"],
    )
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data)
    stacked_chart_example = Chart(defer=DashboardData.fetch_stacked_bar_chart_data)
    bubble_chart_example = Chart(defer=DashboardData.fetch_bubble_chart_data)
    line_chart_example = Chart(
        defer=DashboardData.fetch_scatter_chart_data,
        filter_form=ExampleForm,
        dependents=["stat_three"],
    )
    stat_one = Stat(value={"text": "100%", "sub_text": "increase"})
    stat_two = Stat(value={"text": "88%", "sub_text": "increase"})
    stat_three = Stat(
        defer=lambda request: {
            "text": "33%",
            "sub_text": request.GET.get("country", "all"),
        }
    )
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


class DemoDashboardOneDiv(DemoDashboardOne):
    template_name = "demo/div.html"


class DemoDashboardOneCustom(DemoDashboardOne):
    template_name = "demo/custom.html"


class DemoDashboardOneVary(DemoDashboardOne):
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data, width=12)
    calculated_example = Text(defer=lambda _: "some calculated text", width=3)
    table_example = Table(defer=DashboardData.fetch_table_data, width=12)

    class Meta:
        name = "Dashboard One Vary"

    class Layout(Dashboard.Layout):
        components = LayoutComponent(
            Header("Header", size=2),
            HTML(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec vestibulum orci. Sed ac eleifend diam. Duis quis congue ex. Mauris at bibendum est, nec bibendum ipsum. Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            ),
            Card(
                "text_example",
                "html_example",
                element_id="text_group_div",
            ),
            Div(
                Div("stat_one", element_id="stat_group_div", css_class_names="span-4"),
                Div("stat_two", element_id="stat_group_div", css_class_names="span-4"),
                Div(
                    "stat_three", element_id="stat_group_div", css_class_names="span-4"
                ),
                element_id="stat_group_div",
                css_class_names="dashboard-container",
            ),
            HR(),
            Header("Tab Example", size=3),
            TabContainer(
                Tab(
                    "Calculated Example",
                    "calculated_example",
                    element_id="tab1",
                ),
                Tab(
                    "Chart Example",
                    "chart_example",
                    element_id="tab2",
                ),
                Tab(
                    "Table Example",
                    "table_example",
                    element_id="tab3",
                ),
                Tab(
                    "Gauge Example",
                    "gauge_two",
                    element_id="tab4",
                ),
                element_id="tabs",
            ),
        )


class DemoDashboardAdmin(Dashboard):
    permission_classes = [IsAdminUser]
    admin_text = Text(value="Admin Only Text")
    scatter_map_example = Map(defer=DashboardData.fetch_scatter_map_data)
    choropleth_map_example = Map(defer=DashboardData.fetch_choropleth_map_data)

    class Meta:
        name = "Admin Dashboard"


class DemoDashboardGridTemplate(Dashboard):
    template_name = "demo/custom_grid.html"

    text_example = Text(
        value="Rendered on load",
        cta=CTA(
            href=reverse_lazy("datorum:dashboards:demodashboardonecustom_dashboard"),
            text="Find out more!",
        ),
    )
    html_example = Text(value="<strong>HTML also rendered on load</strong>", mark_safe=True)
    calculated_example = Text(defer=lambda _: "Deferred text")
    chart_example = Chart(defer=DashboardData.fetch_bar_chart_data)
    stacked_chart_example = Chart(defer=DashboardData.fetch_stacked_bar_chart_data)
    bubble_chart_example = Chart(defer=DashboardData.fetch_bubble_chart_data)

    class Meta:
        name = "Grid Template"

from datorum.component import HTML, Plotly, Stat, Table, Text
from datorum.dashboard import Dashboard
from datorum.permissions import IsAdminUser

from demo.demo_app.data import DashboardData
from demo.demo_app.forms import ExampleForm


class DemoDashboardOne(Dashboard):
    text_example = Text(value="Rendered on load")
    html_example = HTML(value="<strong>HTML also rendered on load</strong>")
    calculated_example = Text(defer=lambda _: "Deferred text")
    chart_example = Plotly(defer=DashboardData.fetch_bar_chart_data)
    bubble_chart_example = Plotly(defer=DashboardData.fetch_bubble_chart_data)
    line_chart_example = Plotly(
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
    free_text_example = HTML(defer=DashboardData.fetch_html)
    gauge_one = Plotly(defer=DashboardData.fetch_gauge_chart_data)
    gauge_two = Plotly(defer=DashboardData.fetch_gauge_chart_data_two)
    table_example = Table(defer=DashboardData.fetch_table_data)
    table_example_not_deferred = Table(
        value=[
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
        ]
    )

    class Meta:
        name = "Dashboard One"


class DemoDashboardOneVary(DemoDashboardOne):
    chart_example = Plotly(defer=DashboardData.fetch_bar_chart_data, width=12)
    calculated_example = Text(defer=lambda _: "some calculated text", width=3)
    table_example = Table(defer=DashboardData.fetch_table_data, width=12)

    class Meta:
        name = "Dashboard One Vary"

    class Layout(Dashboard.Layout):
        grid_default_width = 4
        components = {
            "text_group": {
                "components": ["text_example", "html_example"],
                "component_widths": [3, 6],
                "group_width": 6,
            },
            "stat_group": {
                "components": ["stat_one", "stat_two", "stat_three"],
                "group_width": 3,
            },
            # "chart_group": {
            #     "components": ["bubble_chart_example", "line_chart_example"],
            #     "group_width": 12,
            # },
            # None can be uses as a catch all for the remaining non grouped ones at the end
            None: {
                "components": [
                    "calculated_example",
                    "chart_example",
                    "table_example",
                    "gauge_two",
                ],
            },
        }


class DemoDashboardAdmin(Dashboard):
    permission_classes = [IsAdminUser]
    admin_text = Text(value="Admin Only Text")

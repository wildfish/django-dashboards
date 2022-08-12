from datorum.component import HTML, Plotly, Stat, Tabulator, Text
from datorum.dashboard import Dashboard

from demo.demo_app.data import DashboardData


class DemoDashboardOne(Dashboard):
    text_example = Text(value="Rendered on load")
    html_example = HTML(value="<strong>HTML also rendered on load</strong>")
    calculated_example = Text(defer=lambda _: "Deferred text")
    chart_example = Plotly(defer=DashboardData.fetch_bar_chart_data)
    stat_one = Stat(value={"text": "100%", "sub_text": "increase"})
    stat_two = Stat(value={"text": "88%", "sub_text": "increase"})
    stat_three = Stat(value={"text": "33%", "sub_text": "decrease"})
    free_text_example = HTML(defer=DashboardData.fetch_html)
    gauge_one = Plotly(defer=DashboardData.fetch_gauge_chart_data)
    gauge_two = Plotly(defer=DashboardData.fetch_gauge_chart_data_two)
    table_example = Tabulator(defer=DashboardData.fetch_table_data)
    table_example_not_deferred = Tabulator(
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
    table_example = Tabulator(defer=DashboardData.fetch_table_data, width=12)

    class Meta:
        name = "Dashboard One Vary"

    class Layout(Dashboard.Layout):
        grid_default_width = 3
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

import json

import plotly.express as px
from demo.kitchensink.models import FlatText


class DashboardData:
    def _apply_filter_age_range(self):
        pass

    @staticmethod
    def fetch_html(*args, **kwargs) -> str:
        return getattr(FlatText.objects.all().first(), "text", "")

    @staticmethod
    def fetch_gauge_chart_data(*args, **kwargs) -> str:
        return json.dumps(
            dict(
                data=[
                    dict(
                        domain={"x": [0, 1], "y": [0, 1]},
                        value=2700,
                        title={"text": "Average RPM"},
                        mode="gauge+number",
                        type="indicator",
                    )
                ]
            )
        )

    @staticmethod
    def fetch_gauge_chart_data_two(*args, **kwargs) -> str:
        return json.dumps(
            dict(
                data=[
                    dict(
                        domain={"x": [0, 1], "y": [0, 1]},
                        value=45,
                        title={"text": "MPG"},
                        mode="gauge+number+delta",
                        type="indicator",
                        delta={"reference": 38},
                        gauge={
                            "axis": {"range": [None, 50]},
                            "steps": [
                                {"range": [0, 25], "color": "lightgray"},
                                {"range": [25, 40], "color": "gray"},
                            ],
                            "threshold": {
                                "line": {"color": "red", "width": 4},
                                "thickness": 0.75,
                                "value": 49,
                            },
                        },
                    )
                ]
            )
        )

    @staticmethod
    def fetch_bar_chart_data(request, **kwargs) -> str:
        data = {"giraffes": 20, "orangutans": 14, "monkeys": 23}
        filters = kwargs.get("filters") or {}
        if "animal" in filters and filters["animal"] in data:
            animal = filters["animal"]
            data = {animal: data[animal]}

        return json.dumps(
            dict(
                data=[
                    dict(
                        x=list(data.keys()),
                        y=list(data.values()),
                        type="bar",
                    )
                ]
            )
        )

    @staticmethod
    def fetch_stacked_bar_chart_data(request, **kwargs) -> str:
        sf_data = {"giraffes": 20, "orangutans": 14, "monkeys": 23}
        la_data = {"giraffes": 12, "orangutans": 18, "monkeys": 29}
        filters = kwargs.get("filters") or {}
        if "animal" in filters:
            animal = filters["animal"]
            sf_data = {animal: sf_data[animal]} if animal in sf_data else sf_data
            la_data = {animal: la_data[animal]} if animal in la_data else la_data

        return json.dumps(
            dict(
                data=[
                    dict(
                        x=list(sf_data.keys()),
                        y=list(sf_data.values()),
                        name="SF Zoo",
                        type="bar",
                    ),
                    dict(
                        x=list(la_data.keys()),
                        y=list(la_data.values()),
                        name="LA Zoo",
                        type="bar",
                    ),
                ],
                layout={"barmode": "stack"},
            )
        )

    @staticmethod
    def fetch_bubble_chart_data(*args, **kwargs) -> str:
        return json.dumps(
            dict(
                data=[
                    dict(
                        x=[1, 2, 3, 4],
                        y=[10, 11, 12, 13],
                        mode="markers",
                        marker={"size": [40, 60, 80, 100]},
                    )
                ]
            )
        )

    @staticmethod
    def fetch_scatter_chart_data(request, **kwargs) -> str:
        na = dict(
            x=[52698, 43117],
            y=[53, 31],
            mode="markers",
            name="North America",
            text=["United States", "Canada"],
            marker={
                "color": "rgb(164, 194, 244)",
                "size": 12,
                "line": {"color": "white", "width": 0.5},
            },
            type="scatter",
        )

        europe = dict(
            x=[39317, 37236, 35650, 30066, 29570, 27159, 23557, 21046, 18007],
            y=[33, 20, 13, 19, 27, 19, 49, 44, 38],
            mode="markers",
            name="Europe",
            text=[
                "Germany",
                "Britain",
                "France",
                "Spain",
                "Italy",
                "Czech Rep.",
                "Greece",
                "Poland",
            ],
            marker={"color": "rgb(255, 217, 102)", "size": 12},
            type="scatter",
        )

        asia = dict(
            x=[42952, 37037, 33106, 17478, 9813, 5253, 4692, 3899],
            y=[23, 42, 54, 89, 14, 99, 93, 70],
            mode="markers",
            name="Asia/Pacific",
            text=[
                "Australia",
                "Japan",
                "South Korea",
                "Malaysia",
                "China",
                "Indonesia",
                "Philippines",
                "India",
            ],
            marker={"color": "rgb(234, 153, 153)", "size": 12},
            type="scatter",
        )

        # Very noddy example of filtering, should and could validate against the form class itself :)
        filters = kwargs.get("filters") or {}
        filter_country = filters.get("country")
        if filter_country and filter_country != "all":
            return json.dumps(
                dict(
                    data={"na": [na], "europe": [europe], "asia": [asia]}[
                        filter_country
                    ]
                )
            )

        return json.dumps(dict(data=[na, europe, asia]))

    @staticmethod
    def fetch_scatter_map_data(*args, **kwargs) -> str:
        return json.dumps(
            dict(
                data=[
                    dict(
                        lat=[40.7127, 51.5072],
                        lon=[-74.0059, 0.1275],
                        mode="lines",
                        type="scattergeo",
                        line={"width": 2, "color": "blue"},
                    )
                ],
                layout=dict(
                    title="London to NYC Great Circle",
                    showlegend=False,
                    geo={
                        "resolution": 50,
                        "showland": True,
                        "showlakes": True,
                        "landcolor": "rgb(204, 204, 204)",
                        "countrycolor": "rgb(204, 204, 204)",
                        "lakecolor": "rgb(255, 255, 255)",
                        "projection": {"type": "equirectangular"},
                        "coastlinewidth": 2,
                        "lataxis": {
                            "range": [20, 60],
                            "showgrid": True,
                            "tickmode": "linear",
                            "dtick": 10,
                        },
                        "lonaxis": {
                            "range": [-100, 20],
                            "showgrid": True,
                            "tickmode": "linear",
                            "dtick": 20,
                        },
                    },
                ),
            )
        )

    @staticmethod
    def fetch_choropleth_map_data(*args, **kwargs) -> str:
        fig = px.choropleth(
            locations=["CA", "TX", "NY"],
            locationmode="USA-states",
            color=[1, 2, 3],
            scope="usa",
        )
        return fig.to_json()

    @staticmethod
    def fetch_sse_chart_data(*args, **kwargs) -> str:
        return json.dumps(
            dict(
                data=[
                    dict(
                        y=list([1, 2, 3]),
                        type="scatter",
                        mode="lines",
                    )
                ]
            )
        )

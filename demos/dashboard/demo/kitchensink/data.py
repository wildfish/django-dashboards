import csv

import requests
from demo.kitchensink.models import FlatText

from datorum.dashboards.component.chart import ChartData
from datorum.dashboards.component.map import MapData
from datorum.dashboards.component.table import (
    DatatablesFilter,
    DatatablesSort,
    ReactTablesSort,
    TableData,
    ToTable,
)


class DashboardData:
    def _apply_filter_age_range(self):
        pass

    @staticmethod
    def fetch_html(*args, **kwargs) -> str:
        return FlatText.objects.all().first().text

    @staticmethod
    def fetch_gauge_chart_data(*args, **kwargs) -> ChartData:
        return ChartData(
            data=[
                ChartData.Gauge(
                    domain={"x": [0, 1], "y": [0, 1]},
                    value=2700,
                    title={"text": "Average RPM"},
                    mode=ChartData.Gauge.Mode.STANDARD,
                )
            ]
        )

    @staticmethod
    def fetch_gauge_chart_data_two(*args, **kwargs) -> ChartData:
        return ChartData(
            data=[
                ChartData.Gauge(
                    domain={"x": [0, 1], "y": [0, 1]},
                    value=45,
                    title={"text": "MPG"},
                    mode=ChartData.Gauge.Mode.DELTA,
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

    @staticmethod
    def fetch_bar_chart_data(request, **kwargs) -> ChartData:
        data = {"giraffes": 20, "orangutans": 14, "monkeys": 23}
        filters = kwargs.get("filters") or {}
        if "animal" in filters and filters["animal"] in data:
            animal = filters["animal"]
            data = {animal: data[animal]}

        return ChartData(
            data=[
                ChartData.Trace(
                    x=list(data.keys()),
                    y=list(data.values()),
                    type=ChartData.Trace.Type.BAR,
                )
            ]
        )

    @staticmethod
    def fetch_stacked_bar_chart_data(request, **kwargs) -> ChartData:
        sf_data = {"giraffes": 20, "orangutans": 14, "monkeys": 23}
        la_data = {"giraffes": 12, "orangutans": 18, "monkeys": 29}
        filters = kwargs.get("filters") or {}
        if "animal" in filters:
            animal = filters["animal"]
            sf_data = {animal: sf_data[animal]} if animal in sf_data else sf_data
            la_data = {animal: la_data[animal]} if animal in la_data else la_data

        return ChartData(
            data=[
                ChartData.Trace(
                    x=list(sf_data.keys()),
                    y=list(sf_data.values()),
                    name="SF Zoo",
                    type=ChartData.Trace.Type.BAR,
                ),
                ChartData.Trace(
                    x=list(la_data.keys()),
                    y=list(la_data.values()),
                    name="LA Zoo",
                    type=ChartData.Trace.Type.BAR,
                ),
            ],
            layout={"barmode": "stack"},
        )

    @staticmethod
    def fetch_bubble_chart_data(*args, **kwargs) -> ChartData:
        return ChartData(
            data=[
                ChartData.Trace(
                    x=[1, 2, 3, 4],
                    y=[10, 11, 12, 13],
                    mode=ChartData.Trace.Mode.SCATTER,
                    marker={"size": [40, 60, 80, 100]},
                )
            ]
        )

    @staticmethod
    def fetch_scatter_chart_data(request, **kwargs) -> ChartData:
        na = ChartData.Trace(
            x=[52698, 43117],
            y=[53, 31],
            mode=ChartData.Trace.Mode.SCATTER,
            name="North America",
            text=["United States", "Canada"],
            marker={
                "color": "rgb(164, 194, 244)",
                "size": 12,
                "line": {"color": "white", "width": 0.5},
            },
            type=ChartData.Trace.Type.SCATTER,
        )

        europe = ChartData.Trace(
            x=[39317, 37236, 35650, 30066, 29570, 27159, 23557, 21046, 18007],
            y=[33, 20, 13, 19, 27, 19, 49, 44, 38],
            mode=ChartData.Trace.Mode.SCATTER,
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
            type=ChartData.Trace.Type.SCATTER,
        )

        asia = ChartData.Trace(
            x=[42952, 37037, 33106, 17478, 9813, 5253, 4692, 3899],
            y=[23, 42, 54, 89, 14, 99, 93, 70],
            mode=ChartData.Trace.Mode.SCATTER,
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
            type=ChartData.Trace.Type.SCATTER,
        )

        # Very noddy example of filtering, should and could validate against the form class itself :)
        filters = kwargs.get("filters") or {}
        filter_country = filters.get("country")
        if filter_country and filter_country != "all":
            return ChartData(
                data={"na": [na], "europe": [europe], "asia": [asia]}[filter_country]
            )

        return ChartData(data=[na, europe, asia])

    @staticmethod
    def fetch_table_data(*args, **kwargs) -> TableData:
        """
        Mock return some results for tabular.
        """
        data = [
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
                "name": "Mary May",
                "progress": 1,
                "gender": "female",
                "rating": 2,
                "col": "blue",
                "dob": "14/05/1982",
                "car": True,
            },
            {
                "id": 3,
                "name": "Christine Lobowski",
                "progress": 42,
                "gender": "female",
                "rating": 0,
                "col": "green",
                "dob": "22/05/1982",
                "car": "true",
            },
            {
                "id": 4,
                "name": "Brendon Philips",
                "progress": 100,
                "gender": "male",
                "rating": 1,
                "col": "orange",
                "dob": "01/08/1980",
            },
            {
                "id": 5,
                "name": "Margret Marmajuke",
                "progress": 16,
                "gender": "female",
                "rating": 5,
                "col": "yellow",
                "dob": "31/01/1999",
            },
            {
                "id": 6,
                "name": "Frank Harbours",
                "progress": 38,
                "gender": "male",
                "rating": 4,
                "col": "red",
                "dob": "12/05/1966",
                "car": 1,
            },
        ]

        # data = data * 20

        # searching and sorting params
        filters = kwargs["filters"]
        # pagination
        start = int(filters.get("start", 0))
        length = int(filters.get("length", 5))

        fields = [
            "id",
            "name",
            "progress",
            "gender",
            "rating",
            "col",
            "dob",
            "car",
        ]

        # todo: can this be done better i.e. if mpa do x if spa do y?
        if "draw" in filters:  # assume its datatables request (mpa) if draw in filters
            filter_class = DatatablesFilter
            sort_class = DatatablesSort
        else:
            filter_class = None
            sort_class = ReactTablesSort

        # filter the data
        table_data = ToTable(
            data=data,
            filters=filters,
            count_func=lambda x: len(x),
            fields=fields,
            filter_class=filter_class,
            sort_class=sort_class,
        ).get_data(start, length)

        return table_data

    @staticmethod
    def fetch_scatter_map_data(*args, **kwargs) -> MapData:
        return MapData(
            data=[
                MapData.ScatterGeo(
                    lat=[40.7127, 51.5072],
                    lon=[-74.0059, 0.1275],
                    mode="lines",
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

    @staticmethod
    def fetch_choropleth_map_data(*args, **kwargs) -> MapData:
        url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv"
        r = requests.get(url)
        lines = [line.decode("utf-8") for line in r.iter_lines()]
        reader = csv.reader(lines, delimiter=",")
        locations = []
        z = []
        text = []
        for r in reader:
            locations.append(r[2])
            z.append(r[3])
            text.append(r[1])

        return MapData(
            data=[
                MapData.Choropleth(
                    locationmode="USA-states",
                    locations=locations[1:],
                    z=z[1:],
                    text=text[1:],
                    autocolorscale=True,
                )
            ],
            layout={
                "title": "2014 US Popultaion by State",
                "geo": {
                    "scope": "usa",
                    "countrycolor": "rgb(255, 255, 255)",
                    "showland": True,
                    "landcolor": "rgb(217, 217, 217)",
                    "showlakes": True,
                    "lakecolor": "rgb(255, 255, 255)",
                    "subunitcolor": "rgb(255, 255, 255)",
                    "lonaxis": {},
                    "lataxis": {},
                },
            },
        )

    @staticmethod
    def fetch_sse_chart_data(*args, **kwargs) -> ChartData:
        return ChartData(
            data=[
                ChartData.Trace(
                    y=list([1, 2, 3]),
                    type=ChartData.Trace.Type.SCATTER,
                    mode=ChartData.Trace.Mode.LINE,
                )
            ]
        )

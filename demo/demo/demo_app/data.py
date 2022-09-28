import asyncio
import csv
import math
from collections import namedtuple
from random import randint

from django.db.models import Max
from django.utils.safestring import mark_safe

import requests
from datorum.component.chart import ChartData
from datorum.component.map import MapData
from datorum.component.table import TableData, TablePaging
from datorum.component.text import StatData

from demo.demo_app.models import Data, FlatText, Parameter, Vehicle


def dict_to_table(d: dict):
    html = "<table border='1'>"
    for k, v in d.items():
        html += "<tr><th>%s</th><td>%s</td></tr>" % (k, v or "-")

    html += "</table>"

    return mark_safe(html)


def convert_coord(value):
    coord = value[1:-1]
    coord = coord.split(",")
    lon = float(coord[0].strip())
    lat = float(coord[1].strip())
    Coord = namedtuple("Coord", ["lon", "lat"])
    return Coord(lon=lon, lat=lat)


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

        data = data * 20
        total = len(data)  # total number of items before pagination
        # defaults
        limit = 10  # items per page
        page = 0  # current page starting 0
        sort_by = list(data[0].keys())[0]  # column to sort on
        direction = "asc"  # sort order

        filters = kwargs.get("filters")

        # are we paginating?
        if filters:
            # based on react-table - todo: can these be generic for tabulator too?
            limit = int(filters.get("size", limit))
            page = int(filters.get("page", page))
            sort_by = filters.get("sortby", sort_by)
            direction = filters.get("direction", direction)

        # sort the data
        data = sorted(data, key=lambda x: x[sort_by], reverse=direction == "desc")

        page_count = math.ceil(total / limit)
        page_offset = page * limit
        data = data[page_offset:page_offset+limit]

        paging = TablePaging(
            ssr=True,
            page=page,
            limit=limit,
            page_count=page_count,
            total_items=total,
            sortby=[{
                "id": sort_by,
                "desc": direction == 'desc'
            }],
        )

        table_data = TableData(
            headers=[
                "Id",
                "Name",
                "Progress",
                "Gender",
                "Rating",
                "Colour",
                "DOB",
                "Car",
            ],
            rows=data,
            paging=paging
        )

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


class VehicleData:
    @staticmethod
    def get_queryset(filters):
        qs = Vehicle.objects.all()
        if "vehicle_type" in filters:
            if filters["vehicle_type"] != "":
                qs = qs.for_type(filters["vehicle_type"])

        return qs

    @staticmethod
    def get_vehicle(request):
        try:
            return Vehicle.objects.get(number_plate="OmfGAVOoIa")
        except Vehicle.DoesNotExist:
            return Vehicle()

    @staticmethod
    def fetch_vehicle_count(request, **kwargs):
        filters = kwargs.get("filters") or {}
        qs = VehicleData.get_queryset(filters)
        return StatData(text=str(qs.total_vehicle_count()), sub_text="TOTAL VEHICLES")

    @staticmethod
    def fetch_in_use_count(request, **kwargs):
        filters = kwargs.get("filters") or {}
        qs = VehicleData.get_queryset(filters)
        return StatData(text=str(qs.in_use_count()), sub_text="IN USE")

    @staticmethod
    def fetch_out_of_service_count(request, **kwargs):
        filters = kwargs.get("filters") or {}
        qs = VehicleData.get_queryset(filters)
        return StatData(text=str(qs.out_of_service_count()), sub_text="NOT AVAILABLE")

    @staticmethod
    def fetch_service_count(request, **kwargs):
        filters = kwargs.get("filters") or {}
        qs = VehicleData.get_queryset(filters)
        return StatData(
            text=str(qs.requires_service().count()),
            sub_text="REQUIRES SERVICE",
        )

    @staticmethod
    def fetch_vehicles(request, **kwargs):
        def yes_no(d):
            return "Yes" if d else "No"

        filters = kwargs.get("filters") or {}
        qs = VehicleData.get_queryset(filters)

        return TableData(
            headers=[],
            rows=[
                {
                    "Reg": v.number_plate,  # f"<a href='?number_plate={v.number_plate}'>{v.number_plate}</a>",
                    "Type": v.get_type_display(),
                    "In Use": yes_no(v.in_use),
                    "Available": yes_no(v.available),
                    "Last Job": str(v.last_job_date or "-"),
                }
                for v in qs
            ],
        )

    @staticmethod
    def fetch_vehicle_details(*args, **kwargs):
        dashboard = kwargs.get("dashboard")
        vehicle = dashboard.object
        return StatData(
            text=dict_to_table(
                {
                    "number_plate": vehicle.number_plate,
                    "current_mileage": vehicle.current_mileage,
                    "last_service": vehicle.last_service,
                    "next_mot_due": vehicle.next_mot_due,
                    "purchase_date": vehicle.purchase_date,
                    "last_job_date": vehicle.last_job_date,
                    "in_use": vehicle.in_use,
                    "available": vehicle.available,
                }
            )
        )

    @staticmethod
    def fetch_last_route(*args, **kwargs):
        dashboard = kwargs.get("dashboard")
        vehicle = dashboard.object
        locations = vehicle.get_locations_for_last_job()
        lat_coords = [location.lat for location in locations]
        lon_coords = [location.lon for location in locations]

        return MapData(
            data=[
                MapData.ScatterGeo(
                    lat=lat_coords,
                    lon=lon_coords,
                    line={"width": 2, "color": "red"},
                )
            ],
            layout=dict(
                title="Map of Last Job",
                showlegend=False,
                geo={
                    "showland": True,
                    "showlakes": True,
                    "landcolor": "rgb(204, 204, 204)",
                    "countrycolor": "rgb(204, 204, 204)",
                    "lakecolor": "rgb(255, 255, 255)",
                    "fitbounds": "locations",
                },
            ),
        )

    @staticmethod
    def fetch_current_locations(*args, **kwargs):
        qs = (
            Data.objects.filter(
                parameter=Parameter.objects.get(name="Current Location")
            )
            .values("vehicle")
            .order_by("vehicle")
            .annotate(current_position=Max("timestamp"))
            .values("vehicle", "value")
        )

        vehicle_list = [x["vehicle"] for x in qs]
        locations = map(lambda x: convert_coord(x["value"]), qs)
        lat_coords = [location.lat for location in locations]
        lon_coords = [location.lon for location in locations]

        w = MapData(
            data=[
                MapData.ScatterGeo(
                    text=vehicle_list,
                    lat=lat_coords,
                    lon=lon_coords,
                    mode="markers+text",
                    line={"width": 2, "color": "red"},
                )
            ],
            layout=dict(
                title="Map of Last Job",
                showlegend=False,
                geo={
                    "showland": True,
                    "showlakes": True,
                    "landcolor": "rgb(204, 204, 204)",
                    "countrycolor": "rgb(204, 204, 204)",
                    "lakecolor": "rgb(255, 255, 255)",
                    "fitbounds": "locations",
                },
            ),
        )

        return w

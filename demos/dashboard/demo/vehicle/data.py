import json
from collections import namedtuple

from django.db.models import Max
from django.utils.safestring import mark_safe

from demo.vehicle.models import Data, Parameter, Vehicle

from wildcoeus.dashboards.component.text import StatData


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
    def fetch_vehicle_details(*args, **kwargs):
        vehicle = kwargs.get("object")
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
        vehicle = kwargs.get("object")
        locations = vehicle.get_locations_for_last_job()
        lat_coords = [location.lat for location in locations]
        lon_coords = [location.lon for location in locations]

        return json.dumps(
            dict(
                data=[
                    dict(
                        lat=lat_coords,
                        lon=lon_coords,
                        mode="markers+text",
                        type="scattergeo",
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

        return json.dumps(
            dict(
                data=[
                    dict(
                        text=vehicle_list,
                        lat=lat_coords,
                        lon=lon_coords,
                        mode="markers+text",
                        type="scattergeo",
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
        )

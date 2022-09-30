from datorum.component import Form, Map, Stat, Table
from datorum.component.layout import HTML, Card, ComponentLayout, Div
from datorum.dashboard import Dashboard, ModelDashboard
from datorum.registry import registry

from demo.vehicle.data import VehicleData
from demo.vehicle.forms import VehicleTypeFilterForm
from demo.vehicle.models import Vehicle


class VehicleOverviewDashboard(Dashboard):
    filter_form = Form(
        form=VehicleTypeFilterForm,
        method="get",
        dependents=[
            "no_vehicles",
            "in_use",
            "available",
            "requires_service",
            "vehicles",
        ],
        width=3,
    )
    no_vehicles = Stat(defer=VehicleData.fetch_vehicle_count, href="?type=c1", width=4)
    in_use = Stat(defer=VehicleData.fetch_in_use_count, width=4)
    available = Stat(defer=VehicleData.fetch_out_of_service_count, width=4)
    requires_service = Stat(defer=VehicleData.fetch_service_count, width=4)
    map = Map(defer=VehicleData.fetch_current_locations, width=12)
    vehicles = Table(defer=VehicleData.fetch_vehicles, width=12)

    class Meta:
        name = "Vehicle Dashboard"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            HTML(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec vestibulum orci. Sed ac eleifend "
                "diam. Duis quis congue ex. Mauris at bibendum est, nec bibendum ipsum. Lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit.",
                width=12,
            ),
            "filter_form",
            Div(
                Card("no_vehicles", width=3),
                Card("in_use", width=3),
                Card("available", width=3),
                Card("requires_service", width=3),
                css_classes="dashboard-container",
                width=12,
            ),
            Card(
                "map",
                "vehicles",
                width=12,
            ),
        )


class VehicleDetailDashboard(ModelDashboard):
    vehicle_details = Stat(defer=VehicleData.fetch_vehicle_details, width=6)
    map = Map(defer=VehicleData.fetch_last_route, width=6)

    class Meta:
        name = "Vehicle Detail Dashboard"
        model = Vehicle


registry.register(VehicleOverviewDashboard)
registry.register(VehicleDetailDashboard)

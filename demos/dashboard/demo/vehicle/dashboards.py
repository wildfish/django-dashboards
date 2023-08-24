from enum import Enum

from demo.vehicle.data import VehicleData
from demo.vehicle.forms import VehicleTypeFilterForm
from demo.vehicle.models import Vehicle
from demo.vehicle.tables import VehicleTableSerializer

from dashboards import config
from dashboards.component import Form, Map, Stat, Table
from dashboards.component.layout import HTML, Card, ComponentLayout, Div
from dashboards.dashboard import Dashboard, ModelDashboard
from dashboards.registry import registry


class Grid(Enum):
    """define css classes here for grid layout"""

    DEFAULT = config.Config().DASHBOARDS_DEFAULT_GRID_CSS
    ONE = "span-12"
    DOUBLE = "span-9"
    TWO = "span-6"
    THREE = "span-4"
    FOUR = "span-3"


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
        grid_css_classes=Grid.THREE.value,
    )
    no_vehicles = Stat(
        defer=VehicleData.fetch_vehicle_count,
        href="?type=c1",
    )
    in_use = Stat(defer=VehicleData.fetch_in_use_count)
    available = Stat(defer=VehicleData.fetch_out_of_service_count)
    requires_service = Stat(defer=VehicleData.fetch_service_count)
    map = Map(defer=VehicleData.fetch_current_locations)
    vehicles = Table(defer=VehicleTableSerializer)

    class Meta:
        name = "Summary"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            HTML(
                "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec vestibulum orci. Sed ac eleifend "
                "diam. Duis quis congue ex. Mauris at bibendum est, nec bibendum ipsum. Lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit.</p>",
            ),
            Card("filter_form", grid_css_classes=Grid.ONE.value),
            Card("no_vehicles", grid_css_classes=Grid.FOUR.value),
            Card("in_use", grid_css_classes=Grid.FOUR.value),
            Card("available", grid_css_classes=Grid.FOUR.value),
            Card("requires_service", grid_css_classes=Grid.FOUR.value),
            Card(
                "map",
                "vehicles",
                grid_css_classes=Grid.ONE.value,
            ),
        )


class VehicleDetailDashboard(ModelDashboard):
    vehicle_details = Stat(
        defer=VehicleData.fetch_vehicle_details, grid_css_classes=Grid.TWO.value
    )
    map = Map(defer=VehicleData.fetch_last_route, grid_css_classes=Grid.ONE.value)

    class Meta:
        name = "Vehicle Detail"
        model = Vehicle


registry.register(VehicleOverviewDashboard)
registry.register(VehicleDetailDashboard)

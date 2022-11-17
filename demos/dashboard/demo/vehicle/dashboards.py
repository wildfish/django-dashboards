from enum import Enum

from demo.vehicle.data import VehicleData
from demo.vehicle.forms import VehicleTypeFilterForm
from demo.vehicle.models import Vehicle

from wildcoeus.dashboards import config
from wildcoeus.dashboards.component import Form, Map, Stat, Table
from wildcoeus.dashboards.component.layout import HTML, Card, ComponentLayout, Div
from wildcoeus.dashboards.dashboard import Dashboard, ModelDashboard
from wildcoeus.dashboards.registry import registry


class Grid(Enum):
    """define css classes here for grid layout"""

    DEFAULT = config.Config().WILDCOEUS_DEFAULT_GRID_CSS
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
        grid_css_classes=Grid.FOUR.value,
    )
    in_use = Stat(
        defer=VehicleData.fetch_in_use_count, grid_css_classes=Grid.FOUR.value
    )
    available = Stat(
        defer=VehicleData.fetch_out_of_service_count, grid_css_classes=Grid.FOUR.value
    )
    requires_service = Stat(
        defer=VehicleData.fetch_service_count, grid_css_classes=Grid.FOUR.value
    )
    map = Map(
        defer=VehicleData.fetch_current_locations, grid_css_classes=Grid.ONE.value
    )
    vehicles = Table(defer=VehicleData.fetch_vehicles, grid_css_classes=Grid.ONE.value)

    class Meta:
        name = "Summary"

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            HTML(
                "<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin nec vestibulum orci. Sed ac eleifend "
                "diam. Duis quis congue ex. Mauris at bibendum est, nec bibendum ipsum. Lorem ipsum "
                "dolor sit amet, consectetur adipiscing elit.</p>",
            ),
            "filter_form",
            Div(
                Card("no_vehicles", grid_css_classes=Grid.THREE.value),
                Card("in_use", grid_css_classes=Grid.THREE.value),
                Card("available", grid_css_classes=Grid.THREE.value),
                Card("requires_service", grid_css_classes=Grid.THREE.value),
                css_classes="dashboard-container",
                grid_css_classes=Grid.ONE.value,
            ),
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
    map = Map(defer=VehicleData.fetch_last_route, grid_css_classes=Grid.TWO.value)

    class Meta:
        name = "Vehicle Detail"
        model = Vehicle


registry.register(VehicleOverviewDashboard)
registry.register(VehicleDetailDashboard)

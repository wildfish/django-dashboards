from dashboards.menus.menu import DashboardMenu
from dashboards.menus.registry import menu_registry


class VehicleMenu(DashboardMenu):
    name = "Vehicle"
    app_label = "vehicle"


menu_registry.register(VehicleMenu)

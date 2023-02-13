from wildcoeus.dashboards.menus.menu import DashboardMenu
from wildcoeus.dashboards.menus.registry import menu_registry


class KitchenSinkMenu(DashboardMenu):
    name = "Kitchen Sink"
    app_label = "kitchensink"


menu_registry.register(KitchenSinkMenu)

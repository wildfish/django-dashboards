from dashboards.registry import Registry


class MenuRegistry(Registry):
    def __init__(self):
        super().__init__("dashboard_menu")


menu_registry = MenuRegistry()

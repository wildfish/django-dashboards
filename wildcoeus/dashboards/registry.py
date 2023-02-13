from wildcoeus.registry.registry import Registry


class DashboardRegistry(Registry):
    def __init__(self):
        super().__init__("dashboards")


registry = DashboardRegistry()

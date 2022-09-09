class DashboardError(Exception):
    pass


class ComponentNotFoundError(DashboardError):
    pass


class LayoutError(DashboardError):
    pass

class DashboardError(Exception):
    pass


class DashboardNotFoundError(DashboardError):
    pass


class ComponentNotFoundError(DashboardError):
    pass


class LayoutError(DashboardError):
    pass

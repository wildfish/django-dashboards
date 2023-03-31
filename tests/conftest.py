import pytest

from dashboards.registry import registry
from tests.dashboards.app1 import dashboards


@pytest.fixture(autouse=True)
def auto_registry():
    registry.reset()
    registry.register(dashboards.TestDashboard)
    registry.register(dashboards.TestFilterDashboard)
    registry.register(dashboards.TestAdminDashboard)
    registry.register(dashboards.TestComplexDashboard)
    registry.register(dashboards.TestDashboardWithLayout)
    registry.register(dashboards.TestModelDashboard)
    registry.register(dashboards.TestNoMetaDashboard)

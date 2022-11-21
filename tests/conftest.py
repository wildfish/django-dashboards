import pytest

from tests.dashboards import dashboards
from wildcoeus.dashboards.registry import registry
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.tasks.registry import task_registry


@pytest.fixture(autouse=True)
def auto_registry():
    registry.register(dashboards.TestDashboard)
    registry.register(dashboards.TestFilterDashboard)
    registry.register(dashboards.TestAdminDashboard)
    registry.register(dashboards.TestComplexDashboard)
    registry.register(dashboards.TestDashboardWithLayout)
    registry.register(dashboards.TestModelDashboard)


@pytest.fixture(autouse=True)
def reset_registry():
    task_registry.reset()
    pipeline_registry.reset()

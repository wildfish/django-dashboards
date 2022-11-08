import pytest

from tests.dashboards.dashboards import (
    TestAdminDashboard,
    TestComplexDashboard,
    TestDashboard,
    TestDashboardWithLayout,
    TestFilterDashboard,
    TestModelDashboard,
)
from wildcoeus.dashboards.registry import registry
from wildcoeus.pipelines.tasks.registry import task_registry


@pytest.fixture(autouse=True)
def auto_registry():
    registry.register(TestDashboard)
    registry.register(TestFilterDashboard)
    registry.register(TestAdminDashboard)
    registry.register(TestComplexDashboard)
    registry.register(TestDashboardWithLayout)
    registry.register(TestModelDashboard)


@pytest.fixture(autouse=True)
def reset_registry():
    task_registry.reset()

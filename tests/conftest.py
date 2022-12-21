import pytest

from tests.dashboards.app1 import dashboards
from tests.pipelines import pipelines
from wildcoeus.dashboards.registry import registry
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.tasks.registry import task_registry


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


@pytest.fixture(autouse=True)
def auto_pipeline_registry():
    pipeline_registry.reset()
    pipeline_registry.register(pipelines.TestPipeline)
    pipeline_registry.register(pipelines.TestModelPipeline)
    pipeline_registry.register(pipelines.TestIteratorPipeline)
    pipeline_registry.register(pipelines.TestModelPipelineQS)


@pytest.fixture(autouse=True)
def reset_registry():
    task_registry.reset()

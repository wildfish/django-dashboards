from unittest.mock import Mock

import pytest

from datorum_pipelines import BasePipeline, BaseTask
from datorum_pipelines.runners.base import BasePipelineRunner


pytestmark = pytest.mark.django_db


def test_graph_order__no_parents():
    reporter = Mock()

    class Task(BaseTask):
        def run(self, *args, **kwargs):
            return True

    class Pipeline(BasePipeline):
        first = Task(config={})
        second = Task(config={})

        class Meta:
            title = "Test Pipeline"

    tasks = Pipeline().clean_tasks(reporter)
    ordered_tasks = BasePipelineRunner()._get_task_graph(tasks=tasks)

    assert len(ordered_tasks) == 2
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "second"


def test_graph_order__with_parents():
    reporter = Mock()

    class Task(BaseTask):
        def run(self, *args, **kwargs):
            return True

    class Pipeline(BasePipeline):
        first = Task(config={})
        second = Task(config={"parents": ["first"]})
        third = Task(config={"parents": ["second"]})
        forth = Task(config={})

        class Meta:
            title = "Test Pipeline"

    tasks = Pipeline().clean_tasks(reporter)
    ordered_tasks = BasePipelineRunner()._get_task_graph(tasks=tasks)

    assert len(ordered_tasks) == 4
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "forth"
    assert ordered_tasks[2].pipeline_task == "second"
    assert ordered_tasks[3].pipeline_task == "third"

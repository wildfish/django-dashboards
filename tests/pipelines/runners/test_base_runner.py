from unittest.mock import Mock

import pytest

from wildcoeus.pipelines import Pipeline, Task
from wildcoeus.pipelines.runners.base import PipelineRunner


pytestmark = pytest.mark.django_db


def test_graph_order__no_parents():
    reporter = Mock()

    class TestTask(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTask(config={})
        second = TestTask(config={})

        class Meta:
            title = "Test Pipeline"

    tasks = TestPipeline().clean_tasks(reporter)
    ordered_tasks = PipelineRunner()._get_task_graph(tasks=tasks)

    assert len(ordered_tasks) == 2
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "second"


def test_graph_order__with_parents():
    reporter = Mock()

    class TestTask(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTask(config={})
        second = TestTask(config={"parents": ["first"]})
        third = TestTask(config={"parents": ["second"]})
        forth = TestTask(config={})

        class Meta:
            title = "Test Pipeline"

    tasks = TestPipeline().clean_tasks(reporter)
    ordered_tasks = PipelineRunner()._get_task_graph(tasks=tasks)

    assert len(ordered_tasks) == 4
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "forth"
    assert ordered_tasks[2].pipeline_task == "second"
    assert ordered_tasks[3].pipeline_task == "third"

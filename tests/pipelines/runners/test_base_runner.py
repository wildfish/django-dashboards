from unittest.mock import Mock, patch

import pytest

from tests.dashboards.fakes import fake_user
from wildcoeus.pipelines import Pipeline
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners.base import PipelineRunner


pytestmark = pytest.mark.django_db

pytest_plugins = [
    "tests.pipelines.fixtures",
]


def test_graph_order__no_parents(test_task):
    reporter = Mock()

    class TestPipeline(Pipeline):
        first = test_task(config={})
        second = test_task(config={})

        class Meta:
            title = "Test Pipeline"

    tasks = TestPipeline().clean_tasks(reporter)
    ordered_tasks = PipelineRunner()._get_task_graph(tasks=tasks)

    assert len(ordered_tasks) == 2
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "second"


def test_graph_order__with_parents(test_task):
    reporter = Mock()

    class TestPipeline(Pipeline):
        first = test_task(config={})
        second = test_task(config={"parents": ["first"]})
        third = test_task(config={"parents": ["second"]})
        forth = test_task(config={})

        class Meta:
            title = "Test Pipeline"

    tasks = TestPipeline().clean_tasks(reporter)
    ordered_tasks = PipelineRunner()._get_task_graph(tasks=tasks)

    assert len(ordered_tasks) == 4
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "forth"
    assert ordered_tasks[2].pipeline_task == "second"
    assert ordered_tasks[3].pipeline_task == "third"


def test_start__start_runner_called(test_pipeline):
    reporter = Mock()

    tasks = test_pipeline().clean_tasks(reporter)
    pipeline_registry.register(test_pipeline)

    with patch(
        "wildcoeus.pipelines.runners.base.PipelineRunner.start_runner"
    ) as runner:
        PipelineRunner().start(
            pipeline_id="tests.pipelines.fixtures.TestPipeline",
            run_id="1",
            tasks=tasks,
            input_data={},
            reporter=reporter,
        )
        assert runner.call_count == 1


def test_start__iterator__start_runner_called(test_iterator_pipeline):
    reporter = Mock()
    fake_user(_quantity=3)
    tasks = test_iterator_pipeline().clean_tasks(reporter)
    pipeline_registry.register(test_iterator_pipeline)

    with patch(
        "wildcoeus.pipelines.runners.base.PipelineRunner.start_runner"
    ) as runner:
        PipelineRunner().start(
            pipeline_id="tests.pipelines.fixtures.TestPipeline",
            run_id="1",
            tasks=tasks,
            input_data={},
            reporter=reporter,
        )
        assert runner.call_count == 3


def test_start__model__start_runner_called(test_model_pipeline):
    reporter = Mock()
    fake_user(_quantity=3)
    tasks = test_model_pipeline().clean_tasks(reporter)
    pipeline_registry.register(test_model_pipeline)

    with patch(
        "wildcoeus.pipelines.runners.base.PipelineRunner.start_runner"
    ) as runner:
        PipelineRunner().start(
            pipeline_id="tests.pipelines.fixtures.TestPipeline",
            run_id="1",
            tasks=tasks,
            input_data={},
            reporter=reporter,
        )
        assert runner.call_count == 3


def test_start__model_qs__start_runner_called(test_model_pipeline_qs):
    reporter = Mock()
    fake_user(_quantity=3)
    tasks = test_model_pipeline_qs().clean_tasks(reporter)
    pipeline_registry.register(test_model_pipeline_qs)

    with patch(
        "wildcoeus.pipelines.runners.base.PipelineRunner.start_runner"
    ) as runner:
        PipelineRunner().start(
            pipeline_id="tests.pipelines.fixtures.TestPipeline",
            run_id="1",
            tasks=tasks,
            input_data={},
            reporter=reporter,
        )
        assert runner.call_count == 3

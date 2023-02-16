from unittest.mock import Mock, patch

import pytest

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.results.helpers import build_pipeline_execution
from wildcoeus.pipelines.runners.base import PipelineRunner


pytestmark = pytest.mark.django_db

pytest_plugins = [
    "tests.pipelines.fixtures",
]


def test_graph_order__no_parents(test_task):
    class TestPipeline(Pipeline):
        first = test_task(config={})
        second = test_task(config={})

        class Meta:
            app_label = "pipelinetest"

    pipeline_execution = build_pipeline_execution(
        TestPipeline(),
        "run_id",
        Mock(),
        Mock(),
        {},
    )
    ordered_tasks = PipelineRunner().get_flat_task_list(
        pipeline_execution.get_pipeline_results()[0]
    )

    assert len(ordered_tasks) == 2
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "second"


def test_graph_order__with_parents(test_task):
    class TestPipeline(Pipeline):
        first = test_task(config={})
        second = test_task(config={"parents": ["first"]})
        third = test_task(config={"parents": ["second"]})
        fourth = test_task(config={})

        ordering = {
            "second": ["first"],
            "third": ["second"],
        }

        class Meta:
            app_label = "pipelinetest"

    pipeline_execution = build_pipeline_execution(
        TestPipeline(),
        "run_id",
        Mock(),
        Mock(),
        {},
    )
    ordered_tasks = PipelineRunner().get_flat_task_list(
        pipeline_execution.get_pipeline_results()[0]
    )

    assert len(ordered_tasks) == 4
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "fourth"
    assert ordered_tasks[2].pipeline_task == "second"
    assert ordered_tasks[3].pipeline_task == "third"


def test_start__start_runner_called(test_pipeline):
    reporter = Mock()

    pipeline_execution = build_pipeline_execution(
        test_pipeline(),
        "run_id",
        Mock(),
        reporter,
        {},
    )

    with patch(
        "wildcoeus.pipelines.runners.base.PipelineRunner.start_runner"
    ) as runner:
        PipelineRunner().start(
            pipeline_execution,
            reporter=reporter,
        )
        assert runner.call_count == 1

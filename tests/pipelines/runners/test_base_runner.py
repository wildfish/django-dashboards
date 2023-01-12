from unittest.mock import Mock, patch

import pytest

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.runners.base import PipelineRunner
from wildcoeus.pipelines.status import PipelineTaskStatus


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
            app_label = "pipelinetest"

    tasks = TestPipeline().clean_tasks(reporter, run_id="123")
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
            app_label = "pipelinetest"

    tasks = TestPipeline().clean_tasks(reporter, run_id="123")
    ordered_tasks = PipelineRunner()._get_task_graph(tasks=tasks)

    assert len(ordered_tasks) == 4
    assert ordered_tasks[0].pipeline_task == "first"
    assert ordered_tasks[1].pipeline_task == "forth"
    assert ordered_tasks[2].pipeline_task == "second"
    assert ordered_tasks[3].pipeline_task == "third"


def test_start__start_runner_called(test_pipeline):
    reporter = Mock()

    tasks = test_pipeline().clean_tasks(reporter, run_id="123")

    with patch(
        "wildcoeus.pipelines.runners.base.PipelineRunner.start_runner"
    ) as runner:
        PipelineRunner().start(
            pipeline_id=test_pipeline.get_id(),
            run_id="1",
            tasks=tasks,
            input_data={},
            reporter=reporter,
        )
        assert runner.call_count == 1


def test_multiple_pipeline_objects___start_is_called_with_each():
    class MultiObjectPipeline(Pipeline):
        class Meta:
            app_label = "testpipeline"

        @classmethod
        def get_iterator(cls):
            return ["first", "second"]

    reporter = Mock()

    runner = Mock()

    pipeline = MultiObjectPipeline()
    pipeline.start_pipeline = Mock()
    pipeline.start(
        "1",
        {},
        runner,
        reporter,
    )

    pipeline.start_pipeline.assert_any_call(
        run_id="1",
        input_data={},
        runner=runner,
        reporter=reporter,
        pipeline_object="first",
    )
    pipeline.start_pipeline.assert_any_call(
        run_id="1",
        input_data={},
        runner=runner,
        reporter=reporter,
        pipeline_object="second",
    )
    assert pipeline.start_pipeline.call_count == 2


def test_multiple_pipeline_objects_with_first_erroring___start_is_called_with_each():
    class MultiObjectPipeline(Pipeline):
        class Meta:
            app_label = "testpipeline"

        @classmethod
        def get_iterator(cls):
            return ["first", "second"]

    reporter = Mock()

    runner = Mock()

    pipeline = MultiObjectPipeline()
    pipeline.start_pipeline = Mock(side_effect=[Exception("First has errored"), None])
    pipeline.start(
        "1",
        {},
        runner,
        reporter,
    )

    pipeline.start_pipeline.assert_any_call(
        run_id="1",
        input_data={},
        runner=runner,
        reporter=reporter,
        pipeline_object="first",
    )
    pipeline.start_pipeline.assert_any_call(
        run_id="1",
        input_data={},
        runner=runner,
        reporter=reporter,
        pipeline_object="second",
    )
    reporter.report_pipeline.assert_called_once_with(
        MultiObjectPipeline.get_id(),
        PipelineTaskStatus.RUNTIME_ERROR.value,
        f"Error starting pipeline: First has errored",
        run_id="1",
        serializable_pipeline_object=pipeline.get_serializable_pipeline_object(
            obj="first"
        ),
    )
    assert pipeline.start_pipeline.call_count == 2

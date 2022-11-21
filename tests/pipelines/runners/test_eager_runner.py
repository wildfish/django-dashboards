from unittest.mock import Mock, call

import pytest

from wildcoeus.pipelines import Pipeline, PipelineTaskStatus, Task
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners.eager import Runner


pytestmark = pytest.mark.django_db


def test_task_have_no_parents___tasks_are_ran_in_configured_order():
    reporter = Mock()

    class TestTask(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTask(config={})
        second = TestTask(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    pipeline.start(run_id="123", input_data={}, runner=Runner(), reporter=reporter)

    assert reporter.report_task.call_args_list.index(
        call(
            pipeline_task="first",
            task_id="test_eager_runner.TestTask",
            status=PipelineTaskStatus.RUNNING,
            message="Task is running",
            object_lookup=None,
        )
    ) < reporter.report_task.call_args_list.index(
        call(
            pipeline_task="second",
            task_id="test_eager_runner.TestTask",
            status=PipelineTaskStatus.RUNNING,
            message="Task is running",
            object_lookup=None,
        )
    )


def test_task_with_parent_waits_for_parents_to_be_ran():
    reporter = Mock()

    class TestTask(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        parent = TestTask(config={})
        child = TestTask(config={"parents": ["parent"]})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    pipeline.start(run_id="123", input_data={}, runner=Runner(), reporter=reporter)

    assert reporter.report_task.call_args_list.index(
        call(
            pipeline_task="parent",
            task_id="test_eager_runner.TestTask",
            status=PipelineTaskStatus.RUNNING,
            message="Task is running",
            object_lookup=None,
        )
    ) < reporter.report_task.call_args_list.index(
        call(
            pipeline_task="child",
            task_id="test_eager_runner.TestTask",
            status=PipelineTaskStatus.RUNNING,
            message="Task is running",
            object_lookup=None,
        )
    )


def test_first_task_fails___other_tasks_are_cancelled():
    reporter = Mock()

    class BadTask(Task):
        def run(self, *args, **kwargs):
            raise Exception("Test error")

    good_task_start = Mock()

    class GoodTask(Task):
        def start(self, *args, **kwargs):
            good_task_start(*args, **kwargs)

    class TestPipeline(Pipeline):
        bad = BadTask(config={})
        good = GoodTask(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    pipeline.start(run_id="123", input_data={}, runner=Runner(), reporter=reporter)

    reporter.report_task.assert_any_call(
        pipeline_task="bad",
        task_id="test_eager_runner.BadTask",
        status=PipelineTaskStatus.RUNTIME_ERROR,
        message="Test error",
        object_lookup=None,
    )
    reporter.report_task.assert_any_call(
        pipeline_task="good",
        task_id="test_eager_runner.GoodTask",
        status=PipelineTaskStatus.CANCELLED,
        message="There was an error running a different task",
        object_lookup=None,
    )

    good_task_start.assert_not_called()

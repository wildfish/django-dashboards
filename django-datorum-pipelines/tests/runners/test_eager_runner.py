from unittest.mock import Mock, call

from datorum_pipelines import (
    BasePipeline,
    BaseTask,
    PipelineConfigEntry,
    PipelineTaskStatus,
)
from datorum_pipelines.runners.eager import EagerRunner


def test_task_have_no_parents___tasks_are_ran_in_configured_order():
    reporter = Mock()

    class Task(BaseTask):
        def run(self, cleaned_data):
            return True

    pipeline = BasePipeline(
        "pipeline",
        [
            PipelineConfigEntry(
                name="Task",
                id="first",
                config={},
            ),
            PipelineConfigEntry(
                name="Task",
                id="second",
                config={},
            ),
        ],
    )

    pipeline.start({}, EagerRunner(), reporter)

    reporter.report_task.assert_any_call(
        "first", PipelineTaskStatus.RUNNING, "Task is running"
    )
    reporter.report_task.assert_any_call(
        "second", PipelineTaskStatus.RUNNING, "Task is running"
    )
    assert reporter.report_task.call_args_list.index(
        call("first", PipelineTaskStatus.RUNNING, "Task is running")
    ) < reporter.report_task.call_args_list.index(
        call("second", PipelineTaskStatus.RUNNING, "Task is running")
    )


def test_task_with_parent_waits_for_parents_to_be_ran():
    reporter = Mock()

    class Task(BaseTask):
        def run(self, cleaned_data):
            return True

    pipeline = BasePipeline(
        "pipeline",
        [
            PipelineConfigEntry(
                name="Task",
                id="child",
                config={"parents": ["parent"]},
            ),
            PipelineConfigEntry(
                name="Task",
                id="parent",
                config={"label": "parent"},
            ),
        ],
    )

    pipeline.start({}, EagerRunner(), reporter)

    reporter.report_task.assert_any_call(
        "parent", PipelineTaskStatus.RUNNING, "Task is running"
    )
    reporter.report_task.assert_any_call(
        "child", PipelineTaskStatus.RUNNING, "Task is running"
    )
    assert reporter.report_task.call_args_list.index(
        call("parent", PipelineTaskStatus.RUNNING, "Task is running")
    ) < reporter.report_task.call_args_list.index(
        call("child", PipelineTaskStatus.RUNNING, "Task is running")
    )


def test_first_task_fails___other_tasks_are_cancelled():
    reporter = Mock()

    class BadTask(BaseTask):
        def run(self, cleaned_data):
            raise Exception("Test error")

    good_task_start = Mock()

    class GoodTask(BaseTask):
        def start(self, *args, **kwargs):
            good_task_start(*args, **kwargs)

    pipeline = BasePipeline(
        "pipeline",
        [
            PipelineConfigEntry(
                name="BadTask",
                id="first",
                config={},
            ),
            PipelineConfigEntry(
                name="GoodTask",
                id="second",
                config={},
            ),
        ],
    )

    pipeline.start({}, EagerRunner(), reporter)

    reporter.report_task.assert_any_call(
        "first", PipelineTaskStatus.RUNTIME_ERROR, "Test error"
    )
    reporter.report_task.assert_any_call(
        "second",
        PipelineTaskStatus.CANCELLED,
        "There was an error running a different task",
    )
    good_task_start.assert_not_called()

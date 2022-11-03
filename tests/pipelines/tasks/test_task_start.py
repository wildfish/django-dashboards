from unittest.mock import Mock

import pytest
from pydantic import BaseModel

from tests.pipelines.tasks.fakes import make_fake_task
from wildcoeus.pipelines import BaseTask
from wildcoeus.pipelines.reporters import PipelineTaskStatus


pytestmark = pytest.mark.django_db


class InputType(BaseModel):
    value: int


def test_input_is_provided_when_not_expected___error_is_reported_run_is_not_called():
    reporter = Mock()

    task = make_fake_task(input_type=None)()

    task.start(
        pipeline_id="pipeline",
        run_id="123",
        input_data={"value": 1},
        reporter=reporter,
    )

    reporter.report_task.assert_called_once_with(
        pipeline_task="fake",
        task_id=task.task_id,
        status=PipelineTaskStatus.VALIDATION_ERROR,
        message="Input data was provided when no input type was specified",
    )
    task.run_body.assert_not_called()


def test_input_data_does_not_match_the_input_type___error_is_reported_run_is_not_called():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()

    task.start(
        pipeline_id="pipeline",
        run_id="123",
        input_data={"value": "foo"},
        reporter=reporter,
    )

    reporter.report_task.assert_called_once_with(
        pipeline_task="fake",
        task_id=task.task_id,
        status=PipelineTaskStatus.VALIDATION_ERROR,
        message='[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]',
    )
    task.run_body.assert_not_called()


def test_input_data_matches_the_input_type___run_is_called_with_the_cleaned_data():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()

    task.start(
        pipeline_id="pipeline",
        run_id="123",
        input_data={"value": "1"},
        reporter=reporter,
    )

    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        status=PipelineTaskStatus.RUNNING,
        message="Task is running",
    )
    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )
    task.run_body.assert_called_once_with({"value": 1})


def test_input_data_and_type_are_none___run_is_called_with_none():
    reporter = Mock()

    task = make_fake_task(input_type=None)()

    task.start(
        pipeline_id="pipeline",
        run_id="123",
        input_data=None,
        reporter=reporter,
    )

    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        status=PipelineTaskStatus.RUNNING,
        message="Task is running",
    )
    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )
    task.run_body.assert_called_once_with(None)


def test_errors_at_runtime___task_is_recorded_as_error():
    reporter = Mock()

    class ErroringTask(BaseTask):
        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            raise Exception("Some bad error")

    task = ErroringTask({})
    task.pipeline_task = "erroring_task"

    task.start(
        pipeline_id="pipeline",
        run_id="123",
        input_data={},
        reporter=reporter,
    )

    reporter.report_task.assert_any_call(
        pipeline_task="erroring_task",
        task_id="test_task_start.ErroringTask",
        status=PipelineTaskStatus.RUNTIME_ERROR,
        message="Some bad error",
    )

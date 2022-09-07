from unittest.mock import Mock

from pydantic import BaseModel

from datorum_pipelines import BaseTask
from datorum_pipelines.reporters import PipelineTaskStatus
from tests.tasks.fakes import make_fake_task


class InputType(BaseModel):
    value: int


def test_input_is_provided_when_not_expected___error_is_reported_run_is_not_called():
    reporter = Mock()

    task = make_fake_task(input_type=None)()

    task.start({"value": 1}, reporter)

    reporter.report_task.assert_called_once_with(
        task.id,
        PipelineTaskStatus.VALIDATION_ERROR,
        "Input data was provided when no input type was specified",
    )
    task.run_body.assert_not_called()


def test_input_data_does_not_match_the_input_type___error_is_reported_run_is_not_called():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()

    task.start({"value": "foo"}, reporter)

    reporter.report_task.assert_called_once_with(
        task.id,
        PipelineTaskStatus.VALIDATION_ERROR,
        '[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]',
    )
    task.run_body.assert_not_called()


def test_input_data_matches_the_input_type___run_is_called_with_the_cleaned_data():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()

    task.start({"value": "1"}, reporter)

    reporter.report_task.assert_any_call(
        task.id,
        PipelineTaskStatus.RUNNING,
        "Task is running",
    )
    reporter.report_task.assert_any_call(
        task.id,
        PipelineTaskStatus.DONE,
        "Done",
    )
    task.run_body.assert_called_once_with({"value": 1})


def test_input_data_and_type_are_none___run_is_called_with_none():
    reporter = Mock()

    task = make_fake_task(input_type=None)()

    task.start(None, reporter)

    reporter.report_task.assert_any_call(
        task.id,
        PipelineTaskStatus.RUNNING,
        "Task is running",
    )
    reporter.report_task.assert_any_call(
        task.id,
        PipelineTaskStatus.DONE,
        "Done",
    )
    task.run_body.assert_called_once_with(None)


def test_errors_at_runtime___task_is_recorded_as_error():
    reporter = Mock()

    class ErroringTask(BaseTask):
        def run(self, cleaned_data):
            raise Exception("Some bad error")

    task = ErroringTask("error", {})

    task.start({}, reporter)

    reporter.report_task.assert_any_call(
        "error", PipelineTaskStatus.RUNTIME_ERROR, "Some bad error"
    )

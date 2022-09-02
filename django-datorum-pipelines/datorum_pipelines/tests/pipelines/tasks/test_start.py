from unittest.mock import Mock
from uuid import uuid4

from pydantic import BaseModel

from datorum_pipelines import BaseTask
from datorum_pipelines.reporter import PipelineTaskStatus


class InputType(BaseModel):
    value: int


def make_fake_task(input_type):
    class FakeTask(BaseTask):
        InputType = input_type

        def __init__(self):
            super().__init__(uuid4().hex, Mock())
            self.input_data = None

    task = FakeTask()
    task.run = Mock()
    return task


def test_no_input_is_provided_when_expected___error_is_reported_run_is_not_called():
    task = make_fake_task(InputType)

    task.start({})

    task.reporter.report_task.assert_called_once_with(
        task.id,
        PipelineTaskStatus.VALIDATION_ERROR,
        "Input data was not provided when expected",
    )
    task.run.assert_not_called()


def test_input_is_provided_when_not_expected___error_is_reported_run_is_not_called():
    task = make_fake_task(None)

    task.start({"value": 1})

    task.reporter.report_task.assert_called_once_with(
        task.id,
        PipelineTaskStatus.VALIDATION_ERROR,
        "Input data was provided when not expected",
    )
    task.run.assert_not_called()


def test_input_data_does_not_match_the_input_type___error_is_reported_run_is_not_called():
    task = make_fake_task(InputType)

    task.start({"value": "foo"})

    task.reporter.report_task.assert_called_once_with(
        task.id,
        PipelineTaskStatus.VALIDATION_ERROR,
        '[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]',
    )
    task.run.assert_not_called()


def test_input_data_matches_the_input_type___run_is_called_with_the_cleaned_data():
    task = make_fake_task(InputType)

    task.start({"value": "1"})

    task.reporter.report_task.assert_not_called()
    task.run.assert_called_once_with({"value": 1})

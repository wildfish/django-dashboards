import logging
import uuid
from unittest.mock import Mock

from django.contrib.auth.models import User

import pytest
from pydantic import BaseModel

from tests.dashboards.fakes import fake_user
from tests.pipelines.tasks.fakes import make_fake_task
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task
from wildcoeus.pipelines.tasks.base import InputValidationError


pytestmark = pytest.mark.django_db


logger = logging.getLogger("test_task_start")


class InputType(BaseModel):
    value: int


def test_input_is_provided_when_not_expected___error_is_reported_run_is_not_called():
    reporter = Mock()

    task = make_fake_task(input_type=None)()

    with pytest.raises(InputValidationError):
        task.start(
            pipeline_id="pipeline",
            run_id="123",
            input_data={"value": 1},
            reporter=reporter,
        )

    reporter.report_task.assert_called_once_with(
        pipeline_task="fake",
        task_id=task.task_id,
        run_id="123",
        status=PipelineTaskStatus.VALIDATION_ERROR.value,
        message="Input data was provided when no input type was specified",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )
    task.run_body.assert_not_called()


def test_input_data_does_not_match_the_input_type___error_is_reported_run_is_not_called():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()

    with pytest.raises(InputValidationError):
        task.start(
            pipeline_id="pipeline",
            run_id="123",
            input_data={"value": "foo"},
            reporter=reporter,
        )

    reporter.report_task.assert_called_once_with(
        pipeline_task="fake",
        task_id=task.task_id,
        run_id="123",
        status=PipelineTaskStatus.VALIDATION_ERROR.value,
        message='[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]',
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )
    task.run_body.assert_not_called()


def test_input_data_matches_the_input_type___run_is_called_with_the_cleaned_data():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()
    run_id = str(uuid.uuid4())

    task.start(
        pipeline_id="pipeline",
        run_id=run_id,
        input_data={"value": "1"},
        reporter=reporter,
    )

    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        run_id=run_id,
        status=PipelineTaskStatus.RUNNING.value,
        message="Task is running",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )
    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        run_id=run_id,
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )
    task.run_body.assert_called_once_with({"value": 1})


def test_input_data_and_type_are_none___run_is_called_with_none():
    reporter = Mock()

    task = make_fake_task(input_type=None)()
    run_id = str(uuid.uuid4())

    task.start(
        pipeline_id="pipeline",
        run_id=run_id,
        input_data=None,
        reporter=reporter,
    )

    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        run_id=run_id,
        status=PipelineTaskStatus.RUNNING.value,
        message="Task is running",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )
    reporter.report_task.assert_any_call(
        pipeline_task="fake",
        task_id=task.task_id,
        run_id=run_id,
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )
    task.run_body.assert_called_once_with(None)


def test_errors_at_runtime___task_is_recorded_as_error():
    reporter = Mock()

    class ErroringTask(Task):
        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            raise Exception("Some bad error")

    task = ErroringTask({})
    task.pipeline_task = "erroring_task"
    run_id = str(uuid.uuid4())

    with pytest.raises(Exception):
        task.start(
            pipeline_id="pipeline",
            run_id=run_id,
            input_data={},
            reporter=reporter,
        )

    reporter.report_task.assert_any_call(
        pipeline_task="erroring_task",
        task_id="test_task_start.ErroringTask",
        run_id=run_id,
        status=PipelineTaskStatus.RUNTIME_ERROR.value,
        message="Some bad error",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )


def test_pipeline_object_accessible__django_object(caplog):
    reporter = Mock()
    user = fake_user()

    class ObjectTask(Task):
        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert isinstance(self.pipeline_object, User)
            with caplog.at_level(logging.INFO):
                logger.info(f"Object {self.pipeline_object.pk}")

    task = ObjectTask({})
    task.pipeline_task = "object_task"
    run_id = str(uuid.uuid4())

    task.start(
        pipeline_id="pipeline",
        run_id=run_id,
        input_data={},
        reporter=reporter,
        serializable_pipeline_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
        serializable_task_object=None,
    )

    reporter.report_task.assert_any_call(
        pipeline_task="object_task",
        task_id="test_task_start.ObjectTask",
        run_id=run_id,
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
        serializable_task_object=None,
    )

    assert f"Object {user.pk}" in caplog.text


def test_pipeline_object_accessible__non_django_object(caplog):
    reporter = Mock()
    user = fake_user()

    class ObjectTask(Task):
        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert isinstance(self.pipeline_object, User)
            with caplog.at_level(logging.INFO):
                logger.info(f"Object {self.pipeline_object.pk}")

    task = ObjectTask({})
    task.pipeline_task = "object_task"
    run_id = str(uuid.uuid4())

    task.start(
        pipeline_id="pipeline",
        run_id=run_id,
        input_data={},
        reporter=reporter,
        serializable_pipeline_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
        serializable_task_object=None,
    )

    reporter.report_task.assert_any_call(
        pipeline_task="object_task",
        task_id="test_task_start.ObjectTask",
        run_id=run_id,
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
        serializable_task_object=None,
    )

    assert f"Object {user.pk}" in caplog.text


def test_task_object_accessible__django_object(caplog):
    reporter = Mock()
    user = fake_user()

    class ObjectTask(Task):
        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert isinstance(self.task_object, User)
            with caplog.at_level(logging.INFO):
                logger.info(f"Object {self.task_object.pk}")

    task = ObjectTask({})
    task.pipeline_task = "object_task"
    run_id = str(uuid.uuid4())

    task.start(
        pipeline_id="pipeline",
        run_id=run_id,
        input_data={},
        reporter=reporter,
        serializable_pipeline_object=None,
        serializable_task_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
    )

    reporter.report_task.assert_any_call(
        pipeline_task="object_task",
        task_id="test_task_start.ObjectTask",
        run_id=run_id,
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
    )

    assert f"Object {user.pk}" in caplog.text


def test_task_object_accessible__non_django_object(caplog):
    reporter = Mock()
    user = fake_user()

    class ObjectTask(Task):
        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert isinstance(self.task_object, User)
            with caplog.at_level(logging.INFO):
                logger.info(f"Object {self.task_object.pk}")

    task = ObjectTask({})
    task.pipeline_task = "object_task"
    run_id = str(uuid.uuid4())

    task.start(
        pipeline_id="pipeline",
        run_id=run_id,
        input_data={},
        reporter=reporter,
        serializable_pipeline_object=None,
        serializable_task_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
    )

    reporter.report_task.assert_any_call(
        pipeline_task="object_task",
        task_id="test_task_start.ObjectTask",
        run_id=run_id,
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
    )

    assert f"Object {user.pk}" in caplog.text

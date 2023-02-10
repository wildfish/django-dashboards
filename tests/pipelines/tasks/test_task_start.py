import logging
from unittest import mock
from unittest.mock import Mock

from django.contrib.auth.models import User

import pytest
from model_bakery import baker
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

    pipeline_execution = baker.make_recipe(
        "pipelines.fake_pipeline_execution", input_data={"value": 1}
    )
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result", execution=pipeline_execution
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution",
        task_id=task.get_id(),
        pipeline_result=pipeline_result,
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result", execution=task_execution
    )

    with pytest.raises(InputValidationError):
        task.start(
            task_result,
            reporter=reporter,
        )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.VALIDATION_ERROR,
        "Changed state to VALIDATION_ERROR - Input data was provided when no input type was specified",
    )
    task.run_body.assert_not_called()


def test_input_data_does_not_match_the_input_type___error_is_reported_run_is_not_called():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()

    pipeline_execution = baker.make_recipe(
        "pipelines.fake_pipeline_execution", input_data={"value": "foo"}
    )
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result", execution=pipeline_execution
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution",
        task_id=task.get_id(),
        pipeline_result=pipeline_result,
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result", execution=task_execution
    )

    with pytest.raises(InputValidationError):
        task.start(
            task_result,
            reporter=reporter,
        )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.VALIDATION_ERROR,
        'Changed state to VALIDATION_ERROR - [\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]',
    )
    task.run_body.assert_not_called()


def test_input_data_matches_the_input_type___run_is_called_with_the_cleaned_data():
    reporter = Mock()

    task = make_fake_task(input_type=InputType)()

    pipeline_execution = baker.make_recipe(
        "pipelines.fake_pipeline_execution", input_data={"value": "1"}
    )
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result", execution=pipeline_execution
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution",
        task_id=task.get_id(),
        pipeline_result=pipeline_result,
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result", execution=task_execution
    )

    task.start(
        task_result,
        reporter=reporter,
    )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.RUNNING,
        mock.ANY,
    )
    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.DONE,
        mock.ANY,
    )
    task.run_body.assert_called_once_with({"value": 1})


def test_input_data_and_type_are_none___run_is_called_with_none():
    reporter = Mock()

    task = make_fake_task(input_type=None)()

    pipeline_execution = baker.make_recipe("pipelines.fake_pipeline_execution")
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result", execution=pipeline_execution
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution",
        task_id=task.get_id(),
        pipeline_result=pipeline_result,
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result", execution=task_execution
    )

    task.start(
        task_result,
        reporter=reporter,
    )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.RUNNING,
        mock.ANY,
    )
    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.DONE,
        mock.ANY,
    )
    task.run_body.assert_called_once_with(None)


def test_errors_at_runtime___task_is_recorded_as_error():
    reporter = Mock()

    class ErroringTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            raise Exception("Some bad error")

    task = ErroringTask({})

    pipeline_execution = baker.make_recipe("pipelines.fake_pipeline_execution")
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result", execution=pipeline_execution
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution",
        task_id=task.get_id(),
        pipeline_result=pipeline_result,
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result", execution=task_execution
    )

    with pytest.raises(Exception):
        task.start(
            task_result,
            reporter=reporter,
        )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.RUNTIME_ERROR,
        "Changed state to RUNTIME_ERROR - Some bad error",
    )


def test_pipeline_object_accessible__django_object(caplog):
    reporter = Mock()
    user = fake_user()

    class ObjectTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert isinstance(self.pipeline_object, User)
            with caplog.at_level(logging.INFO):
                logger.info(f"Object {self.pipeline_object.pk}")

    task = ObjectTask({})

    pipeline_execution = baker.make_recipe("pipelines.fake_pipeline_execution")
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result",
        execution=pipeline_execution,
        serializable_pipeline_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution",
        task_id=task.get_id(),
        pipeline_result=pipeline_result,
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result", execution=task_execution
    )

    task.start(
        task_result,
        reporter=reporter,
    )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.DONE,
        mock.ANY,
    )

    assert f"Object {user.pk}" in caplog.text


def test_pipeline_object_accessible__non_django_object(caplog):
    reporter = Mock()
    user = fake_user()

    class ObjectTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert isinstance(self.pipeline_object, User)
            with caplog.at_level(logging.INFO):
                logger.info(f"Object {self.pipeline_object.pk}")

    task = ObjectTask({})

    pipeline_execution = baker.make_recipe("pipelines.fake_pipeline_execution")
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result",
        execution=pipeline_execution,
        serializable_pipeline_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution",
        task_id=task.get_id(),
        pipeline_result=pipeline_result,
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result", execution=task_execution
    )

    task.start(
        task_result,
        reporter=reporter,
    )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.DONE,
        mock.ANY,
    )

    assert f"Object {user.pk}" in caplog.text


def test_task_object_accessible__django_object(caplog):
    reporter = Mock()
    user = fake_user()

    class ObjectTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert isinstance(self.task_object, User)
            with caplog.at_level(logging.INFO):
                logger.info(f"Object {self.task_object.pk}")

    task = ObjectTask({})

    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution", task_id=task.get_id()
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result",
        execution=task_execution,
        serializable_task_object={
            "pk": user.pk,
            "model_name": "user",
            "app_label": "auth",
        },
    )

    task.start(
        task_result,
        reporter=reporter,
    )

    reporter.report_context_object.assert_any_call(
        task_result, PipelineTaskStatus.DONE, mock.ANY
    )

    assert f"Object {user.pk}" in caplog.text


def test_task_object_accessible__non_django_object(caplog):
    reporter = Mock()

    class ObjectTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, pipeline_id="pipeline", run_id="123", cleaned_data=None):
            assert self.task_object == {"obj": 1}
            with caplog.at_level(logging.INFO):
                logger.info("Object 1")

    task = ObjectTask({})

    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution", task_id=task.get_id()
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result",
        execution=task_execution,
        serializable_task_object={"obj": 1},
    )

    task.start(
        task_result,
        reporter=reporter,
    )

    reporter.report_context_object.assert_any_call(
        task_result,
        PipelineTaskStatus.DONE,
        mock.ANY,
    )

    assert "Object 1" in caplog.text

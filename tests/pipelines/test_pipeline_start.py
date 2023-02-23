import uuid
from unittest.mock import Mock

import pytest
from pydantic import BaseModel

from tests.dashboards.fakes import fake_user
from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.models import OrmPipelineExecution
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.base import ConfigValidationError, Task, TaskConfig


pytest_plugins = [
    "tests.pipelines.fixtures",
]

pytestmark = pytest.mark.django_db


def test_one_task_has_a_bad_config___error_is_reported_runner_is_not_started_tasks_are_marked_as_cancelled():
    class BadConfig(Task):
        class ConfigType(TaskConfig):
            value: int

        class Meta:
            app_label = "pipelinetest"

    class GoodConfig(Task):
        class ConfigType(TaskConfig):
            value: int

        class Meta:
            app_label = "pipelinetest"

    with pytest.raises(ConfigValidationError) as e:

        class TestPipeline(Pipeline):
            bad = BadConfig(config={"value": "foo"})
            good = GoodConfig(config={"value": "1"})

            class Meta:
                app_label = "pipelinetest"

    assert (
        str(e.value)
        == '[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]'
    )


def test_all_tasks_have_a_good_config___runner_is_started_tasks_are_marked_as_pending():
    reporter = Mock()
    runner = Mock()
    runner.start.return_value = True

    class GoodConfigA(Task):
        class ConfigType(TaskConfig):
            value: int

        class Meta:
            app_label = "pipelinetest"

    class GoodConfigB(Task):
        class ConfigType(TaskConfig):
            value: int

        class Meta:
            app_label = "pipelinetest"

    class TestPipeline(Pipeline):
        good = GoodConfigA(config={"value": "0"})
        also_good = GoodConfigB(config={"value": "1"})

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()
    run_id = str(uuid.uuid4())
    assert (
        pipeline.start(run_id=run_id, input_data={}, runner=runner, reporter=reporter)
        is True
    )

    pipeline_execution = OrmPipelineExecution.objects.first()
    [pipeline_result] = pipeline_execution.get_pipeline_results()
    [task_a_execution, task_b_execution] = pipeline_result.get_task_executions()
    [task_a_result] = task_a_execution.get_task_results()
    [task_b_result] = task_b_execution.get_task_results()

    reporter.report_pipeline_execution(
        pipeline_execution, PipelineTaskStatus.PENDING, "Pipeline is waiting to start"
    )
    reporter.report_pipeline_result(
        pipeline_result, PipelineTaskStatus.PENDING, "Pipeline is waiting to start"
    )
    reporter.report_task_execution(
        task_a_execution, PipelineTaskStatus.PENDING, "Task is waiting to start"
    )
    reporter.report_task_result(
        task_a_result, PipelineTaskStatus.PENDING, "Task is waiting to start"
    )
    reporter.report_task_execution(
        task_b_execution, PipelineTaskStatus.PENDING, "Task is waiting to start"
    )
    reporter.report_task_result(
        task_b_result, PipelineTaskStatus.PENDING, "Task is waiting to start"
    )


def test_all_tasks_have_a_good_config_and_input_data___runner_is_started_with_input_data():
    reporter = Mock()
    runner = Mock()
    runner.start.return_value = True

    class GoodConfigA(Task):
        class ConfigType(TaskConfig):
            value: int

        class InputType(BaseModel):
            message: str

        class Meta:
            app_label = "pipelinetest"

    class GoodConfigB(Task):
        class ConfigType(TaskConfig):
            value: int

        class Meta:
            app_label = "pipelinetest"

    class TestPipeline(Pipeline):
        good = GoodConfigA(config={"value": "0"})
        also_good = GoodConfigB(config={"value": "1"})

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()
    run_id = str(uuid.uuid4())
    assert (
        pipeline.start(
            run_id=run_id,
            input_data={"message": "something"},
            runner=runner,
            reporter=reporter,
        )
        is True
    )

    assert OrmPipelineExecution.objects.first().input_data == {"message": "something"}


def test_tasks_has_a_missing_parent___error_is_raised():
    reporter = Mock()
    runner = Mock()

    class BadConfig(Task):
        class Meta:
            app_label = "pipelinetest"

    class GoodConfig(Task):
        class Meta:
            app_label = "pipelinetest"

    class TestPipeline(Pipeline):
        bad = BadConfig()
        good = GoodConfig()

        ordering = {"bad": ["missing"]}

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()
    run_id = str(uuid.uuid4())

    with pytest.raises(Exception):
        pipeline.start(run_id=run_id, input_data={}, runner=runner, reporter=reporter)

    runner.start.assert_not_called()

    pipeline_execution = OrmPipelineExecution.objects.first()

    reporter.report_pipeline_execution(
        pipeline_execution,
        PipelineTaskStatus.PENDING,
        "One or more of the parent ids are not in the pipeline",
    )


def test_pipeline__iterator__all_tasks_have_a_good_config___runner_is_started_tasks_are_marked_as_pending():
    reporter = Mock()
    runner = Mock()
    runner.start.return_value = True

    class GoodConfigA(Task):
        class ConfigType(TaskConfig):
            value: int

        class Meta:
            app_label = "pipelinetest"

    class GoodConfigB(Task):
        class ConfigType(TaskConfig):
            value: int

        class Meta:
            app_label = "pipelinetest"

    class TestPipeline(Pipeline):
        good = GoodConfigA(config={"value": "0"})
        also_good = GoodConfigB(config={"value": "1"})

        @classmethod
        def get_iterator(cls):
            return range(0, 2)

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()
    run_id = str(uuid.uuid4())
    assert (
        pipeline.start(run_id=run_id, input_data={}, runner=runner, reporter=reporter)
        is True
    )

    pipeline_execution = OrmPipelineExecution.objects.first()
    [pipeline_result_a, pipeline_result_b] = pipeline_execution.get_pipeline_results()
    [a_a_execution, a_b_execution] = pipeline_result_a.get_task_executions()
    [a_a_result] = a_a_execution.get_task_results()
    [a_b_result] = a_b_execution.get_task_results()
    [b_a_execution, b_b_execution] = pipeline_result_b.get_task_executions()
    [b_a_result] = b_a_execution.get_task_results()
    [b_b_result] = b_b_execution.get_task_results()

    assert pipeline_execution.status == PipelineTaskStatus.PENDING.value

    assert pipeline_result_a.status == PipelineTaskStatus.PENDING.value
    assert a_a_execution.status == PipelineTaskStatus.PENDING.value
    assert a_a_result.status == PipelineTaskStatus.PENDING.value
    assert a_b_execution.status == PipelineTaskStatus.PENDING.value
    assert a_b_result.status == PipelineTaskStatus.PENDING.value

    assert pipeline_result_a.status == PipelineTaskStatus.PENDING.value
    assert b_a_execution.status == PipelineTaskStatus.PENDING.value
    assert b_a_result.status == PipelineTaskStatus.PENDING.value
    assert b_b_execution.status == PipelineTaskStatus.PENDING.value
    assert b_b_result.status == PipelineTaskStatus.PENDING.value

    runner.start.assert_called_once_with(pipeline_execution, reporter=reporter)


def test_pipeline___model__all_tasks_have_a_good_config___runner_is_started_tasks_are_marked_as_pending(
    test_model_pipeline,
):
    reporter = Mock()
    runner = Mock()
    users = fake_user(_quantity=2)

    runner.start.return_value = True

    pipeline = test_model_pipeline()
    run_id = str(uuid.uuid4())
    assert (
        pipeline.start(run_id=run_id, input_data={}, runner=runner, reporter=reporter)
        is True
    )

    pipeline_execution = OrmPipelineExecution.objects.first()
    [pipeline_result_a, pipeline_result_b] = pipeline_execution.get_pipeline_results()
    [task_execution_a] = pipeline_result_a.get_task_executions()
    [task_result_a] = task_execution_a.get_task_results()
    [task_execution_b] = pipeline_result_b.get_task_executions()
    [task_result_b] = task_execution_b.get_task_results()

    assert pipeline_execution.status == PipelineTaskStatus.PENDING.value

    assert pipeline_result_a.status == PipelineTaskStatus.PENDING.value
    assert task_execution_a.status == PipelineTaskStatus.PENDING.value
    assert task_result_a.status == PipelineTaskStatus.PENDING.value
    assert task_result_a.get_pipeline_object() == users[0]

    assert pipeline_result_b.status == PipelineTaskStatus.PENDING.value
    assert task_execution_b.status == PipelineTaskStatus.PENDING.value
    assert task_result_b.status == PipelineTaskStatus.PENDING.value
    assert task_result_a.get_pipeline_object() == users[0]

    runner.start.assert_called_once_with(pipeline_execution, reporter=reporter)


def test_pipeline___model_qs__all_tasks_have_a_good_config___runner_is_started_tasks_are_marked_as_pending(
    test_model_pipeline_qs,
):
    reporter = Mock()
    runner = Mock()
    users = fake_user(_quantity=2)

    runner.start.return_value = True

    pipeline = test_model_pipeline_qs()
    run_id = str(uuid.uuid4())
    assert (
        pipeline.start(run_id=run_id, input_data={}, runner=runner, reporter=reporter)
        is True
    )

    pipeline_execution = OrmPipelineExecution.objects.first()
    [pipeline_result_a, pipeline_result_b] = pipeline_execution.get_pipeline_results()
    [task_execution_a] = pipeline_result_a.get_task_executions()
    [task_result_a] = task_execution_a.get_task_results()
    [task_execution_b] = pipeline_result_b.get_task_executions()
    [task_result_b] = task_execution_b.get_task_results()

    assert pipeline_execution.status == PipelineTaskStatus.PENDING.value

    assert pipeline_result_a.status == PipelineTaskStatus.PENDING.value
    assert task_execution_a.status == PipelineTaskStatus.PENDING.value
    assert task_result_a.status == PipelineTaskStatus.PENDING.value
    assert task_result_a.get_pipeline_object() == users[0]

    assert pipeline_result_b.status == PipelineTaskStatus.PENDING.value
    assert task_execution_b.status == PipelineTaskStatus.PENDING.value
    assert task_result_b.status == PipelineTaskStatus.PENDING.value
    assert task_result_a.get_pipeline_object() == users[0]

    runner.start.assert_called_once_with(pipeline_execution, reporter=reporter)

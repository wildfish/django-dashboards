import uuid
from unittest.mock import Mock

import pytest
from pydantic import BaseModel

from datorum_pipelines import BasePipeline, BaseTask, BaseTaskConfig, PipelineTaskStatus
from datorum_pipelines.tasks.base import ConfigValidationError


pytestmark = pytest.mark.django_db


def test_one_task_has_a_bad_config___error_is_reported_runner_is_not_started_tasks_are_marked_as_cancelled():
    class BadConfig(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

    class GoodConfig(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

    with pytest.raises(ConfigValidationError) as e:

        class Pipeline(BasePipeline):
            bad = BadConfig(config={"value": "foo"})
            good = GoodConfig(config={"value": "1"})

            class Meta:
                title = "Test Pipeline"

    assert (
        str(e.value)
        == '[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]'
    )


def test_all_tasks_have_a_good_config___runner_is_started_tasks_are_marked_as_pending():
    reporter = Mock()
    runner = Mock()
    runner.start.return_value = True

    class GoodConfigA(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

    class GoodConfigB(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

    class Pipeline(BasePipeline):
        good = GoodConfigA(config={"value": "0"})
        also_good = GoodConfigB(config={"value": "1"})

        class Meta:
            title = "Test Pipeline"

    pipeline = Pipeline()
    run_id = str(uuid.uuid4())
    assert (
        pipeline.start(run_id=run_id, input_data={}, runner=runner, reporter=reporter)
        is True
    )

    reporter.report_task.assert_any_call(
        pipeline_task="good",
        task_id="test_pipeline_start.GoodConfigA",
        status=PipelineTaskStatus.PENDING,
        message="Task is waiting to start",
    )
    reporter.report_task.assert_any_call(
        pipeline_task="also_good",
        task_id="test_pipeline_start.GoodConfigB",
        status=PipelineTaskStatus.PENDING,
        message="Task is waiting to start",
    )

    runner.start.assert_called_once_with(
        pipeline_id="test_pipeline_start.Pipeline",
        run_id=run_id,
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
    )


def test_all_tasks_have_a_good_config_and_input_data___runner_is_started_with_input_data():
    reporter = Mock()
    runner = Mock()
    runner.start.return_value = True

    class GoodConfigA(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

        class InputType(BaseModel):
            message: str

    class GoodConfigB(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

    class Pipeline(BasePipeline):
        good = GoodConfigA(config={"value": "0"})
        also_good = GoodConfigB(config={"value": "1"})

        class Meta:
            title = "Test Pipeline"

    pipeline = Pipeline()
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

    reporter.report_task.assert_any_call(
        pipeline_task="good",
        task_id="test_pipeline_start.GoodConfigA",
        status=PipelineTaskStatus.PENDING,
        message="Task is waiting to start",
    )

    reporter.report_task.assert_any_call(
        pipeline_task="also_good",
        task_id="test_pipeline_start.GoodConfigB",
        status=PipelineTaskStatus.PENDING,
        message="Task is waiting to start",
    )

    runner.start.assert_called_once_with(
        pipeline_id="test_pipeline_start.Pipeline",
        run_id=run_id,
        tasks=pipeline.cleaned_tasks,
        input_data={"message": "something"},
        reporter=reporter,
    )


def test_tasks_has_a_missing_parent___error_is_raised():
    reporter = Mock()
    runner = Mock()

    class BadConfig(BaseTask):
        pass

    class GoodConfig(BaseTask):
        pass

    class Pipeline(BasePipeline):
        bad = BadConfig(
            config={
                "parents": ["missing"],
            }
        )
        good = GoodConfig(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = Pipeline()

    assert (
        pipeline.start(
            run_id=str(uuid.uuid4()), input_data={}, runner=runner, reporter=reporter
        )
        is False
    )
    reporter.report_task.assert_any_call(
        pipeline_task="bad",
        task_id="test_pipeline_start.BadConfig",
        status=PipelineTaskStatus.CONFIG_ERROR,
        message="One or more of the parent ids are not in the pipeline",
    )

    runner.start.assert_not_called()

from unittest.mock import Mock

from pydantic import BaseModel

from datorum_pipelines import (
    BasePipeline,
    BaseTask,
    BaseTaskConfig,
    PipelineConfigEntry,
    PipelineTaskStatus,
)


def test_one_task_has_a_bad_config___error_is_reported_runner_is_not_started_tasks_are_marked_as_cancelled():
    reporter = Mock()
    runner = Mock()

    class BadConfig(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

    class GoodConfig(BaseTask):
        class ConfigType(BaseTaskConfig):
            value: int

    pipeline = BasePipeline(
        "id",
        [
            PipelineConfigEntry(
                name="BadConfig",
                id="bad_config",
                config={"value": "foo"},
            ),
            PipelineConfigEntry(
                name="GoodConfig",
                id="good_config",
                config={"value": "1"},
            ),
        ],
    )

    assert pipeline.start({}, runner, reporter) is False
    reporter.report_task.assert_any_call(
        "bad_config",
        PipelineTaskStatus.CONFIG_ERROR,
        '[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]',
    )
    reporter.report_task.assert_any_call(
        "good_config",
        PipelineTaskStatus.CANCELLED,
        "Tasks cancelled due to an error in the pipeline config",
    )
    runner.start.assert_not_called()


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

    pipeline = BasePipeline(
        "id",
        [
            PipelineConfigEntry(
                name="GoodConfigA",
                id="good_config_a",
                config={"value": "0"},
            ),
            PipelineConfigEntry(
                name="GoodConfigB",
                id="good_config_b",
                config={"value": "1"},
            ),
        ],
    )

    assert pipeline.start({}, runner, reporter) is True
    reporter.report_task.assert_any_call(
        "good_config_a",
        PipelineTaskStatus.PENDING,
        "Task is waiting to start",
    )
    reporter.report_task.assert_any_call(
        "good_config_b",
        PipelineTaskStatus.PENDING,
        "Task is waiting to start",
    )
    runner.start.assert_called_once_with("id", pipeline.cleaned_tasks, {}, reporter)


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

    pipeline = BasePipeline(
        "id",
        [
            PipelineConfigEntry(
                name="GoodConfigA",
                id="good_config_a",
                config={"value": "0"},
            ),
            PipelineConfigEntry(
                name="GoodConfigB",
                id="good_config_b",
                config={"value": "1"},
            ),
        ],
    )

    assert pipeline.start({"message": "something"}, runner, reporter) is True
    reporter.report_task.assert_any_call(
        "good_config_a",
        PipelineTaskStatus.PENDING,
        "Task is waiting to start",
    )
    reporter.report_task.assert_any_call(
        "good_config_b",
        PipelineTaskStatus.PENDING,
        "Task is waiting to start",
    )
    runner.start.assert_called_once_with(
        "id", pipeline.cleaned_tasks, {"message": "something"}, reporter
    )


def test_tasks_has_a_missing_parent___error_is_raised():
    reporter = Mock()
    runner = Mock()

    class BadConfig(BaseTask):
        pass

    class GoodConfig(BaseTask):
        pass

    pipeline = BasePipeline(
        "id",
        [
            PipelineConfigEntry(
                name="BadConfig",
                id="bad_config",
                config={
                    "parents": ["missing"],
                },
            ),
            PipelineConfigEntry(
                name="GoodConfig",
                id="good_config",
                config={},
            ),
        ],
    )

    assert pipeline.start({}, runner, reporter) is False
    reporter.report_task.assert_any_call(
        "bad_config",
        PipelineTaskStatus.CONFIG_ERROR,
        "One or more of the parent labels are not in the pipeline",
    )
    reporter.report_task.assert_any_call(
        "good_config",
        PipelineTaskStatus.CANCELLED,
        "Tasks cancelled due to an error in the pipeline config",
    )
    runner.start.assert_not_called()

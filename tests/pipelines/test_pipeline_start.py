import uuid
from unittest.mock import Mock, call

import pytest
from pydantic import BaseModel

from tests.dashboards.fakes import fake_user
from wildcoeus.pipelines.base import Pipeline
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

    class GoodConfig(Task):
        class ConfigType(TaskConfig):
            value: int

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

    class GoodConfigB(Task):
        class ConfigType(TaskConfig):
            value: int

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

    reporter.report_task.assert_any_call(
        pipeline_task="good",
        task_id="test_pipeline_start.GoodConfigA",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )
    reporter.report_task.assert_any_call(
        pipeline_task="also_good",
        task_id="test_pipeline_start.GoodConfigB",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )

    runner.start.assert_called_once_with(
        pipeline_id="test_pipeline_start.TestPipeline",
        run_id=run_id,
        pipeline_object=None,
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
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

    class GoodConfigB(Task):
        class ConfigType(TaskConfig):
            value: int

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

    reporter.report_task.assert_any_call(
        pipeline_task="good",
        task_id="test_pipeline_start.GoodConfigA",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )

    reporter.report_task.assert_any_call(
        pipeline_task="also_good",
        task_id="test_pipeline_start.GoodConfigB",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )

    runner.start.assert_called_once_with(
        pipeline_id="test_pipeline_start.TestPipeline",
        run_id=run_id,
        pipeline_object=None,
        tasks=pipeline.cleaned_tasks,
        input_data={"message": "something"},
        reporter=reporter,
    )


def test_tasks_has_a_missing_parent___error_is_raised():
    reporter = Mock()
    runner = Mock()

    class BadConfig(Task):
        pass

    class GoodConfig(Task):
        pass

    class TestPipeline(Pipeline):
        bad = BadConfig(
            config={
                "parents": ["missing"],
            }
        )
        good = GoodConfig(config={})

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()
    run_id = str(uuid.uuid4())

    assert (
        pipeline.start(run_id=run_id, input_data={}, runner=runner, reporter=reporter)
        is False
    )
    reporter.report_task.assert_any_call(
        pipeline_task="bad",
        task_id="test_pipeline_start.BadConfig",
        run_id=run_id,
        status=PipelineTaskStatus.CONFIG_ERROR.value,
        message="One or more of the parent ids are not in the pipeline",
    )

    runner.start.assert_not_called()


def test_pipeline__iterator__all_tasks_have_a_good_config___runner_is_started_tasks_are_marked_as_pending():
    reporter = Mock()
    runner = Mock()
    runner.start.return_value = True

    class GoodConfigA(Task):
        class ConfigType(TaskConfig):
            value: int

    class GoodConfigB(Task):
        class ConfigType(TaskConfig):
            value: int

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

    reporter.report_task.assert_any_call(
        pipeline_task="good",
        task_id="test_pipeline_start.GoodConfigA",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )
    reporter.report_task.assert_any_call(
        pipeline_task="also_good",
        task_id="test_pipeline_start.GoodConfigB",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )

    c1 = call(
        pipeline_id="test_pipeline_start.TestPipeline",
        run_id=run_id,
        pipeline_object=0,
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
    )
    c2 = call(
        pipeline_id="test_pipeline_start.TestPipeline",
        run_id=run_id,
        pipeline_object=1,
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
    )
    calls = [c1, c2]

    runner.start.assert_has_calls(calls)


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

    reporter.report_task.assert_any_call(
        pipeline_task="first",
        task_id="tests.pipelines.app.pipelines.TestTask",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )

    c1 = call(
        pipeline_id=pipeline.get_id(),
        run_id=run_id,
        pipeline_object=users[0],
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
    )
    c2 = call(
        pipeline_id=pipeline.get_id(),
        run_id=run_id,
        pipeline_object=users[1],
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
    )
    calls = [c1, c2]

    runner.start.assert_has_calls(calls)


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

    reporter.report_task.assert_any_call(
        pipeline_task="first",
        task_id="tests.pipelines.app.pipelines.TestTask",
        run_id=run_id,
        status=PipelineTaskStatus.PENDING.value,
        message="Task is waiting to start",
    )

    c1 = call(
        pipeline_id=pipeline.get_id(),
        run_id=run_id,
        pipeline_object=users[0],
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
    )
    c2 = call(
        pipeline_id=pipeline.get_id(),
        run_id=run_id,
        pipeline_object=users[1],
        tasks=pipeline.cleaned_tasks,
        input_data={},
        reporter=reporter,
    )
    calls = [c1, c2]

    runner.start.assert_has_calls(calls)

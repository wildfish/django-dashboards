from unittest.mock import Mock

from pydantic import BaseModel

from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task
from wildcoeus.pipelines.tasks.registry import task_registry


def test_task_class_created_without_name___it_is_added_to_the_registry_using_the_classname():
    class TestTask(Task):
        pass

    assert ["test_registry.TestTask"] == list(task_registry.tasks.keys())
    assert task_registry.tasks["test_registry.TestTask"] == TestTask


def test_request_to_load_a_task_that_isnt_registered___error_is_reported():
    class TestTask(Task):
        pass

    reporter = Mock()

    task = task_registry.load_task_from_id(
        pipeline_task="fake",
        task_id="missing_task_id",
        run_id="123543455435",
        config={},
        reporter=reporter,
    )

    assert task is None
    reporter.report_task.assert_called_once_with(
        pipeline_task="fake",
        task_id="missing_task_id",
        run_id="123543455435",
        status=PipelineTaskStatus.CONFIG_ERROR.value,
        message="No task named missing_task_id is registered",
    )


def test_request_to_load_a_task_that_exists_with_a_bad_config___error_is_reported():
    class TestTaskConfigType(BaseModel):
        value: int

    class TestTask(Task):
        ConfigType = TestTaskConfigType

    reporter = Mock()

    task = task_registry.load_task_from_id(
        pipeline_task="fake",
        task_id="missing_task_id",
        run_id="123543455435",
        config={"value": "foo"},
        reporter=reporter,
    )

    assert task is None
    reporter.report_task.assert_called_once_with(
        pipeline_task="fake",
        task_id="missing_task_id",
        run_id="123543455435",
        status=PipelineTaskStatus.CONFIG_ERROR.value,
        message="No task named missing_task_id is registered",
    )


def test_request_to_load_a_task_that_exists_with_a_valid_config___task_is_loaded():
    class TestTaskConfigType(BaseModel):
        value: int

    class TestTask(Task):
        ConfigType = TestTaskConfigType

    reporter = Mock()
    task = task_registry.load_task_from_id(
        pipeline_task="fake",
        task_id="test_registry.TestTask",
        run_id="123543455435",
        config={"value": 1},
        reporter=reporter,
    )

    assert isinstance(task, TestTask)
    assert task.cleaned_config == TestTaskConfigType(value=1)

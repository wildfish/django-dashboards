from unittest.mock import Mock

import pytest
from pydantic import BaseModel

from datorum_pipelines import BaseTask
from datorum_pipelines.reporter import PipelineTaskStatus
from datorum_pipelines.tasks.registry import RegistryError, task_registry


@pytest.fixture(autouse=True)
def reset_registry():
    task_registry.reset()


def test_task_class_created_without_name___it_is_added_to_the_registry_using_the_classname():
    class TestTask(BaseTask):
        pass

    assert ["TestTask"] == list(task_registry.tasks.keys())
    assert task_registry.tasks["TestTask"] == TestTask


def test_task_class_created_with_name___it_is_added_to_the_registry_using_the_overridden_name():
    class TestTask(BaseTask):
        name = "Other Name"

    assert ["Other Name"] == list(task_registry.tasks.keys())
    assert task_registry.tasks["Other Name"] == TestTask


def test_multiple_tasks_created_with_the_same_name___error_is_raised():
    with pytest.raises(
        RegistryError,
        match="Multiple tasks named AnotherTestTask have been registered.",
    ):

        class AnotherTestTask(BaseTask):
            pass

        class YetAnotherTestTask(BaseTask):
            name = "AnotherTestTask"


def test_request_to_load_a_task_that_isnt_registered___error_is_reported():
    class TestTask(BaseTask):
        pass

    reporter = Mock()

    task = task_registry.load("DifferentTestTask", "missing_task_id", {}, reporter)

    assert task is None
    reporter.report_task.assert_called_once_with(
        "missing_task_id",
        PipelineTaskStatus.CONFIG_ERROR,
        "No task named DifferentTestTask is registered",
    )


def test_request_to_load_a_task_that_exists_with_a_config_when_non_is_expected___error_is_reported():
    class TestTask(BaseTask):
        pass

    reporter = Mock()

    task = task_registry.load("TestTask", "missing_task_id", {"value": 1}, reporter)

    assert task is None
    reporter.report_task.assert_called_once_with(
        "missing_task_id",
        PipelineTaskStatus.CONFIG_ERROR,
        "Config was provided no config type was specified",
    )


def test_request_to_load_a_task_that_exists_with_a_bad_config___error_is_reported():
    class TestTaskConfigType(BaseModel):
        value: int

    class TestTask(BaseTask):
        ConfigType = TestTaskConfigType

    reporter = Mock()

    task = task_registry.load("TestTask", "missing_task_id", {"value": "foo"}, reporter)

    assert task is None
    reporter.report_task.assert_called_once_with(
        "missing_task_id",
        PipelineTaskStatus.CONFIG_ERROR,
        '[\n{\n"loc": [\n"value"\n],\n"msg": "value is not a valid integer",\n"type": "type_error.integer"\n}\n]',
    )


def test_request_to_load_a_task_that_exists_with_a_valid_config___task_is_loaded():
    class TestTaskConfigType(BaseModel):
        value: int

    class TestTask(BaseTask):
        ConfigType = TestTaskConfigType

    reporter = Mock()

    task = task_registry.load("TestTask", "missing_task_id", {"value": 1}, reporter)

    assert isinstance(task, TestTask)
    assert task.cleaned_config == TestTaskConfigType(value=1)

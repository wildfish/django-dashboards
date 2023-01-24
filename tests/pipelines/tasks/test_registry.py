import pytest
from pydantic import BaseModel

from wildcoeus.pipelines.tasks import Task
from wildcoeus.pipelines.tasks.registry import task_registry


def test_task_class_created_without_name___it_is_added_to_the_registry_using_the_classname():
    class TestTask(Task):
        class Meta:
            app_label = "pipelinetest"

    assert "pipelinetest.TestTask" in [t.get_id() for t in task_registry.items]


def test_request_to_load_a_task_that_isnt_registered___error_is_reported():
    class TestTask(Task):
        class Meta:
            app_label = "pipelinetest"

    with pytest.raises(IndexError):
        task_registry.load_task_from_id(
            pipeline_task="fake",
            task_id="missing_task_id",
            config={},
        )


def test_request_to_load_a_task_that_exists_with_a_valid_config___task_is_loaded():
    class TestTaskConfigType(BaseModel):
        value: int

    class TestTask(Task):
        class Meta:
            app_label = "pipelinetest"

        ConfigType = TestTaskConfigType

    task = task_registry.load_task_from_id(
        pipeline_task="fake",
        task_id="pipelinetest.TestTask",
        config={"value": 1},
    )

    assert isinstance(task, TestTask)
    assert task.cleaned_config == TestTaskConfigType(value=1)

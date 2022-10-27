from unittest.mock import Mock

import pytest

from datorum.pipelines import BasePipeline, BaseTask, PipelineTaskStatus
from datorum.pipelines.runners.celery.runner import Runner


pytestmark = pytest.mark.django_db


def validate_pipeline_report(task, name, pipeline_id, status):
    assert task.name == name
    assert task.kwargs == {
        "pipeline_id": pipeline_id,
        "status": status,
        "message": status.value.title(),
    }


def validate_run_task(task, task_id, pipeline_id, input_data):
    assert task.name == "datorum.pipelines.runners.celery.tasks.run_task"
    assert list(task.kwargs.keys()) == [
        "task_id",
        "run_id",
        "pipeline_id",
        "input_data",
    ]
    assert task.kwargs["task_id"] == task_id
    assert task.kwargs["pipeline_id"] == pipeline_id
    assert task.kwargs["input_data"] == input_data


def test_task_have_no_parents___tasks_are_added_to_chain_in_configured_order():
    reporter = Mock()

    class TaskFirst(BaseTask):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(BaseTask):
        def run(self, *args, **kwargs):
            return True

    class Pipeline(BasePipeline):
        first = TaskFirst(config={})
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = Pipeline()

    chain = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert len(chain.tasks) == 4

    validate_pipeline_report(
        task=chain.tasks[0],
        name="datorum.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.RUNNING,
    )

    validate_run_task(
        task=chain.tasks[1],
        task_id="test_celery_runner.TaskFirst",
        pipeline_id="test_celery_runner.Pipeline",
        input_data={},
    )

    validate_run_task(
        task=chain.tasks[2],
        task_id="test_celery_runner.TaskSecond",
        pipeline_id="test_celery_runner.Pipeline",
        input_data={},
    )

    validate_pipeline_report(
        task=chain.tasks[3],
        name="datorum.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.DONE,
    )


def test_task_with_parents___tasks_are_added_to_chain_in_configured_order():
    reporter = Mock()

    class TaskFirst(BaseTask):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(BaseTask):
        def run(self, *args, **kwargs):
            return True

    class Pipeline(BasePipeline):
        first = TaskFirst(
            config={"parents": ["second"]}
        )  # Force first to run after second
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = Pipeline()

    chain = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert len(chain.tasks) == 4

    validate_pipeline_report(
        task=chain.tasks[0],
        name="datorum.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.RUNNING,
    )

    validate_run_task(
        task=chain.tasks[1],
        task_id="test_celery_runner.TaskSecond",
        pipeline_id="test_celery_runner.Pipeline",
        input_data={},
    )

    validate_run_task(
        task=chain.tasks[2],
        task_id="test_celery_runner.TaskFirst",
        pipeline_id="test_celery_runner.Pipeline",
        input_data={},
    )

    validate_pipeline_report(
        task=chain.tasks[3],
        name="datorum.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.DONE,
    )


def test_task__link_error_added():
    reporter = Mock()

    class TaskFirst(BaseTask):
        def run(self, *args, **kwargs):
            return True

    class Pipeline(BasePipeline):
        first = TaskFirst()

        class Meta:
            title = "Test Pipeline"

    pipeline = Pipeline()

    chain = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert (
        chain.options["link_error"][0].name
        == "datorum.pipelines.runners.celery.tasks.run_pipeline_report"
    )
    assert chain.options["link_error"][0].kwargs == {
        "pipeline_id": "test_celery_runner.Pipeline",
        "status": PipelineTaskStatus.RUNTIME_ERROR,
        "message": "Pipeline Error - remaining tasks cancelled",
    }

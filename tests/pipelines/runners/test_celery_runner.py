from unittest.mock import Mock

from django.contrib.auth.models import User

import pytest

from tests.dashboards.fakes import fake_user
from wildcoeus.pipelines import Pipeline, PipelineTaskStatus, Task
from wildcoeus.pipelines.base import ModelPipeline
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners.celery.runner import Runner


pytestmark = pytest.mark.django_db


def validate_pipeline_report(task, name, pipeline_id, status, instance_lookup=None):
    assert task.name == name
    assert task.kwargs == {
        "pipeline_id": pipeline_id,
        "status": status,
        "message": status.value.title(),
        "instance_lookup": instance_lookup,
    }


def validate_run_task(
    task, task_id, pipeline_id, input_data, instance_lookup=None, instance_model=None
):
    assert task.name == "wildcoeus.pipelines.runners.celery.tasks.run_task"
    assert list(task.kwargs.keys()) == [
        "task_id",
        "run_id",
        "pipeline_id",
        "input_data",
        "instance_lookup",
    ]
    assert task.kwargs["task_id"] == task_id
    assert task.kwargs["pipeline_id"] == pipeline_id
    assert task.kwargs["input_data"] == input_data
    assert task.kwargs["instance_lookup"] == instance_lookup


def test_task_have_no_parents___tasks_are_added_to_chain_in_configured_order():
    reporter = Mock()

    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TaskFirst(config={})
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    chain = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert len(chain.tasks) == 4

    validate_pipeline_report(
        task=chain.tasks[0],
        name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.RUNNING,
    )

    validate_run_task(
        task=chain.tasks[1],
        task_id="test_celery_runner.TaskFirst",
        pipeline_id="test_celery_runner.TestPipeline",
        input_data={},
    )

    validate_run_task(
        task=chain.tasks[2],
        task_id="test_celery_runner.TaskSecond",
        pipeline_id="test_celery_runner.TestPipeline",
        input_data={},
    )

    validate_pipeline_report(
        task=chain.tasks[3],
        name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.DONE,
    )


def test_task_with_parents___tasks_are_added_to_chain_in_configured_order():
    reporter = Mock()

    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TaskFirst(
            config={"parents": ["second"]}
        )  # Force first to run after second
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    chain = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert len(chain.tasks) == 4

    validate_pipeline_report(
        task=chain.tasks[0],
        name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.RUNNING,
    )

    validate_run_task(
        task=chain.tasks[1],
        task_id="test_celery_runner.TaskSecond",
        pipeline_id="test_celery_runner.TestPipeline",
        input_data={},
    )

    validate_run_task(
        task=chain.tasks[2],
        task_id="test_celery_runner.TaskFirst",
        pipeline_id="test_celery_runner.TestPipeline",
        input_data={},
    )

    validate_pipeline_report(
        task=chain.tasks[3],
        name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
        pipeline_id=pipeline.id,
        status=PipelineTaskStatus.DONE,
    )


def test_task__link_error_added():
    reporter = Mock()

    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TaskFirst()

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    chain = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert (
        chain.options["link_error"][0].name
        == "wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report"
    )
    assert chain.options["link_error"][0].kwargs == {
        "pipeline_id": "test_celery_runner.TestPipeline",
        "status": PipelineTaskStatus.RUNTIME_ERROR,
        "message": "Pipeline Error - remaining tasks cancelled",
        "instance_lookup": None,
    }


def test_model_pipeline__task_have_no_parents___tasks_are_added_to_chain_in_configured_order():
    reporter = Mock()
    users = [fake_user(username="a"), fake_user(username="b")]

    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(ModelPipeline):
        first = TaskFirst(config={})
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"
            queryset = User.objects.all()

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    chains = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert len(chains) == 2

    for i, chain in enumerate(chains):
        user = users[i]
        assert len(chain.tasks) == 4

        validate_pipeline_report(
            task=chain.tasks[0],
            name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
            pipeline_id=pipeline.id,
            status=PipelineTaskStatus.RUNNING,
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )

        validate_run_task(
            task=chain.tasks[1],
            task_id="test_celery_runner.TaskFirst",
            pipeline_id="test_celery_runner.TestPipeline",
            input_data={},
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )

        validate_run_task(
            task=chain.tasks[2],
            task_id="test_celery_runner.TaskSecond",
            pipeline_id="test_celery_runner.TestPipeline",
            input_data={},
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )

        validate_pipeline_report(
            task=chain.tasks[3],
            name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
            pipeline_id=pipeline.id,
            status=PipelineTaskStatus.DONE,
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )


def test_model_pipeline__task_with_parents___tasks_are_added_to_chain_in_configured_order():
    reporter = Mock()
    users = [fake_user(username="a"), fake_user(username="b")]

    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(ModelPipeline):
        first = TaskFirst(
            config={"parents": ["second"]}
        )  # Force first to run after second
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"
            queryset = User.objects.all()

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    chains = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert len(chains) == 2

    for i, chain in enumerate(chains):
        user = users[i]
        assert len(chain.tasks) == 4

        validate_pipeline_report(
            task=chain.tasks[0],
            name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
            pipeline_id=pipeline.id,
            status=PipelineTaskStatus.RUNNING,
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )

        validate_run_task(
            task=chain.tasks[1],
            task_id="test_celery_runner.TaskSecond",
            pipeline_id="test_celery_runner.TestPipeline",
            input_data={},
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )

        validate_run_task(
            task=chain.tasks[2],
            task_id="test_celery_runner.TaskFirst",
            pipeline_id="test_celery_runner.TestPipeline",
            input_data={},
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )

        validate_pipeline_report(
            task=chain.tasks[3],
            name="wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report",
            pipeline_id=pipeline.id,
            status=PipelineTaskStatus.DONE,
            instance_lookup={"app_label": "auth", "model_name": "user", "pk": user.pk},
        )


def test_model_pipeline__link_error_added():
    reporter = Mock()
    users = [fake_user(username="a"), fake_user(username="b")]

    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(ModelPipeline):
        first = TaskFirst()

        class Meta:
            title = "Test Pipeline"
            queryset = User.objects.all()

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    chains = pipeline.start(
        run_id="123", input_data={}, runner=Runner(), reporter=reporter
    )

    assert len(chains) == 2

    for i, chain in enumerate(chains):
        user = users[i]
        assert (
            chain.options["link_error"][0].name
            == "wildcoeus.pipelines.runners.celery.tasks.run_pipeline_report"
        )
        assert chain.options["link_error"][0].kwargs == {
            "pipeline_id": "test_celery_runner.TestPipeline",
            "status": PipelineTaskStatus.RUNTIME_ERROR,
            "message": "Pipeline Error - remaining tasks cancelled",
            "instance_lookup": {
                "app_label": "auth",
                "model_name": "user",
                "pk": user.pk,
            },
        }

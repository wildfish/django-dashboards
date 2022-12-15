import logging
from unittest.mock import Mock

from django.contrib.auth.models import User

import pytest

from tests.dashboards.fakes import fake_user
from wildcoeus.pipelines import Pipeline, Task
from wildcoeus.pipelines.base import ModelPipeline
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners.celery.runner import Runner
from wildcoeus.pipelines.runners.celery.tasks import run_pipeline
from wildcoeus.pipelines.tasks.base import ModelTask


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def celery_config():
    return {
        "broker_url": "memory://",
        "results_backend": "memory://",
        "task_always_eager": True,
    }


@pytest.fixture(autouse=True)
def logger(caplog):
    caplog.set_level(logging.INFO, logger="wildcoeus-pipelines")
    return caplog


def test_task_have_no_parents___tasks_are_added_to_chain_in_configured_order(
    celery_worker, logger
):
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

    run_pipeline(pipeline_id=pipeline.id, input_data={}, run_id="123")

    assert [
        "Pipeline test_celery_runner.TestPipeline changed to state PENDING: Pipeline is waiting to start",
        "Task first:test_celery_runner.TaskFirst changed to state PENDING: Task is waiting to start",
        "Task second:test_celery_runner.TaskSecond changed to state PENDING: Task is waiting to start",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Started",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running",
        "Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running",
        "Task first:test_celery_runner.TaskFirst changed to state DONE: Done",
        "Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running",
        "Task second:test_celery_runner.TaskSecond changed to state DONE: Done",
        "Pipeline test_celery_runner.TestPipeline changed to state DONE: Done",
    ] == [rec.message for rec in logger.records]


def test_task_with_parents___tasks_are_added_to_chain_in_configured_order(
    celery_worker, logger
):
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

    run_pipeline(pipeline_id=pipeline.id, input_data={}, run_id="123")

    assert [
        "Pipeline test_celery_runner.TestPipeline changed to state PENDING: Pipeline is waiting to start",
        "Task first:test_celery_runner.TaskFirst changed to state PENDING: Task is waiting to start",
        "Task second:test_celery_runner.TaskSecond changed to state PENDING: Task is waiting to start",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Started",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running",
        "Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running",
        "Task second:test_celery_runner.TaskSecond changed to state DONE: Done",
        "Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running",
        "Task first:test_celery_runner.TaskFirst changed to state DONE: Done",
        "Pipeline test_celery_runner.TestPipeline changed to state DONE: Done",
    ] == [rec.message for rec in logger.records]


def test_model_pipeline(celery_worker, logger):
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

    run_pipeline(pipeline_id=pipeline.id, input_data={}, run_id="123")

    user_one_for = f"| pipeline object: {{'pk': {users[0].pk}, 'app_label': 'auth', 'model_name': 'user'}}"
    user_two_for = f"| pipeline object: {{'pk': {users[1].pk}, 'app_label': 'auth', 'model_name': 'user'}}"

    assert [
        "Pipeline test_celery_runner.TestPipeline changed to state PENDING: Pipeline is waiting to start",
        "Task first:test_celery_runner.TaskFirst changed to state PENDING: Task is waiting to start",
        "Task second:test_celery_runner.TaskSecond changed to state PENDING: Task is waiting to start",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Started",
        f"Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running {user_one_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running {user_one_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state DONE: Done {user_one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {user_one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {user_one_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state DONE: Done {user_one_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running {user_two_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running {user_two_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state DONE: Done {user_two_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {user_two_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {user_two_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state DONE: Done {user_two_for}",
    ] == [rec.message for rec in logger.records]


def test_iterator_pipeline(celery_worker, logger):
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

        @classmethod
        def get_iterator(cls):
            return [1, 2]

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    run_pipeline(pipeline_id=pipeline.id, input_data={}, run_id="123")

    one_for = f"| pipeline object: {{'obj': 1}}"
    two_for = f"| pipeline object: {{'obj': 2}}"

    assert [
        "Pipeline test_celery_runner.TestPipeline changed to state PENDING: Pipeline is waiting to start",
        "Task first:test_celery_runner.TaskFirst changed to state PENDING: Task is waiting to start",
        "Task second:test_celery_runner.TaskSecond changed to state PENDING: Task is waiting to start",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Started",
        f"Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running {one_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running {one_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state DONE: Done {one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {one_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state DONE: Done {one_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running {two_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running {two_for}",
        f"Task first:test_celery_runner.TaskFirst changed to state DONE: Done {two_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {two_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {two_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state DONE: Done {two_for}",
    ] == [rec.message for rec in logger.records]


def test_iterator__iterate_task(celery_worker, logger):
    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(Task):
        def run(self, *args, **kwargs):
            return True

        def get_iterator(cls):
            return [1, 2]

    class TestPipeline(Pipeline):
        first = TaskFirst(config={})
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    run_pipeline(pipeline_id=pipeline.id, input_data={}, run_id="123")

    one_for = f"| task object: {{'obj': 1}}"
    two_for = f"| task object: {{'obj': 2}}"

    assert [
        "Pipeline test_celery_runner.TestPipeline changed to state PENDING: Pipeline is waiting to start",
        "Task first:test_celery_runner.TaskFirst changed to state PENDING: Task is waiting to start",
        "Task second:test_celery_runner.TaskSecond changed to state PENDING: Task is waiting to start",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Started",
        f"Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running",
        f"Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running",
        f"Task first:test_celery_runner.TaskFirst changed to state DONE: Done",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {two_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {two_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state DONE: Done",
    ] == [rec.message for rec in logger.records]


def test_model__iterate_task(celery_worker, logger):
    users = [fake_user(username="a"), fake_user(username="b")]

    class TaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TaskSecond(ModelTask):
        def run(self, *args, **kwargs):
            return True

        class Meta:
            queryset = User.objects.all()

    class TestPipeline(Pipeline):
        first = TaskFirst(config={})
        second = TaskSecond(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    run_pipeline(pipeline_id=pipeline.id, input_data={}, run_id="123")

    user_one_for = f"| task object: {{'pk': {users[0].pk}, 'app_label': 'auth', 'model_name': 'user'}}"
    user_two_for = f"| task object: {{'pk': {users[1].pk}, 'app_label': 'auth', 'model_name': 'user'}}"

    assert [
        "Pipeline test_celery_runner.TestPipeline changed to state PENDING: Pipeline is waiting to start",
        "Task first:test_celery_runner.TaskFirst changed to state PENDING: Task is waiting to start",
        "Task second:test_celery_runner.TaskSecond changed to state PENDING: Task is waiting to start",
        "Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Started",
        f"Pipeline test_celery_runner.TestPipeline changed to state RUNNING: Running",
        f"Task first:test_celery_runner.TaskFirst changed to state RUNNING: Task is running",
        f"Task first:test_celery_runner.TaskFirst changed to state DONE: Done",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {user_one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {user_one_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state RUNNING: Task is running {user_two_for}",
        f"Task second:test_celery_runner.TaskSecond changed to state DONE: Done {user_two_for}",
        f"Pipeline test_celery_runner.TestPipeline changed to state DONE: Done",
    ] == [rec.message for rec in logger.records]


def test__task_to_celery_tasks__queue_defined():
    class TaskWithQueue(Task):
        def run(self, *args, **kwargs):
            return True

    class TaskWithoutQueue(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        with_queue = TaskWithQueue(config={"celery_queue": "else"})
        without_queue = TaskWithoutQueue(config={})

        class Meta:
            title = "Test Pipeline"

    with_queue_result = Runner()._task_to_celery_tasks(
        task=TestPipeline().tasks["with_queue"],
        pipeline_id="test_celery_runner.TestPipeline",
        run_id="123",
        input_data={},
        serializable_pipeline_object=None,
    )

    assert with_queue_result[0].options["queue"] == "else"

    without_queue_result = Runner()._task_to_celery_tasks(
        task=TestPipeline().tasks["without_queue"],
        pipeline_id="test_celery_runner.TestPipeline",
        run_id="123",
        input_data={},
        serializable_pipeline_object=None,
    )

    assert without_queue_result[0].options["queue"] == None

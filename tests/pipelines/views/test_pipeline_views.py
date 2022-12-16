from unittest.mock import ANY, patch

from django.urls import reverse

import pytest
from model_bakery import baker
from pydantic import BaseModel

from wildcoeus.pipelines import Pipeline, PipelineTaskStatus, Task
from wildcoeus.pipelines.registry import pipeline_registry


pytest_plugins = [
    "tests.pipelines.fixtures",
]

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "url",
    [
        reverse("wildcoeus.pipelines:list"),
        reverse("wildcoeus.pipelines:pipeline-execution-list", args=["pipeline-slug"]),
        reverse("wildcoeus.pipelines:results-list", args=["123"]),
        reverse("wildcoeus.pipelines:logs-list", args=["123"]),
        reverse("wildcoeus.pipelines:start", args=["pipeline-slug"]),
        reverse("wildcoeus.pipelines:rerun-task", args=["1"]),
    ],
)
def test_view__no_permission(url, client):
    response = client.get(url)

    assert response.status_code == 302


def test_pipeline_list(client, user):
    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:list"))

    assert response.status_code == 200
    assert "pipelines" in list(response.context_data.keys())
    assert len(response.context_data["pipelines"]) == 4


def test_pipeline_execution_list(client, user):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")

    client.force_login(user)
    response = client.get(
        reverse("wildcoeus.pipelines:pipeline-execution-list", args=[pe.pipeline_id])
    )

    assert response.status_code == 200
    assert "object_list" in list(response.context_data.keys())
    assert len(response.context_data["object_list"]) == 1
    assert pe in response.context_data["object_list"]


def test_pipeline_execution_list_queries_pinned(
    client, user, django_assert_num_queries
):
    client.force_login(user)
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")

    with django_assert_num_queries(3):
        client.get(
            reverse(
                "wildcoeus.pipelines:pipeline-execution-list", args=[pe.pipeline_id]
            )
        )


def test_results_list__tasks_completed(client, user):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    te = baker.make_recipe("pipelines.fake_task_result", run_id=pe.run_id, _quantity=3)

    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:results-list", args=[pe.run_id]))

    assert response.status_code == 286
    assert "object_list" in list(response.context_data.keys())
    assert len(response.context_data["object_list"]) == 3
    assert te[0] in response.context_data["object_list"]


def test_results_list__tasks_not_completed(client, user):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    baker.make_recipe("pipelines.fake_task_result", run_id=pe.run_id)
    baker.make_recipe(
        "pipelines.fake_task_result",
        run_id=pe.run_id,
        status=PipelineTaskStatus.PENDING.value,
    )

    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:results-list", args=[pe.run_id]))

    assert response.status_code == 200


def test_results_list_queries_pinned(client, user, django_assert_num_queries):
    client.force_login(user)
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    te = baker.make_recipe("pipelines.fake_task_result", run_id=pe.run_id, _quantity=3)

    with django_assert_num_queries(4):
        client.get(reverse("wildcoeus.pipelines:results-list", args=[pe.run_id]))


def test_log_list__tasks_completed(client, user):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    te = baker.make_recipe("pipelines.fake_task_result", run_id=pe.run_id, _quantity=3)
    pl = baker.make_recipe("pipelines.fake_pipeline_log", run_id=pe.run_id, _quantity=3)
    tl = baker.make_recipe("pipelines.fake_task_log", run_id=pe.run_id, _quantity=3)

    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id]))

    assert response.status_code == 286
    assert "logs" in list(response.context_data.keys())
    assert len(response.context_data["logs"]) == 6
    assert pl[0].log_message in [x[1] for x in response.context_data["logs"]]
    assert tl[0].log_message in [x[1] for x in response.context_data["logs"]]


def test_log_list__tasks_not_completed(client, user):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    baker.make_recipe("pipelines.fake_task_result", run_id=pe.run_id)
    baker.make_recipe(
        "pipelines.fake_task_result",
        run_id=pe.run_id,
        status=PipelineTaskStatus.PENDING.value,
    )
    baker.make_recipe("pipelines.fake_pipeline_log", run_id=pe.run_id)
    baker.make_recipe("pipelines.fake_task_log", run_id=pe.run_id)

    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id]))

    assert response.status_code == 200


def test_log_list_queries_pinned(client, user, django_assert_num_queries):
    client.force_login(user)
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    baker.make_recipe("pipelines.fake_task_result", run_id=pe.run_id, _quantity=3)
    baker.make_recipe("pipelines.fake_pipeline_log", run_id=pe.run_id)
    baker.make_recipe("pipelines.fake_task_log", run_id=pe.run_id)

    with django_assert_num_queries(5):
        client.get(reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id]))


def test_start__get(client, user, test_pipeline):
    client.force_login(user)
    response = client.get(
        reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()])
    )

    assert response.status_code == 200


@patch("wildcoeus.pipelines.views.run_pipeline")
def test_start__eager__post(run_pipeline, client, user, test_pipeline):
    client.force_login(user)
    response = client.post(
        reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()]), data={}
    )

    print(response.__dict__)
    run_pipeline.assert_called_once_with(
        pipeline_id=test_pipeline.get_id(),
        input_data=ANY,
        run_id=ANY,
    )
    assert response.status_code == 302


@patch("wildcoeus.pipelines.views.run_pipeline")
def test_start__celery__post(run_pipeline, client, user, settings, test_pipeline):
    settings.WILDCOEUS_DEFAULT_PIPELINE_RUNNER = (
        "wildcoeus.pipelines.runners.celery.runner.Runner"
    )
    client.force_login(user)
    response = client.post(
        reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()]), data={}
    )

    run_pipeline.assert_called_once_with(
        pipeline_id=test_pipeline.get_id(),
        input_data=ANY,
        run_id=ANY,
    )
    assert response.status_code == 302


@patch("wildcoeus.pipelines.views.run_pipeline")
def test_start__post__with_formdata(run_pipeline, client, user):
    class MessageInputType(BaseModel):
        message: str

    class TestTaskFirst(Task):
        InputType = MessageInputType

        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTaskFirst(config={})

        class Meta:
            title = "Test Pipeline"

    test_pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    client.force_login(user)
    response = client.post(
        reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()]),
        data={"message": "test"},
    )

    run_pipeline.assert_called_once_with(
        pipeline_id=test_pipeline.get_id(),
        input_data=ANY,
        run_id=ANY,
    )
    assert response.status_code == 302


@patch("wildcoeus.pipelines.views.run_pipeline")
def test_start__post__with_no_formdata(run_pipeline, client, user):
    class MessageInputType(BaseModel):
        message: str

    class TestTaskFirst(Task):
        InputType = MessageInputType

        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTaskFirst(config={})

        class Meta:
            title = "Test Pipeline"

    test_pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    client.force_login(user)
    response = client.post(
        reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()]), data={}
    )

    run_pipeline.assert_not_called()
    assert response.status_code == 200


@patch("wildcoeus.pipelines.views.run_task")
def test_rerun_task__post(run_task, client, user):
    class TestTaskFirst(Task):
        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTaskFirst(config={})

        class Meta:
            title = "Test Pipeline"

    pipeline = TestPipeline()
    pipeline_registry.register(TestPipeline)

    tr = baker.make_recipe(
        "pipelines.fake_task_result",
        pipeline_id=pipeline.get_id(),
        pipeline_task="first",
        task_id="test_pipeline_views.TestTaskFirst",
    )
    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:rerun-task", args=[tr.pk]))

    run_task.assert_called_once_with(
        pipeline_id=tr.pipeline_id,
        task_id=tr.task_id,
        run_id=tr.run_id,
        input_data=tr.input_data,
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )

    assert response.status_code == 302


def test_rerun_task__no_task(client, user):
    tr = baker.make_recipe("pipelines.fake_task_result", pipeline_task="fake")
    client.force_login(user)
    response = client.get(reverse("wildcoeus.pipelines:rerun-task", args=[tr.pk]))

    assert response.status_code == 404

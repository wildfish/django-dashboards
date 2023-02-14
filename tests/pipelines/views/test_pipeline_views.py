import tempfile
from functools import reduce
from itertools import chain
from typing import List
from unittest.mock import patch

from django.test.utils import override_settings
from django.urls import reverse

import pytest
from model_bakery import baker
from pydantic import BaseModel

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.models import (
    OrmPipelineExecution,
    OrmPipelineResult,
    OrmTaskExecution,
    OrmTaskResult,
)
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task


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
        reverse("wildcoeus.pipelines:logs-filter", args=["123"]),
        reverse("wildcoeus.pipelines:start", args=["pipeline-slug"]),
        reverse("wildcoeus.pipelines:rerun-task", args=["1"]),
    ],
)
def test_view__no_permission(url, client):
    response = client.get(url)

    assert response.status_code == 302


def test_pipeline_list(client, staff):
    client.force_login(staff)
    response = client.get(reverse("wildcoeus.pipelines:list"))

    assert response.status_code == 200
    assert "pipelines" in list(response.context_data.keys())
    assert len(response.context_data["pipelines"]) == 4


def test_pipeline_execution_list(client, staff):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")

    client.force_login(staff)
    response = client.get(
        reverse("wildcoeus.pipelines:pipeline-execution-list", args=[pe.pipeline_id])
    )

    assert response.status_code == 200
    assert "object_list" in list(response.context_data.keys())
    assert len(response.context_data["object_list"]) == 1
    assert pe in response.context_data["object_list"]


def test_pipeline_execution_list_queries_pinned(
    client, staff, django_assert_num_queries
):
    client.force_login(staff)
    baker.make_recipe(
        "pipelines.fake_pipeline_execution", pipeline_id="12345", _quantity=50
    )

    with django_assert_num_queries(4):
        client.get(
            reverse("wildcoeus.pipelines:pipeline-execution-list", args=["12345"])
        )


def test_results_list__tasks_completed(client, staff):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    pr = baker.make_recipe("pipelines.fake_pipeline_result", execution=pe)
    baker.make_recipe("pipelines.fake_task_execution", pipeline_result=pr, _quantity=3)

    client.force_login(staff)
    response = client.get(reverse("wildcoeus.pipelines:results-list", args=[pe.run_id]))

    assert response.status_code == 200
    assert "object_list" in list(response.context_data.keys())
    assert len(response.context_data["object_list"]) == 1
    assert pr in response.context_data["object_list"]


def test_results_list__tasks_not_completed(client, staff):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    baker.make_recipe("pipelines.fake_pipeline_execution")

    pr = baker.make_recipe("pipelines.fake_pipeline_result", execution=pe)
    te = baker.make_recipe("pipelines.fake_task_execution", pipeline_result=pr)
    baker.make_recipe(
        "pipelines.fake_task_result",
        execution=te,
        status=PipelineTaskStatus.PENDING.value,
    )

    client.force_login(staff)
    response = client.get(reverse("wildcoeus.pipelines:results-list", args=[pe.run_id]))

    assert response.status_code == 200


def test_results_list_queries_pinned(client, staff, django_assert_num_queries):
    client.force_login(staff)
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    baker.make_recipe("pipelines.fake_pipeline_execution", _quantity=3)

    with django_assert_num_queries(4):
        client.get(reverse("wildcoeus.pipelines:results-list", args=[pe.run_id]))


@pytest.mark.freeze_time("2022-12-20 13:23:55")
def test_log_list__tasks_completed(client, staff, snapshot):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    pr = baker.make_recipe("pipelines.fake_pipeline_result", execution=pe)
    te = baker.make_recipe("pipelines.fake_task_execution", pipeline_result=pr)
    baker.make_recipe("pipelines.fake_task_result", execution=te, _quantity=3)
    baker.make_recipe("pipelines.fake_pipeline_log", run_id=pe.run_id, _quantity=3)

    client.force_login(staff)
    response = client.get(reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id]))

    assert response.status_code == 200
    assert "logs" in list(response.context_data.keys())
    snapshot.assert_match(response.context_data["logs"])


@pytest.fixture
def setup_logs():
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    prs = baker.make_recipe("pipelines.fake_pipeline_result", execution=pe, _quantity=2)
    tes = [
        baker.make_recipe("pipelines.fake_task_execution", pipeline_result=pr)
        for pr in prs
    ]
    trs: List[OrmTaskResult] = list(
        reduce(
            lambda a, b: [*a, *b],
            [
                baker.make_recipe(
                    "pipelines.fake_task_result", execution=te, _quantity=2
                )
                for te in tes
            ],
            [],
        )
    )

    for obj in chain([pe], prs, tes, trs):
        baker.make_recipe(
            "pipelines.fake_pipeline_log",
            context_type=obj.content_type_name,
            context_id=obj.id,
            message=f"{obj.content_type_name} {obj.id}",
            run_id=pe.run_id,
        )


def build_expected_message(context_object):
    return f"[20/Dec/2022 13:23:55]: {context_object.content_type_name} {context_object.id}"


@pytest.mark.freeze_time("2022-12-20 13:23:55")
@pytest.mark.parametrize("status", PipelineTaskStatus.final_statuses())
def test_log_list__pipeline_is_in_final_state__status_is_286(
    client, staff, setup_logs, status
):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution", status=status.value)

    client.force_login(staff)
    response = client.get(
        reverse(
            "wildcoeus.pipelines:logs-list",
            args=[pe.run_id],
        )
    )

    assert response.status_code == 286


@pytest.mark.freeze_time("2022-12-20 13:23:55")
@pytest.mark.parametrize("status", PipelineTaskStatus.non_final_statuses())
def test_log_list__pipeline_not_in_final_state__status_is_286(
    client, staff, setup_logs, status
):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution", status=status.value)

    client.force_login(staff)
    response = client.get(
        reverse(
            "wildcoeus.pipelines:logs-list",
            args=[pe.run_id],
        )
    )

    assert response.status_code == 200


@pytest.mark.freeze_time("2022-12-20 13:23:55")
def test_log_list__no_filters__all_logs_included(client, staff, setup_logs):
    pe = OrmPipelineExecution.objects.first()

    client.force_login(staff)
    response = client.get(reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id]))

    assert build_expected_message(pe) in response.context_data["logs"]

    for pr in pe.results.all():
        assert build_expected_message(pr) in response.context_data["logs"]

        for te in pr.task_executions.all():
            assert build_expected_message(te) in response.context_data["logs"]

            for tr in te.results.all():
                assert build_expected_message(tr) in response.context_data["logs"]


@pytest.mark.freeze_time("2022-12-20 13:23:55")
def test_log_list__filter_by_pipeline_result__pipeline_result_and_children_in_logs(
    client, staff, setup_logs
):
    pe = OrmPipelineExecution.objects.first()
    [target, other] = pe.results.all()

    client.force_login(staff)
    response = client.get(
        reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id])
        + f"?type=PipelineResult&id={target.id}"
    )

    assert build_expected_message(pe) not in response.context_data["logs"]

    assert build_expected_message(target) in response.context_data["logs"]
    for te in target.task_executions.all():
        assert build_expected_message(te) in response.context_data["logs"]

        for tr in te.results.all():
            assert build_expected_message(tr) in response.context_data["logs"]

    assert build_expected_message(other) not in response.context_data["logs"]
    for te in other.task_executions.all():
        assert build_expected_message(te) not in response.context_data["logs"]

        for tr in te.results.all():
            assert build_expected_message(tr) not in response.context_data["logs"]


@pytest.mark.freeze_time("2022-12-20 13:23:55")
def test_log_list__filter_by_task_execution__task_execution_and_children_in_logs(
    client, staff, setup_logs
):
    [target, *others] = OrmTaskExecution.objects.all()

    client.force_login(staff)
    response = client.get(
        reverse("wildcoeus.pipelines:logs-list", args=[target.run_id])
        + f"?type=TaskExecution&id={target.id}"
    )

    assert (
        build_expected_message(target.pipeline_result.execution)
        not in response.context_data["logs"]
    )
    for pr in OrmPipelineResult.objects.all():
        assert build_expected_message(pr) not in response.context_data["logs"]

    for te in others:
        assert build_expected_message(te) not in response.context_data["logs"]

        for tr in te.results.all():
            assert build_expected_message(tr) not in response.context_data["logs"]

    assert build_expected_message(target) in response.context_data["logs"]
    for tr in target.results.all():
        assert build_expected_message(tr) in response.context_data["logs"]


@pytest.mark.freeze_time("2022-12-20 13:23:55")
def test_log_list__filter_by_task_result__task_result_in_logs(
    client, staff, setup_logs
):
    [target, *others] = OrmTaskResult.objects.all()

    client.force_login(staff)
    response = client.get(
        reverse("wildcoeus.pipelines:logs-list", args=[target.run_id])
        + f"?type=TaskResult&id={target.id}"
    )

    assert (
        build_expected_message(target.execution.pipeline_result.execution)
        not in response.context_data["logs"]
    )

    for pr in OrmPipelineResult.objects.all():
        assert build_expected_message(pr) not in response.context_data["logs"]

    for te in OrmTaskExecution.objects.all():
        assert build_expected_message(te) not in response.context_data["logs"]

    for tr in others:
        assert build_expected_message(tr) not in response.context_data["logs"]

    assert build_expected_message(target) in response.context_data["logs"]


def test_log_list__tasks_not_completed(client, staff):
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    pr = baker.make_recipe("pipelines.fake_pipeline_result", execution=pe)
    te = baker.make_recipe("pipelines.fake_task_execution", pipeline_result=pr)
    baker.make_recipe("pipelines.fake_task_result", execution=te)
    baker.make_recipe(
        "pipelines.fake_task_result",
        execution=te,
        status=PipelineTaskStatus.PENDING.value,
    )
    baker.make_recipe("pipelines.fake_pipeline_log", run_id=pe.run_id)

    client.force_login(staff)
    response = client.get(reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id]))

    assert response.status_code == 200


def test_log_list_queries_pinned(client, staff, django_assert_num_queries):
    client.force_login(staff)
    pe = baker.make_recipe("pipelines.fake_pipeline_execution")
    pr = baker.make_recipe("pipelines.fake_pipeline_result", execution=pe)
    te = baker.make_recipe("pipelines.fake_task_execution", pipeline_result=pr)
    baker.make_recipe("pipelines.fake_task_result", execution=te)
    baker.make_recipe(
        "pipelines.fake_task_result",
        execution=te,
        status=PipelineTaskStatus.PENDING.value,
    )
    baker.make_recipe("pipelines.fake_pipeline_log", run_id=pe.run_id)

    with django_assert_num_queries(4):
        client.get(reverse("wildcoeus.pipelines:logs-list", args=[pe.run_id]))


def test_start__get(client, staff, test_pipeline):
    client.force_login(staff)
    response = client.get(
        reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()])
    )

    assert response.status_code == 200


def test_start__post(client, staff, test_pipeline):
    client.force_login(staff)
    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
        response = client.post(
            reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()]), data={}
        )

    assert response.status_code == 302
    assert OrmPipelineResult.objects.count() == 1


def test_start__post__with_formdata(client, staff):
    class MessageInputType(BaseModel):
        message: str

    class TestTaskFirst(Task):
        InputType = MessageInputType

        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTaskFirst(config={})

        class Meta:
            app_label = "pipelinetest"

    test_pipeline = TestPipeline()

    client.force_login(staff)
    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
        response = client.post(
            reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()]),
            data={"message": "test"},
        )

    assert response.status_code == 302
    assert OrmPipelineResult.objects.count() == 1


def test_start__post__with_no_formdata(client, staff):
    class MessageInputType(BaseModel):
        message: str

    class TestTaskFirst(Task):
        InputType = MessageInputType

        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTaskFirst(config={})

        class Meta:
            app_label = "pipelinetest"

    test_pipeline = TestPipeline()

    client.force_login(staff)
    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
        response = client.post(
            reverse("wildcoeus.pipelines:start", args=[test_pipeline.get_id()]), data={}
        )

    assert response.context_data["form"].errors == {
        "message": ["This field is required."]
    }
    assert response.status_code == 200


@patch("wildcoeus.pipelines.views.run_task")
def test_rerun_task__post(run_task, client, staff):
    class TestTaskFirst(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTaskFirst(config={})

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()

    pe = baker.make_recipe(
        "pipelines.fake_pipeline_execution", pipeline_id=pipeline.get_id()
    )
    pr = baker.make_recipe("pipelines.fake_pipeline_result", execution=pe)
    te = baker.make_recipe(
        "pipelines.fake_task_execution",
        pipeline_result=pr,
        pipeline_task="first",
        task_id="pipelinetest.TestTaskFirst",
    )
    tr = baker.make_recipe(
        "pipelines.fake_task_result",
        execution=te,
    )
    client.force_login(staff)
    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
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


def test_rerun_task__no_task(client, staff):
    client.force_login(staff)
    response = client.get(reverse("wildcoeus.pipelines:rerun-task", args=["123"]))

    assert response.status_code == 404

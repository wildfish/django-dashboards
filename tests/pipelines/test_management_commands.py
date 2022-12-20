from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.utils.timezone import now

import pytest
from model_bakery import baker

from wildcoeus.pipelines.models import (
    PipelineExecution,
    PipelineLog,
    TaskLog,
    TaskResult,
)


pytest_plugins = [
    "tests.pipelines.fixtures",
]

pytestmark = pytest.mark.django_db


def test_clear_tasks_and_logs__all_deleted(freezer):
    today = now().today()

    baker.make_recipe("pipelines.fake_pipeline_execution", started=today, _quantity=3)
    baker.make_recipe("pipelines.fake_task_result", started=today, _quantity=3)
    baker.make_recipe("pipelines.fake_pipeline_log", _quantity=3)
    baker.make_recipe("pipelines.fake_task_log", _quantity=3)

    freezer.move_to(today + timedelta(days=11))

    out = StringIO()
    call_command("clear_tasks_and_logs", days=10, stdout=out)

    assert PipelineExecution.objects.count() == 0
    assert TaskResult.objects.count() == 0
    assert PipelineLog.objects.count() == 0
    assert TaskLog.objects.count() == 0


def test_clear_tasks_and_logs__non_deleted():
    today = now().today()

    baker.make_recipe("pipelines.fake_pipeline_execution", started=today, _quantity=3)
    baker.make_recipe("pipelines.fake_task_result", started=today, _quantity=3)
    baker.make_recipe("pipelines.fake_pipeline_log", _quantity=3)
    baker.make_recipe("pipelines.fake_task_log", _quantity=3)

    out = StringIO()
    call_command("clear_tasks_and_logs", days=10, stdout=out)

    assert PipelineExecution.objects.count() == 3
    assert TaskResult.objects.count() == 3
    assert PipelineLog.objects.count() == 3
    assert TaskLog.objects.count() == 3


def test_clear_tasks_and_logs__part_deleted(freezer):
    today = now().today()

    for d in [9, 11]:
        freezer.move_to(today - timedelta(days=d))
        baker.make_recipe(
            "pipelines.fake_pipeline_execution", started=now().today(), _quantity=2
        )
        baker.make_recipe(
            "pipelines.fake_task_result", started=now().today(), _quantity=2
        )
        baker.make_recipe("pipelines.fake_pipeline_log", _quantity=2)
        baker.make_recipe("pipelines.fake_task_log", _quantity=2)

    freezer.move_to(today)

    out = StringIO()
    call_command("clear_tasks_and_logs", days=10, stdout=out)

    assert PipelineExecution.objects.count() == 2
    assert TaskResult.objects.count() == 2
    assert PipelineLog.objects.count() == 2
    assert TaskLog.objects.count() == 2

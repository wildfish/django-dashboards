import tempfile
from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test.utils import override_settings
from django.utils.timezone import now

import pytest
from model_bakery import baker

from wildcoeus.pipelines.models import (
    PipelineExecution,
    PipelineLog,
    TaskLog,
    TaskResult,
)
from wildcoeus.pipelines.reporters.logging import LoggingReporter
from wildcoeus.pipelines.storage import LogFileSystemStorage


pytest_plugins = [
    "tests.pipelines.fixtures",
]

pytestmark = pytest.mark.django_db


def test_clear_tasks_and_logs__all_deleted(freezer):
    today = now().today()

    baker.make_recipe("pipelines.fake_pipeline_execution", run_id="123", started=today)
    baker.make_recipe(
        "pipelines.fake_task_result", run_id="123", started=today, _quantity=3
    )
    baker.make_recipe("pipelines.fake_pipeline_log", run_id="123", _quantity=3)
    baker.make_recipe("pipelines.fake_task_log", run_id="123", _quantity=3)

    freezer.move_to(today + timedelta(days=11))

    out = StringIO()
    call_command("clear_tasks_and_logs", days=10, stdout=out)

    assert PipelineExecution.objects.count() == 0
    assert TaskResult.objects.count() == 0
    assert PipelineLog.objects.count() == 0
    assert TaskLog.objects.count() == 0


def test_clear_tasks_and_logs__deletes_files(freezer):
    today = now().today()

    baker.make_recipe("pipelines.fake_pipeline_execution", run_id="123", started=today)
    freezer.move_to(today + timedelta(days=11))
    out = StringIO()

    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
        LoggingReporter._write_log_to_file("Some example text", "123")
        fs = LogFileSystemStorage()
        path = "logs/123.log"

        assert fs.exists(path)
        call_command("clear_tasks_and_logs", days=10, stdout=out)
        assert fs.exists(path) is False


def test_clear_tasks_and_logs__does_not_delete_files_if_date_current():
    today = now().today()

    baker.make_recipe("pipelines.fake_pipeline_execution", run_id="123", started=today)
    out = StringIO()

    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
        LoggingReporter._write_log_to_file("Some example text", "123")
        fs = LogFileSystemStorage()
        path = "logs/123.log"

        call_command("clear_tasks_and_logs", days=10, stdout=out)
        assert fs.exists(path)


def test_clear_tasks_and_logs__non_deleted():
    today = now().today()

    baker.make_recipe(
        "pipelines.fake_pipeline_execution", run_id="123", started=today, _quantity=3
    )
    baker.make_recipe(
        "pipelines.fake_task_result", run_id="123", started=today, _quantity=3
    )
    baker.make_recipe("pipelines.fake_pipeline_log", run_id="123", _quantity=3)
    baker.make_recipe("pipelines.fake_task_log", run_id="123", _quantity=3)

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
        pe = baker.make_recipe(
            "pipelines.fake_pipeline_execution",
            started=now().today(),
        )
        baker.make_recipe(
            "pipelines.fake_task_result",
            run_id=str(pe.run_id),
            started=now().today(),
            _quantity=2,
        )
        baker.make_recipe(
            "pipelines.fake_pipeline_log", run_id=str(pe.run_id), _quantity=2
        )
        baker.make_recipe("pipelines.fake_task_log", run_id=str(pe.run_id), _quantity=2)

    freezer.move_to(today)

    out = StringIO()
    call_command("clear_tasks_and_logs", days=10, stdout=out)

    assert PipelineExecution.objects.count() == 1
    assert TaskResult.objects.count() == 2
    assert PipelineLog.objects.count() == 2
    assert TaskLog.objects.count() == 2

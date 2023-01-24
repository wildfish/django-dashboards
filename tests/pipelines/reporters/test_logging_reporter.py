import logging
import tempfile
from unittest.mock import Mock

from django.test.utils import override_settings

import pytest
from model_bakery import baker

from wildcoeus.pipelines import config
from wildcoeus.pipelines.reporters.logging import LoggingReporter
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.storage import get_log_path


pytestmark = pytest.mark.django_db


def test_report_writes_the_message_to_info(caplog):
    caplog.set_level(logging.INFO)

    LoggingReporter().report(
        Mock(),
        PipelineTaskStatus.DONE.value,
        "The Message",
    )

    assert "The Message" in caplog.text


@pytest.mark.freeze_time("2022-12-20 13:23:55")
def test_report_task_writes_the_message_to_file():
    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
        LoggingReporter().report(
            baker.make_recipe("pipelines.fake_pipeline_execution", run_id="123"),
            PipelineTaskStatus.DONE.value,
            "The Message",
        )

        fs = config.Config().WILDCOEUS_LOG_FILE_STORAGE
        path = get_log_path("123")

        assert fs.exists(path)
        with fs.open(path, "r") as f:
            logs = f.read()
            assert logs == "[20/Dec/2022 13:23:55]: The Message\n"

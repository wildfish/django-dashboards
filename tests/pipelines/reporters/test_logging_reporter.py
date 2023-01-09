import logging
import tempfile

from django.test.utils import override_settings

import pytest

from wildcoeus.pipelines import config
from wildcoeus.pipelines.reporters.logging import LoggingReporter
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.storage import get_log_path


def test_report_task_writes_the_message_to_info(caplog):
    caplog.set_level(logging.INFO)

    LoggingReporter().report_task(
        pipeline_task="fake",
        task_id="task_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )

    assert "Task fake (task_id) changed to state DONE: Done" in caplog.text


def test_report_task_writes_the_message_to_info__with_object(caplog):
    caplog.set_level(logging.INFO)

    LoggingReporter().report_task(
        pipeline_task="fake",
        task_id="task_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object={"object": 1},
        serializable_task_object={"object": 2},
    )
    assert (
        "Task fake (task_id) changed to state DONE: Done | pipeline object: {'object': 1} | task object: {'object': 2}"
        in caplog.text
    )


def test_report_pipeline_writes_the_message_to_info(caplog):
    caplog.set_level(logging.INFO)

    LoggingReporter().report_pipeline(
        pipeline_id="pipeline_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )

    assert "Pipeline pipeline_id changed to state DONE: Done" in caplog.text


def test_report_pipeline_writes_the_message_to_info__with_object(caplog):
    caplog.set_level(logging.INFO)

    LoggingReporter().report_pipeline(
        pipeline_id="pipeline_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object={"object": 1},
        serializable_task_object={"object": 2},
    )

    assert (
        "Pipeline pipeline_id changed to state DONE: Done | pipeline object: {'object': 1}"
        in caplog.text
    )


@pytest.mark.freeze_time("2022-12-20 13:23:55")
def test_report_task_writes_the_message_to_file():
    with tempfile.TemporaryDirectory() as d, override_settings(MEDIA_ROOT=d):
        LoggingReporter().report(
            pipeline_id="pipeline_id",
            run_id="123",
            status=PipelineTaskStatus.DONE.value,
            message="Done",
            serializable_pipeline_object=None,
            serializable_task_object=None,
        )

        fs = config.Config().WILDCOEUS_LOG_FILE_STORAGE
        path = get_log_path("123")

        assert fs.exists(path)
        with fs.open(path, "r") as f:
            logs = f.read()
            assert (
                logs
                == "[20/Dec/2022 13:23:55]: Pipeline pipeline_id changed to state DONE: Done\n"
            )

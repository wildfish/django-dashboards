import logging

from datorum_pipelines import PipelineTaskStatus
from datorum_pipelines.reporters.logging import LoggingReporter


def test_report_task_writes_the_message_to_info(caplog):
    caplog.set_level(logging.INFO)

    LoggingReporter().report_task(
        pipeline_task="fake",
        task_id="task_id",
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    assert "Task fake:task_id changed to state DONE: Done" in caplog.text


def test_report_pipeline_writes_the_message_to_info(caplog):
    caplog.set_level(logging.INFO)

    LoggingReporter().report_pipeline(
        pipeline_id="pipeline_id", status=PipelineTaskStatus.DONE, message="Done"
    )

    assert "Pipeline pipeline_id changed to state DONE: Done" in caplog.text

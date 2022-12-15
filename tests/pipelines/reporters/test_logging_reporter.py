import logging

from wildcoeus.pipelines import PipelineTaskStatus
from wildcoeus.pipelines.reporters.logging import LoggingReporter


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

    assert "Task fake:task_id changed to state DONE: Done" in caplog.text


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
        "Task fake:task_id changed to state DONE: Done | pipeline object: {'object': 1} | task object: {'object': 2}"
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

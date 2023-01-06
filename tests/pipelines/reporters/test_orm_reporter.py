import pytest

from wildcoeus.pipelines.models import PipelineLog, TaskLog
from wildcoeus.pipelines.reporters.orm import ORMReporter
from wildcoeus.pipelines.status import PipelineTaskStatus


pytestmark = pytest.mark.django_db


def test_report_task_saves_message_to_db():
    ORMReporter().report_task(
        pipeline_task="fake",
        task_id="task_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )

    log = TaskLog.objects.last()

    assert log.log_message == "Task fake (task_id) changed to state DONE: Done"
    assert log.pipeline_task == "fake"
    assert log.task_id == "task_id"
    assert log.status == PipelineTaskStatus.DONE.value
    assert log.message == "Done"


def test_report_task_writes_saves_message_to_db__with_object():
    ORMReporter().report_task(
        pipeline_task="fake",
        task_id="task_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object={"object": 1},
        serializable_task_object={"object": 2},
    )

    log = TaskLog.objects.last()

    assert (
        log.log_message
        == "Task fake (task_id) changed to state DONE: Done | pipeline object: {'object': 1} | task object: {'object': 2}"
    )
    assert log.pipeline_task == "fake"
    assert log.task_id == "task_id"
    assert log.status == PipelineTaskStatus.DONE.value
    assert (
        log.message
        == "Done | pipeline object: {'object': 1} | task object: {'object': 2}"
    )


def test_report_pipeline_saves_message_to_db():
    ORMReporter().report_pipeline(
        pipeline_id="pipeline_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )

    log = PipelineLog.objects.last()

    assert log.log_message == "Pipeline pipeline_id changed to state DONE: Done"
    assert log.pipeline_id == "pipeline_id"
    assert log.status == PipelineTaskStatus.DONE.value
    assert log.message == "Done"


def test_report_pipeline_saves_message_to_db__with_object(caplog):
    ORMReporter().report_pipeline(
        pipeline_id="pipeline_id",
        status=PipelineTaskStatus.DONE.value,
        message="Done",
        serializable_pipeline_object={"object": 1},
        serializable_task_object={"object": 2},
    )

    log = PipelineLog.objects.last()

    assert (
        log.log_message
        == "Pipeline pipeline_id changed to state DONE: Done | pipeline object: {'object': 1}"
    )
    assert log.pipeline_id == "pipeline_id"
    assert log.status == PipelineTaskStatus.DONE.value
    assert log.message == "Done | pipeline object: {'object': 1}"

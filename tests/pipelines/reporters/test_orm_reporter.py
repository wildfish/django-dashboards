import pytest
from model_bakery import baker

from wildcoeus.pipelines.models import PipelineLog
from wildcoeus.pipelines.reporters.orm import ORMReporter
from wildcoeus.pipelines.status import PipelineTaskStatus


pytestmark = pytest.mark.django_db


def test_report_pipeline_execution_saves_message_to_db():
    pipeline_execution = baker.make_recipe("pipelines.fake_pipeline_execution")
    ORMReporter().report_pipeline_execution(
        pipeline_execution,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    log = PipelineLog.objects.last()

    assert log.context_type == "PipelineExecution"
    assert log.context_id == str(pipeline_execution.id)
    assert (
        log.log_message
        == f"Pipeline {pipeline_execution.pipeline_id} changed to state DONE: Done"
    )
    assert log.pipeline_id == pipeline_execution.pipeline_id
    assert log.run_id == pipeline_execution.run_id
    assert log.status == PipelineTaskStatus.DONE.value


def test_report_pipeline_result_saves_message_to_db():
    pipeline_result = baker.make_recipe("pipelines.fake_pipeline_result")
    ORMReporter().report_pipeline_result(
        pipeline_result,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    log = PipelineLog.objects.last()

    assert log.context_type == "PipelineResult"
    assert log.context_id == str(pipeline_result.id)
    assert (
        log.log_message
        == f"Pipeline result {pipeline_result.pipeline_id} changed to state DONE: Done"
    )
    assert log.pipeline_id == pipeline_result.pipeline_id
    assert log.run_id == pipeline_result.run_id
    assert log.status == PipelineTaskStatus.DONE.value


def test_report_pipeline_results_writes_saves_message_to_db__with_object():
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result",
        serializable_pipeline_object={"object": 1},
    )
    ORMReporter().report_pipeline_result(
        pipeline_result,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    log = PipelineLog.objects.last()

    assert log.context_type == "PipelineResult"
    assert log.context_id == str(pipeline_result.id)
    assert (
        log.log_message
        == f"Pipeline result {pipeline_result.pipeline_id} changed to state DONE: Done | "
        "pipeline object: {'object': 1}"
    )
    assert log.pipeline_id == pipeline_result.pipeline_id
    assert log.run_id == pipeline_result.run_id
    assert log.status == PipelineTaskStatus.DONE.value


def test_report_task_execution_saves_message_to_db():
    task_execution = baker.make_recipe("pipelines.fake_task_execution")
    ORMReporter().report_task_execution(
        task_execution,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    log = PipelineLog.objects.last()

    assert log.context_type == "TaskExecution"
    assert log.context_id == str(task_execution.id)
    assert (
        log.log_message
        == f"Task {task_execution.pipeline_task} ({task_execution.task_id}) changed to state DONE: Done"
    )
    assert log.pipeline_id == task_execution.pipeline_id
    assert log.run_id == task_execution.run_id
    assert log.status == PipelineTaskStatus.DONE.value


def test_report_task_execution_writes_saves_message_to_db__with_object():
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result",
        serializable_pipeline_object={"object": 1},
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution", pipeline_result=pipeline_result
    )

    ORMReporter().report_task_execution(
        task_execution,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    log = PipelineLog.objects.last()

    assert log.context_type == "TaskExecution"
    assert log.context_id == str(task_execution.id)
    assert (
        log.log_message
        == f"Task {task_execution.pipeline_task} ({task_execution.task_id}) changed to state DONE: Done | "
        "pipeline object: {'object': 1}"
    )
    assert log.pipeline_id == task_execution.pipeline_id
    assert log.run_id == task_execution.run_id
    assert log.status == PipelineTaskStatus.DONE.value


def test_report_task_result_saves_message_to_db():
    task_result = baker.make_recipe("pipelines.fake_task_result")
    ORMReporter().report_task_result(
        task_result,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    log = PipelineLog.objects.last()

    assert log.context_type == "TaskResult"
    assert log.context_id == str(task_result.id)
    assert (
        log.log_message
        == f"Task result {task_result.pipeline_task} ({task_result.task_id}) changed to state DONE: Done"
    )
    assert log.pipeline_id == task_result.pipeline_id
    assert log.run_id == task_result.run_id
    assert log.status == PipelineTaskStatus.DONE.value


def test_report_task_result_writes_saves_message_to_db__with_object():
    pipeline_result = baker.make_recipe(
        "pipelines.fake_pipeline_result",
        serializable_pipeline_object={"object": 1},
    )
    task_execution = baker.make_recipe(
        "pipelines.fake_task_execution", pipeline_result=pipeline_result
    )
    task_result = baker.make_recipe(
        "pipelines.fake_task_result",
        execution=task_execution,
        serializable_task_object={"object": 2},
    )

    ORMReporter().report_task_result(
        task_result,
        status=PipelineTaskStatus.DONE,
        message="Done",
    )

    log = PipelineLog.objects.last()

    assert log.context_type == "TaskResult"
    assert log.context_id == str(task_result.id)
    assert (
        log.log_message
        == f"Task result {task_result.pipeline_task} ({task_result.task_id}) changed to state DONE: Done | "
        "pipeline object: {'object': 1} | task object: {'object': 2}"
    )
    assert log.pipeline_id == task_result.pipeline_id
    assert log.run_id == task_result.run_id
    assert log.status == PipelineTaskStatus.DONE.value

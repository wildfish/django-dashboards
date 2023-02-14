from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence

from wildcoeus.pipelines.config import Config


if TYPE_CHECKING:
    from wildcoeus.pipelines.base import Pipeline

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import (
    PipelineDigest,
    PipelineExecution,
    PipelineResult,
    PipelineResultsStorage,
    TaskExecution,
    TaskResult,
)
from wildcoeus.pipelines.runners import PipelineRunner


_storage = None


def reset_storage_class():
    global _storage
    _storage = None


def get_pipeline_results_storage() -> PipelineResultsStorage:
    """
    Gets the configured pipeline results storage.
    """
    global _storage

    if _storage is None:
        _storage = Config().WILDCOEUS_PIPELINE_STORAGE

    return _storage


def build_pipeline_execution(
    pipeline: "Pipeline",
    run_id: str,
    runner: PipelineRunner,
    reporter: PipelineReporter,
    input_data: Dict[str, Any],
    build_all=True,
) -> PipelineExecution:
    """
    Creates a pipeline execution object along with all the pipeline results,
    task executions and task results.

    :param pipeline: The `Pipeline` object to create the results storage for
    :param run_id: A UUID for referencing the run
    :param runner: The `PipelineRunner` object that will be used to run the
        pipeline
    :param reporter: The `PipelineReporter` object that will be used to report
        status changed
    :param input_data: A json serializable `dict` containing the input parameters
    :param build_all: If True, all results objects are create otherwise only
        the pipeline execution object will be created (to store config errors for
        example)
    """
    storage = get_pipeline_results_storage()
    return storage.build_pipeline_execution(
        pipeline,
        run_id,
        runner,
        reporter,
        input_data,
        build_all=build_all,
    )


def get_pipeline_digest() -> PipelineDigest:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_digest()


def get_pipeline_executions(
    pipeline_id: Optional[str] = None,
) -> Sequence[PipelineExecution]:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_executions(pipeline_id=pipeline_id)


def get_pipeline_execution(_id) -> PipelineExecution | None:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_execution(_id)


def get_pipeline_results(run_id: Optional[str] = None) -> Sequence[PipelineResult]:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_results(run_id=run_id)


def get_pipeline_result(_id) -> PipelineResult | None:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_result(_id)


def get_task_executions(
    run_id: Optional[str] = None, pipeline_result_id: Optional[str] = None
) -> Sequence[TaskExecution]:
    storage = get_pipeline_results_storage()
    return storage.get_task_executions(
        run_id=run_id, pipeline_result_id=pipeline_result_id
    )


def get_task_execution(_id) -> TaskExecution | None:
    storage = get_pipeline_results_storage()
    return storage.get_task_execution(_id)


def get_task_results(
    run_id: Optional[str] = None,
    pipeline_result_id: Optional[str] = None,
    task_execution_id: Optional[str] = None,
) -> Sequence[TaskResult]:
    storage = get_pipeline_results_storage()
    return storage.get_task_results(
        run_id=run_id,
        pipeline_result_id=pipeline_result_id,
        task_execution_id=task_execution_id,
    )


def get_task_result(_id) -> TaskResult | None:
    storage = get_pipeline_results_storage()
    return storage.get_task_result(_id)


def cleanup_task_results(before: Optional[datetime] = None) -> Sequence[str]:
    storage = get_pipeline_results_storage()
    return storage.cleanup(before=before)

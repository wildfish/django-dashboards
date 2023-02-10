from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence


if TYPE_CHECKING:
    from wildcoeus.pipelines.base import Pipeline

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BasePipelineResultsStorage,
    BaseTaskExecution,
    BaseTaskResult,
    PipelineDigest,
)
from wildcoeus.pipelines.runners import PipelineRunner


def get_pipeline_results_storage() -> BasePipelineResultsStorage:
    """
    Gets the configured pipeline results storage.
    """

    # currently we only support orm storage but this could be extended for redis etc
    from .orm import OrmPipelineResultsStorage

    return OrmPipelineResultsStorage()


def build_pipeline_execution(
    pipeline: "Pipeline",
    run_id: str,
    runner: PipelineRunner,
    reporter: PipelineReporter,
    input_data: Dict[str, Any],
    build_all=True,
) -> BasePipelineExecution:
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
) -> Sequence[BasePipelineExecution]:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_executions(pipeline_id=pipeline_id)


def get_pipeline_execution(_id) -> BasePipelineExecution | None:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_execution(_id)


def get_pipeline_results(run_id: Optional[str] = None) -> Sequence[BasePipelineResult]:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_results(run_id=run_id)


def get_pipeline_result(_id) -> BasePipelineResult | None:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_result(_id)


def get_task_executions(
    run_id: Optional[str] = None, pipeline_result_id: Optional[str] = None
) -> Sequence[BaseTaskExecution]:
    storage = get_pipeline_results_storage()
    return storage.get_task_executions(
        run_id=run_id, pipeline_result_id=pipeline_result_id
    )


def get_task_execution(_id) -> BaseTaskExecution | None:
    storage = get_pipeline_results_storage()
    return storage.get_task_execution(_id)


def get_task_results(
    run_id: Optional[str] = None,
    pipeline_result_id: Optional[str] = None,
    task_execution_id: Optional[str] = None,
) -> Sequence[BaseTaskResult]:
    storage = get_pipeline_results_storage()
    return storage.get_task_results(
        run_id=run_id,
        pipeline_result_id=pipeline_result_id,
        task_execution_id=task_execution_id,
    )


def get_task_result(_id) -> BaseTaskResult | None:
    storage = get_pipeline_results_storage()
    return storage.get_task_result(_id)


def cleanup_task_results(before: Optional[datetime] = None) -> Sequence[str]:
    storage = get_pipeline_results_storage()
    return storage.cleanup(before=before)

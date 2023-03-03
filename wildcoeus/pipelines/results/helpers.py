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


def reset_storage_object():
    """
    Resets the cached storage object so that it is reevaluated from
    the settings the next time :code:`get_pipeline_results_storage`
    is called.
    """
    global _storage
    _storage = None


def get_pipeline_results_storage() -> PipelineResultsStorage:
    """
    Gets the configured pipeline results storage.
    """
    global _storage

    if _storage is None:
        _storage = Config().WILDCOEUS_DEFAULT_PIPELINE_STORAGE

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
    """
    Returns the ``PipelineDigest`` object providing stats for all registered pipeline
    classes.
    """
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_digest()


def get_pipeline_executions(
    pipeline_id: Optional[str] = None,
) -> Sequence[PipelineExecution]:
    """
    Gets all pipeline executions from the storage. If ``pipeline_id`` is supplied
    only executions for the given pipeline id will be returned

    :param pipeline_id: The id of the registered pipeline class
    """
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_executions(pipeline_id=pipeline_id)


def get_pipeline_execution(run_id) -> PipelineExecution | None:
    """
    Fetch a specific pipeline execution from the storage.

    If the pipeline execution isn't found, None will be returned.

    :param run_id: The id of the pipeline run to fetch the execution for
    """
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_execution(run_id)


def get_pipeline_results(run_id: Optional[str] = None) -> Sequence[PipelineResult]:
    """
    Gets all pipeline results from the storage. If ``run_id`` is supplied only results
    for that particular run will be returned.

    :param run_id: The id of the run to filter results by
    """
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_results(run_id=run_id)


def get_pipeline_result(_id) -> PipelineResult | None:
    """
    Fetch a specific pipeline result from the storage.

    If the pipeline result isn't found, None will be returned.

    :param _id: The id of the result to fetch from storage
    """
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_result(_id)


def get_task_executions(
    run_id: Optional[str] = None, pipeline_result_id: Optional[str] = None
) -> Sequence[TaskExecution]:
    """
    Gets all task executions from the storage.

    :param run_id: The id of the run to filter results by
    :param pipeline_result_id: The id of the parent pipeline result object to filter results by
    """
    storage = get_pipeline_results_storage()
    return storage.get_task_executions(
        run_id=run_id, pipeline_result_id=pipeline_result_id
    )


def get_task_execution(_id) -> TaskExecution | None:
    """
    Fetch a specific task execution from the storage.

    If the pipeline result isn't found, None will be returned.

    :param _id: The id of the task execution to fetch from storage
    """
    storage = get_pipeline_results_storage()
    return storage.get_task_execution(_id)


def get_task_results(
    run_id: Optional[str] = None,
    pipeline_result_id: Optional[str] = None,
    task_execution_id: Optional[str] = None,
) -> Sequence[TaskResult]:
    """
    Gets all task results from the storage.

    :param run_id: The id of the run to filter results by
    :param pipeline_result_id: The id of the grandparent pipeline result object to filter results by
    :param task_execution_id: The id of the parent task execution object to filter results by
    """
    storage = get_pipeline_results_storage()
    return storage.get_task_results(
        run_id=run_id,
        pipeline_result_id=pipeline_result_id,
        task_execution_id=task_execution_id,
    )


def get_task_result(_id) -> TaskResult | None:
    """
    Fetch a specific task result from the storage.

    If the pipeline result isn't found, None will be returned.

    :param _id: The id of the task result to fetch from storage
    """
    storage = get_pipeline_results_storage()
    return storage.get_task_result(_id)


def cleanup_task_results(before: Optional[datetime] = None) -> Sequence[str]:
    """
    Removes all results objects from the storage.

    :param before: If set only objects created before the date will be removed. Otherwise
        all will be removed.
    """
    storage = get_pipeline_results_storage()
    return storage.cleanup(before=before)

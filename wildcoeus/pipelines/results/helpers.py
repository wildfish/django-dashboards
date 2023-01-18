from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from wildcoeus.pipelines.base import Pipeline

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import BasePipelineResultsStorage, BasePipelineExecution, BasePipelineResult, \
    BaseTaskResult, BaseTaskExecution
from wildcoeus.pipelines.runners import PipelineRunner


def get_pipeline_results_storage() -> BasePipelineResultsStorage:
    # currently we only support orm storage but this could be extended for redis etc
    from .orm import OrmPipelineResultsStorage
    return OrmPipelineResultsStorage()


def build_pipeline_execution(
    pipeline: "Pipeline",
    run_id: str,
    runner: PipelineRunner,
    reporter: PipelineReporter,
    input_data: Dict[str, Any],
) -> BasePipelineExecution:
    storage = get_pipeline_results_storage()
    return storage.build_pipeline_execution(
        pipeline,
        run_id,
        runner,
        reporter,
        input_data,
    )


def get_pipeline_execution(_id) -> BasePipelineExecution:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_execution(_id)


def get_pipeline_result(_id) -> BasePipelineResult:
    storage = get_pipeline_results_storage()
    return storage.get_pipeline_result(_id)


def get_task_execution(_id) -> BaseTaskExecution:
    storage = get_pipeline_results_storage()
    return storage.get_task_execution(_id)


def get_task_result(_id) -> BaseTaskResult:
    storage = get_pipeline_results_storage()
    return storage.get_task_result(_id)

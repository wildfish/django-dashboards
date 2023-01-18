import datetime
from typing import Dict, Any, Optional, Iterable, TYPE_CHECKING

from wildcoeus.pipelines import config

if TYPE_CHECKING:
    from wildcoeus.pipelines.base import Pipeline
    from wildcoeus.pipelines.reporters import PipelineReporter
    from wildcoeus.pipelines.runners import PipelineRunner
    from wildcoeus.pipelines.status import PipelineTaskStatus
    from wildcoeus.pipelines.tasks import Task


class BasePipelineExecution:
    id: Any
    started: Optional[datetime]
    pipeline_id: str
    run_id: str
    status: str

    def report_status_change(self, reporter: "PipelineReporter", status: "PipelineTaskStatus", message=""):
        raise NotImplementedError()

    def get_pipeline(self) -> "Pipeline":
        raise NotImplementedError()

    def get_pipeline_results(self) -> Iterable["BasePipelineResult"]:
        raise NotImplementedError()


class BasePipelineResult:
    id: Any
    started: Optional[datetime]
    pipeline_id: str
    run_id: str
    status: str
    serializable_pipeline_object: Dict[str, Any]
    input_data: Dict[str, Any]
    runner: str
    reporter: str

    def get_pipeline(self) -> "Pipeline":
        raise NotImplementedError()

    def get_pipeline_execution(self) -> BasePipelineExecution:
        raise NotImplementedError()

    def get_task_executions(self) -> Iterable["BaseTaskExecution"]:
        raise NotImplementedError()

    def report_status_change(self, reporter: "PipelineReporter", status: "PipelineTaskStatus", propagate=True, message=""):
        raise NotImplementedError()


class BaseTaskExecution:
    id: Any
    pipeline_result: BasePipelineResult
    task_id: str
    pipeline_task: str
    pipeline_id: str
    run_id: str
    config: Dict[str, Any]
    input_data: Dict[str, Any]
    status: str
    serializable_pipeline_object: Dict[str, Any]

    def report_status_change(self, reporter: "PipelineReporter", status: "PipelineTaskStatus", propagate=True, message=""):
        raise NotImplementedError()

    def get_task(self, reporter) -> "Task":
        raise NotImplementedError()

    def get_task_results(self) -> Iterable["BaseTaskResult"]:
        raise NotImplementedError()


class BaseTaskResult:
    id: Any
    run_id: str
    pipeline_id: str
    task_id: str
    pipeline_task: str
    config: Dict[str, Any]
    input_data: Dict[str, Any]
    serializable_pipeline_object: Dict[str, Any]
    serializable_task_object: Dict[str, Any]
    status: str
    started: Optional[datetime]
    completed: Optional[datetime]

    def get_task_execution(self) -> BaseTaskExecution:
        raise NotImplementedError()

    def report_status_change(self, reporter: "PipelineReporter", status: "PipelineTaskStatus", propagate=True, message=""):
        raise NotImplementedError()

    def get_task(self) -> "Task":
        from wildcoeus.pipelines.tasks import task_registry

        reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER

        return task_registry.load_task_from_id(
            pipeline_task=self.pipeline_task,
            task_id=self.task_id,
            run_id=self.run_id,
            config=self.config,
            reporter=reporter,
        )

    @property
    def duration(self):
        if (
            self.status == PipelineTaskStatus.DONE.value
            and self.completed
            and self.started
        ):
            return (self.completed - self.started).seconds

        return None


class BasePipelineResultsStorage:
    def build_pipeline_execution(
        self,
        pipeline: "Pipeline",
        run_id: str,
        runner: "PipelineRunner",
        reporter: "PipelineReporter",
        input_data: Dict[str, Any],
    ):
        raise NotImplementedError()

    def get_pipeline_execution(self, _id):
        raise NotImplementedError()

    def get_pipeline_result(self, _id):
        raise NotImplementedError()

    def get_task_execution(self, _id):
        raise NotImplementedError()

    def get_task_result(self, _id):
        raise NotImplementedError()

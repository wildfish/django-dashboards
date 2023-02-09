import dataclasses
import re
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Sequence


if TYPE_CHECKING:
    from wildcoeus.pipelines.base import Pipeline
    from wildcoeus.pipelines.reporters import PipelineReporter
    from wildcoeus.pipelines.runners import PipelineRunner
    from wildcoeus.pipelines.status import PipelineTaskStatus
    from wildcoeus.pipelines.tasks import Task


@dataclasses.dataclass
class PipelineDigestItem:
    total_runs: int | None = None
    total_success: int | None = None
    total_failure: int | None = None
    last_ran: datetime | None = None
    average_runtime: float | None = None


PipelineDigest = Dict[str, PipelineDigestItem]


class BasePipelineStorageObject:
    content_type_name: str

    get_prop_re = re.compile("get_(.*)")

    def __getattr__(self, item):
        # if the class implements the property use that
        if item in self.__dict__:
            return self.__dict__[item]

        get_prop_match = self.get_prop_re.match(item)

        # if the property is a get_ method try to find an underlying
        # backing field and return that
        if get_prop_match:
            prop_name = get_prop_match.group(1)
            if hasattr(self, prop_name):
                return lambda: getattr(self, prop_name)

        return super().__getattribute__(item)


class BasePipelineExecution(BasePipelineStorageObject):
    content_type_name = "PipelineExecution"

    get_id: Callable[[], str]
    get_started: Callable[[], Optional[datetime]]
    get_pipeline_id: Callable[[], str]
    get_run_id: Callable[[], str]
    get_status: Callable[[], "PipelineTaskStatus"]
    get_input_data: Callable[[], Dict[str, Any]]
    get_pipeline: Callable[[], "Pipeline"]
    get_pipeline_results: Callable[[], Sequence["BasePipelineResult"]]

    def report_status_change(
        self, reporter: "PipelineReporter", status: "PipelineTaskStatus", message=""
    ):
        raise NotImplementedError()


class BasePipelineResult(BasePipelineStorageObject):
    content_type_name = "PipelineResult"

    get_id: Callable[[], Any]
    get_started: Callable[[], Optional[datetime]]
    get_pipeline_id: Callable[[], str]
    get_run_id: Callable[[], str]
    get_status: Callable[[], "PipelineTaskStatus"]
    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    get_input_data: Callable[[], Dict[str, Any]]
    get_runner: Callable[[], str]
    get_reporter: Callable[[], str]
    get_pipeline: Callable[[], "Pipeline"]
    get_pipeline_execution: Callable[[], BasePipelineExecution]
    get_task_executions: Callable[[], Sequence["BaseTaskExecution"]]

    def report_status_change(
        self,
        reporter: "PipelineReporter",
        status: "PipelineTaskStatus",
        propagate=True,
        message="",
    ):
        raise NotImplementedError()


class BaseTaskExecution(BasePipelineStorageObject):
    content_type_name = "TaskExecution"

    get_id: Callable[[], Any]
    get_pipeline_result: Callable[[], BasePipelineResult]
    get_task_id: Callable[[], str]
    get_pipeline_task: Callable[[], str]
    get_pipeline_id: Callable[[], str]
    get_run_id: Callable[[], str]
    get_config: Callable[[], Dict[str, Any]]
    get_input_data: Callable[[], Dict[str, Any]]
    get_status: Callable[[], "PipelineTaskStatus"]
    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    get_task: Callable[[], "Task"]
    get_task_results: Callable[[], Sequence["BaseTaskResult"]]

    def report_status_change(
        self,
        reporter: "PipelineReporter",
        status: "PipelineTaskStatus",
        propagate=True,
        message="",
    ):
        raise NotImplementedError()


class BaseTaskResult(BasePipelineStorageObject):
    content_type_name = "TaskResult"

    get_id: Callable[[], Any]
    get_run_id: Callable[[], str]
    get_pipeline_id: Callable[[], str]
    get_task_id: Callable[[], str]
    get_pipeline_task: Callable[[], str]
    get_config: Callable[[], Dict[str, Any]]
    get_input_data: Callable[[], Dict[str, Any]]
    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    get_serializable_task_object: Callable[[], Dict[str, Any]]
    get_status: Callable[[], "PipelineTaskStatus"]
    get_started: Callable[[], Optional[datetime]]
    get_completed: Callable[[], Optional[datetime]]
    get_task_execution: Callable[[], BaseTaskExecution]

    def report_status_change(
        self,
        reporter: "PipelineReporter",
        status: "PipelineTaskStatus",
        propagate=True,
        message="",
    ):
        raise NotImplementedError()

    def get_task(self) -> "Task":
        from wildcoeus.pipelines.tasks import task_registry

        return task_registry.load_task_from_id(
            pipeline_task=self.pipeline_task,
            task_id=self.task_id,
            config=self.config,
        )

    def get_duration(self):
        status = self.get_status()
        started = self.get_started()
        completed = self.get_completed()

        if status == PipelineTaskStatus.DONE and completed and started:
            return (completed - started).seconds

        return None


class BasePipelineResultsStorage:
    def build_pipeline_execution(
        self,
        pipeline: "Pipeline",
        run_id: str,
        runner: "PipelineRunner",
        reporter: "PipelineReporter",
        input_data: Dict[str, Any],
        build_all=True,
    ) -> BasePipelineExecution:
        """
        Creates a pipeline execution object along with all the pipeline results,
        task executions and task results.

        If `build_all` is True, the storage class should create:

        * 1 pipeline execution object
        * A pipeline result object per element in the pipeline iterator
        * Per pipeline result, a tasks execution object per task in the pipeline
        * Per task execution object, a task result object per element in the task
          iterator

        If `build_all` is False, only the pipeline execution should be created.
        This is used to capture error states when the pipeline is badly
        configured and the other objects may not be able to be created.

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
        raise NotImplementedError()

    def get_pipeline_digest(self) -> PipelineDigest:
        raise NotImplementedError()

    def get_pipeline_executions(
        self, pipeline_id: str = None
    ) -> Sequence[BasePipelineExecution]:
        raise NotImplementedError()

    def get_pipeline_execution(self, run_id) -> BasePipelineExecution | None:
        raise NotImplementedError()

    def get_pipeline_results(self, run_id: str = None) -> Sequence[BasePipelineResult]:
        raise NotImplementedError()

    def get_pipeline_result(self, _id) -> BasePipelineResult | None:
        raise NotImplementedError()

    def get_task_executions(
        self, run_id: str = None, pipeline_result_id: str = None
    ) -> Sequence[BaseTaskExecution]:
        raise NotImplementedError()

    def get_task_execution(self, _id) -> BaseTaskExecution | None:
        raise NotImplementedError()

    def get_task_results(
        self,
        run_id: str = None,
        pipeline_result_id: str = None,
        task_execution_id: str = None,
    ) -> Sequence[BaseTaskResult]:
        raise NotImplementedError()

    def get_task_result(self, _id) -> BaseTaskResult | None:
        raise NotImplementedError()

    def cleanup(self, before: datetime = None) -> Sequence[str]:
        raise NotImplementedError()

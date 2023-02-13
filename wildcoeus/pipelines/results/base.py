import dataclasses
import re
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Sequence

from django.utils.timezone import now


if TYPE_CHECKING:
    from wildcoeus.pipelines.base import Pipeline
    from wildcoeus.pipelines.reporters import PipelineReporter
    from wildcoeus.pipelines.runners import PipelineRunner
    from wildcoeus.pipelines.status import PipelineTaskStatus
    from wildcoeus.pipelines.tasks import Task


@dataclasses.dataclass
class PipelineDigestItem:
    """
    Data class for storing entries in the pipeline digest

    :attribute total_runs: The total number of times the pipeline has been ran
    :attribute total_success: The total number of times the pipeline has been successfully ran
    :attribute total_failure: The total number of times the pipeline has failed
    :attribute last_ran: The date and time the pipeline was last ran
    :attribute average_runtime: The average amount of time (in seconds) it takes to run the pipeline
    """

    total_runs: int = 0
    total_success: int = 0
    total_failure: int = 0
    last_ran: datetime | None = None
    average_runtime: float | None = None


"""
A dictionary type mapping pipeline ids to the ``PipelineDigestItem``
"""
PipelineDigest = Dict[str, PipelineDigestItem]


class PipelineStorageObject:
    """
    Base object for all items in the pipeline results storage.

    It handles looking resolving un implemented ``get_`` methods by falling
    back to looking up the attribute on the model and returning that if present.
    For example, if a method call ``get_run_id`` is made, the class will:

    1. First check if ``get_run_id`` is implemented, if it is, use it
    2. If it's not implemented, check if the object has a ``run_id`` attribute
       if so, return a method that returns the attribute value.
    3. If neither are present, raise an ``AttributeError`` as normal

    ``set_`` methods are also handled in a similar manner:

    1. First check if ``set_run_id`` is implemented, if it is, use it
    2. If not, return a method that sets the value of ``run_id`` on the object

    :attribute content_type_name: The type name of the results object. This is
        used throughout the system and is set by the specific base class and
        should not be changed.
    :attribute method_prop_re: Regular expression used to extract property name
        from the lookup item.
    :attribute getter: The fallback method to use when the a ``get_`` function
        isn't implemented.
    :attribute setter: The fallback method to use when the a ``set_`` function
        isn't implemented.
    """

    content_type_name: str

    method_prop_re = re.compile("^(get|set)_(.*)$")

    setter: Callable[["PipelineStorageObject", str, Any], None] = setattr
    getter: Callable[["PipelineStorageObject", str], None] = getattr

    get_run_id: Callable[[], str]
    get_started: Callable[[], Optional[datetime]]
    set_started: Callable[[datetime], None]
    get_completed: Callable[[], Optional[datetime]]
    set_completed: Callable[[datetime], None]
    get_pipeline_id: Callable[[], str]
    get_status: Callable[[], "PipelineTaskStatus"]
    get_input_data: Callable[[], Dict[str, Any]]
    get_pipeline: Callable[[], "Pipeline"]

    save: Callable[[], Any]

    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            # if the property is a ``get_`` or ``set_`` method try to find an underlying
            # backing field and return or update that
            method_prop_match = self.method_prop_re.match(item)
            if method_prop_match:
                method = method_prop_match.group(1)
                prop_name = method_prop_match.group(2)

                if hasattr(self, prop_name):
                    return {
                        "get": lambda: self.getter(self, prop_name),
                        "set": lambda v: self.setter(self, prop_name, v),
                    }[method]

            raise

    def _get_propagate_parent(self) -> Optional["PipelineStorageObject"]:
        return None

    def report_status_change(
        self,
        reporter: "PipelineReporter",
        status: "PipelineTaskStatus",
        message="",
        propagate=True,
    ):
        """
        Update the status of the pipeline execution. If the status hasn't changed
        or hasn't moved on (ie not pending -> running or running -> a final state)
        the message wont be reported.

        :param reporter: The reporter to write the message to.
        :param status: The new status of the
        :param message: Optional message to record with the status change
        :param propagate: If True and the object specifies propagation parents the
            status changed will be passed to the parents
        """
        from wildcoeus.pipelines.status import PipelineTaskStatus

        if not PipelineTaskStatus[self.get_status().value].has_advanced(status):
            return

        # if the object has any parents to propagate to, report there too
        prop_parent = self._get_propagate_parent()
        if propagate and prop_parent:
            prop_parent.report_status_change(
                reporter, status, message=message, propagate=propagate
            )

        if status == PipelineTaskStatus.RUNNING:
            self.set_started(now())

        if status in PipelineTaskStatus.final_statuses():
            self.set_completed(now())

        self.set_status(status.value)
        self.save()
        reporter.report_context_object(
            self,
            status,
            f"Changed state to {status.value}{'' if not message else ' - ' + message}",
        )


class PipelineExecution(PipelineStorageObject):
    """
    Object to store the overall result of a pipeline run
    """

    content_type_name = "PipelineExecution"
    get_pipeline_results: Callable[[], Sequence["PipelineResult"]]


class PipelineResult(PipelineStorageObject):
    content_type_name = "PipelineResult"

    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    get_runner: Callable[[], str]
    get_reporter: Callable[[], str]
    get_pipeline_execution: Callable[[], PipelineExecution]
    get_task_executions: Callable[[], Sequence["TaskExecution"]]

    def _get_propagate_parent(self) -> Optional["PipelineStorageObject"]:
        return self.get_pipeline_execution()


class TaskExecution(PipelineStorageObject):
    content_type_name = "TaskExecution"

    get_id: Callable[[], Any]
    get_pipeline_result: Callable[[], PipelineResult]
    get_task_id: Callable[[], str]
    get_pipeline_task: Callable[[], str]
    get_config: Callable[[], Dict[str, Any]]
    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    get_task: Callable[[], "Task"]
    get_task_results: Callable[[], Sequence["TaskResult"]]

    def _get_propagate_parent(self) -> Optional["PipelineStorageObject"]:
        return self.get_pipeline_result()


class TaskResult(PipelineStorageObject):
    content_type_name = "TaskResult"

    get_id: Callable[[], Any]
    get_task_id: Callable[[], str]
    get_pipeline_task: Callable[[], str]
    get_config: Callable[[], Dict[str, Any]]
    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    get_serializable_task_object: Callable[[], Dict[str, Any]]
    get_task_execution: Callable[[], TaskExecution]

    def _get_propagate_parent(self) -> Optional["PipelineStorageObject"]:
        return self.get_task_execution()

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


class PipelineResultsStorage:
    def build_pipeline_execution(
        self,
        pipeline: "Pipeline",
        run_id: str,
        runner: "PipelineRunner",
        reporter: "PipelineReporter",
        input_data: Dict[str, Any],
        build_all=True,
    ) -> PipelineExecution:
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
        self, pipeline_id: Optional[str] = None
    ) -> Sequence[PipelineExecution]:
        raise NotImplementedError()

    def get_pipeline_execution(self, run_id) -> PipelineExecution | None:
        raise NotImplementedError()

    def get_pipeline_results(
        self, run_id: Optional[str] = None
    ) -> Sequence[PipelineResult]:
        raise NotImplementedError()

    def get_pipeline_result(self, _id) -> PipelineResult | None:
        raise NotImplementedError()

    def get_task_executions(
        self, run_id: Optional[str] = None, pipeline_result_id: Optional[str] = None
    ) -> Sequence[TaskExecution]:
        raise NotImplementedError()

    def get_task_execution(self, _id) -> TaskExecution | None:
        raise NotImplementedError()

    def get_task_results(
        self,
        run_id: Optional[str] = None,
        pipeline_result_id: Optional[str] = None,
        task_execution_id: Optional[str] = None,
    ) -> Sequence[TaskResult]:
        raise NotImplementedError()

    def get_task_result(self, _id) -> TaskResult | None:
        raise NotImplementedError()

    def cleanup(self, before: Optional[datetime] = None) -> Sequence[str]:
        raise NotImplementedError()

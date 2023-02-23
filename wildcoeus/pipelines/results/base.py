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
    """

    total_runs: int = 0
    """The total number of times the pipeline has been ran"""

    total_success: int = 0
    """The total number of times the pipeline has been successfully ran"""

    total_failure: int = 0
    """The total number of times the pipeline has failed"""

    last_ran: datetime | None = None
    """The date and time the pipeline was last ran"""

    average_runtime: float | None = None
    """The average amount of time (in seconds) it takes to run the pipeline"""


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
    """

    content_type_name: str
    """
    The type name of the results object. This is used throughout the system and is set by the specific base class 
    and should not be changed.
    """

    method_prop_re = re.compile("^(get|set)_(.*)$")
    """Regular expression used to extract property name from the lookup item."""

    setter: Callable[["PipelineStorageObject", str, Any], None] = setattr
    """The fallback method to use when the a ``get_`` function isn't implemented."""

    getter: Callable[["PipelineStorageObject", str], None] = getattr
    """The fallback method to use when the a ``set_`` function isn't implemented."""

    get_run_id: Callable[[], str]
    """Returns the id of the running pipeline instance"""

    get_started: Callable[[], Optional[datetime]]
    """Returns the time the pipeline was started"""

    set_started: Callable[[datetime], None]
    """Sets the time the pipeline was started"""

    get_completed: Callable[[], Optional[datetime]]
    """Returns the time the pipeline finished (whether successful or not)"""

    set_completed: Callable[[datetime], None]
    """Sets the time the pipeline finished"""

    get_pipeline_id: Callable[[], str]
    """Returns the id of the registered pipeline class"""

    get_status: Callable[[], "PipelineTaskStatus"]
    """Returns the current status of the pipeline"""

    get_input_data: Callable[[], Dict[str, Any]]
    """Returns the input data for the pipeline run"""

    get_pipeline: Callable[[], "Pipeline"]
    """Returns the registered pipeline class"""

    save: Callable[[], Any]
    """Commits the current object state to the storage"""

    def __getattribute__(self, item):
        """
        Manages getting and setting from fallback attributes when ``get_``
        and ``set_`` methods are not defined.
        """
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
        """
        Returns the parent object to pass statuses to when statuses
        should be propagated
        """
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

    get_id: Callable[[], Any]
    """Returns id of the task execution in the storage"""

    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    """Returns the object this instance of the pipeline was started with"""

    get_pipeline_object: Callable[[], "Pipeline"]
    """Gets the deserialized pipeline object"""

    get_runner: Callable[[], str]
    """Returns a python path to the runner the pipeline was started with"""

    get_reporter: Callable[[], str]
    """Returns a python path to the reporter the pipeline was started with"""

    get_pipeline_execution: Callable[[], PipelineExecution]
    """Returns the pipeline execution object describing the pipeline as whole"""

    get_task_executions: Callable[[], Sequence["TaskExecution"]]
    """Returns all the task execution objects for this particular pipeline instance"""

    get_pipeline: Callable[[], "Pipeline"]
    """Returns the registered pipeline class"""

    def _get_propagate_parent(self) -> Optional["PipelineStorageObject"]:
        return self.get_pipeline_execution()


class TaskExecution(PipelineStorageObject):
    content_type_name = "TaskExecution"

    get_id: Callable[[], Any]
    """Returns id of the task execution in the storage"""

    get_pipeline_result: Callable[[], PipelineResult]
    """Gets the pipeline result the task execution is linked to"""

    get_task_id: Callable[[], str]
    """Gets the id of the registered task class"""

    get_pipeline_task: Callable[[], str]
    """Gets the name of the task property on the pipeline class"""

    get_config: Callable[[], Dict[str, Any]]
    """Gets the task config"""

    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    """Returns the object this instance of the pipeline was started with"""

    get_pipeline_object: Callable[[], "Pipeline"]
    """Gets the deserialized pipeline object"""

    get_pipeline: Callable[[], "Pipeline"]
    """Returns the registered pipeline class"""

    get_task: Callable[[], "Task"]
    """Gets the registered task class"""

    get_task_results: Callable[[], Sequence["TaskResult"]]
    """Gets all the results for this task execution"""

    def _get_propagate_parent(self) -> Optional["PipelineStorageObject"]:
        return self.get_pipeline_result()

    def get_task(self) -> "Task":
        """Gets the registered task class"""
        from wildcoeus.pipelines.tasks import task_registry

        return task_registry.load_task_from_id(
            pipeline_task=self.pipeline_task,
            task_id=self.task_id,
            config=self.config,
        )


class TaskResult(PipelineStorageObject):
    content_type_name = "TaskResult"

    get_id: Callable[[], Any]
    """Returns id of the task result in the storage"""

    get_task_id: Callable[[], str]
    """Gets the id of the registered task class"""

    get_pipeline_task: Callable[[], str]
    """Gets the name of the task property on the pipeline class"""

    get_config: Callable[[], Dict[str, Any]]
    """Gets the task config"""

    get_serializable_pipeline_object: Callable[[], Dict[str, Any]]
    """Returns the object this instance of the pipeline was started with"""

    get_pipeline_object: Callable[[], "Pipeline"]
    """Gets the deserialized pipeline object"""

    get_serializable_task_object: Callable[[], Dict[str, Any]]
    """Returns the object this instance of the pipeline was started with"""

    get_task_object: Callable[[], "Task"]
    """Gets the deserialized task object"""

    get_task_execution: Callable[[], TaskExecution]
    """Returns the task execution related to this object"""

    get_pipeline: Callable[[], "Pipeline"]
    """Returns the registered pipeline class"""

    get_task: Callable[[], "Task"]
    """Gets the registered task class"""

    def _get_propagate_parent(self) -> Optional["PipelineStorageObject"]:
        return self.get_task_execution()

    def get_task(self) -> "Task":
        """Gets the registered task class"""
        return self.get_task_execution().get_task()

    def get_duration(self):
        """
        Returns the duration of the task
        """
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
        """
        Returns the ``PipelineDigest`` object providing stats for all registered pipeline
        classes.
        """
        raise NotImplementedError()

    def get_pipeline_executions(
        self, pipeline_id: Optional[str] = None
    ) -> Sequence[PipelineExecution]:
        """
        Gets all pipeline executions from the storage. If ``pipeline_id`` is supplied
        only executions for the given pipeline id will be returned

        :param pipeline_id: The id of the registered pipeline class
        """
        raise NotImplementedError()

    def get_pipeline_execution(self, run_id) -> PipelineExecution | None:
        """
        Fetch a specific pipeline execution from the storage.

        If the pipeline execution isn't found, None will be returned.

        :param run_id: The id of the pipeline run to fetch the execution for
        """
        raise NotImplementedError()

    def get_pipeline_results(
        self, run_id: Optional[str] = None
    ) -> Sequence[PipelineResult]:
        """
        Gets all pipeline results from the storage. If ``run_id`` is supplied only results
        for that particular run will be returned.

        :param run_id: The id of the run to filter results by
        """
        raise NotImplementedError()

    def get_pipeline_result(self, _id) -> PipelineResult | None:
        """
        Fetch a specific pipeline result from the storage.

        If the pipeline result isn't found, None will be returned.

        :param _id: The id of the result to fetch from storage
        """
        raise NotImplementedError()

    def get_task_executions(
        self, run_id: Optional[str] = None, pipeline_result_id: Optional[str] = None
    ) -> Sequence[TaskExecution]:
        """
        Gets all task executions from the storage.

        :param run_id: The id of the run to filter results by
        :param pipeline_result_id: The id of the parent pipeline result object to filter results by
        """
        raise NotImplementedError()

    def get_task_execution(self, _id) -> TaskExecution | None:
        """
        Fetch a specific task execution from the storage.

        If the pipeline result isn't found, None will be returned.

        :param _id: The id of the task execution to fetch from storage
        """
        raise NotImplementedError()

    def get_task_results(
        self,
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
        raise NotImplementedError()

    def get_task_result(self, _id) -> TaskResult | None:
        """
        Fetch a specific task result from the storage.

        If the pipeline result isn't found, None will be returned.

        :param _id: The id of the task result to fetch from storage
        """
        raise NotImplementedError()

    def cleanup(self, before: Optional[datetime] = None) -> Sequence[str]:
        """
        Removes all results objects from the storage.

        :param before: If set only objects created before the date will be removed. Otherwise
            all will be removed.
        """
        raise NotImplementedError()

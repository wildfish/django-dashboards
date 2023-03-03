from typing import Any, Dict, Optional, Type

from django.core.exceptions import ImproperlyConfigured

from pydantic import BaseModel, Extra, ValidationError

from wildcoeus.meta import ClassWithAppConfigMeta
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import TaskResult
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.registry import task_registry
from wildcoeus.registry.registry import Registrable


class TaskConfig(BaseModel):
    """
    Base class all task configs should be built from
    """

    class Config:
        extra = Extra.allow


class Task(Registrable, ClassWithAppConfigMeta):
    """
    The base task class that all tasks should extend to implement
    your own tasks.
    """

    pipeline_task: str
    """
    The attribute this tasks is named against. This is set via
    :code:`__init_subclass__` on Pipeline
    """

    ConfigType: Type[TaskConfig] = TaskConfig
    """pydantic class used to validate the task arguments"""

    InputType: Optional[Type[BaseModel]] = None
    """pydantic class used to validate task input data"""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not cls._meta.abstract:
            task_registry.register(cls)

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.task_id = self.get_id()
        self._config = config or {}
        self.cleaned_config = self.clean_config(config or {})
        self.pipeline_object: Optional[Any] = None
        self.task_object: Optional[Any] = None

    @classmethod
    def get_iterator(cls):
        """
        Returns an iterator for multiple instances of the task to be started with.
        If no iteration is required, :code:`None` should be returned.
        """
        return None

    @staticmethod
    def get_serializable_task_object(obj):
        """
        Converts the object to a json serializable version to be stored
        in the db.

        :param obj: The object to store
        """
        if obj is None:
            return None

        return {
            "obj": obj,
        }

    def clean_config(self, config: Dict[str, Any]):
        """
        Validates the supplied config against the defined :code:`ConfigType`

        :param config: The config to check
        """
        try:
            model = self.ConfigType(**(config or {}))
            return model
        except ValidationError as e:
            raise ConfigValidationError(self, e.json(indent=False))

    def clean_input_data(self, input_data: Dict[str, Any]):
        """
        Validates the supplied input data against the defined :code:`InputType`

        :param input_data: The config to check
        """
        if input_data and self.InputType is None:
            raise InputValidationError(
                self, "Input data was provided when no input type was specified"
            )

        if self.InputType is None:
            return None

        try:
            model = self.InputType(**(input_data or {}))
            return model
        except ValidationError as e:
            raise InputValidationError(self, e.json(indent=False))

    def start(
        self,
        task_result: TaskResult,
        reporter: PipelineReporter,
    ):
        """
        Starts the task running. The status of the task result will be updated
        on starting and finishing.

        :param task_result: The task result object representing this task.
        :param reporter: The pipeline reporter to write status changes to.
        """
        try:
            task_result.report_status_change(reporter, PipelineTaskStatus.RUNNING)

            self.pipeline_object = task_result.get_pipeline_object()
            self.task_object = task_result.get_task_object()

            # run the task
            self.run(
                pipeline_id=task_result.get_pipeline_id(),
                run_id=task_result.get_run_id(),
                cleaned_data=task_result.get_task().clean_input_data(
                    task_result.get_input_data()
                ),
            )

            # update the result as completed
            task_result.report_status_change(
                reporter, PipelineTaskStatus.DONE, propagate=False
            )

            return True
        except (InputValidationError, Exception) as e:
            status = (
                PipelineTaskStatus.VALIDATION_ERROR
                if isinstance(e, InputValidationError)
                else PipelineTaskStatus.RUNTIME_ERROR
            )
            task_result.report_status_change(reporter, status, message=str(e))
            raise

    def run(
        self,
        pipeline_id: str,
        run_id: str,
        cleaned_data: Optional[BaseModel],
    ):  # pragma: no cover
        """
        The tasks business logic. When writing custom tasks this needs to be
        implemented with your own logic.

        :param pipeline_id: The id of the registered pipeline the task is part of
        :param run_id: The id of the current pipeline run
        :param cleaned_data: The cleaned input data (based on :code:`InputType`)
        """
        raise NotImplementedError("run not implemented")

    @classmethod
    def get_id(cls):
        """
        Generates the tasks id based in the app label and class name.
        """
        return "{}.{}".format(cls._meta.app_label, cls.__name__)


class ModelTask(Task):
    """
    The base task class to use when iterating over many model instances.
    """

    class Meta:
        model: Optional[str]
        """The model class to use when fetching objects from the database"""

    def get_queryset(self, *args, **kwargs):
        """
        Returns a queryset containing all items for the model provided in the meta.
        If :code:`model` is not defined on the :code:`Meta` class this method must be
        overridden otherwise an :code:`ImproperlyConfigured` error will be raised.
        """
        if self._meta.model is not None:
            queryset = self._meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.Meta.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset

    def get_iterator(self):
        """
        Returns an iterator to run the task over. By default this returns the result
        of :code:`get_queryset`.
        """
        return self.get_queryset()

    @staticmethod
    def get_serializable_task_object(obj):
        """
        Serializes an django model object so that it can be stored on the task result
        object.

        If :code:`obj` is not :code:`None` the object will be stored as a dictionary containing
        :code:`pk`, :code:`app_label` and :code:`model_name` so that the object can be retrieved
        from the database.

        :param obj: The object to serialize
        """
        if not obj:
            return None

        return {
            "pk": obj.pk,
            "app_label": obj._meta.app_label,
            "model_name": obj._meta.model_name,
        }


class TaskError(Exception):
    """
    Base error raised by tasks
    """

    def __init__(self, task: Task, msg: str):
        super().__init__(msg)
        self.task = task
        self.msg = msg


class ConfigValidationError(TaskError):
    """
    Error raised when there is one or more errors in the task config
    """

    pass


class InputValidationError(TaskError):
    """
    Error raised when there is one or more errors in the task input data
    """

    pass
